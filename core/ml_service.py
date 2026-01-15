import pickle
import pandas as pd
import numpy as np
import xgboost as xgb
from django.conf import settings
from .models import OlympicStats
import os

class MLService:
    _instance = None
    model = None
    feature_names = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLService, cls).__new__(cls)
            cls._instance.load_model()
        return cls._instance

    def load_model(self):
        try:
            model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'best_xgb_model.pkl')
            print(f"Loading model from: {model_path}")
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            # Extract expected feature names
            if hasattr(self.model, 'feature_names_in_'):
                self.feature_names = list(self.model.feature_names_in_)
            elif hasattr(self.model, 'get_booster'):
                self.feature_names = self.model.get_booster().feature_names
            else:
                self.feature_names = []
                print("Warning: Could not retrieve feature names from model.")
                
            print(f"Model loaded successfully. Expecting {len(self.feature_names)} features.")
            
        except Exception as e:
            print(f"Failed to load model: {e}")
            self.model = None

    def predict_paris_2024(self):
        if not self.model:
            return []

        # 1. Get Baseline Data (Latest Summer Games - Tokyo 2020)
        # We need stats like 'total_athletes', 'avg_athlete_age' etc.
        # We'll fetch the most recent Summer participation for each country
        
        # Get all stats for Summer
        qs = OlympicStats.objects.filter(season='Summer').values(
            'country_3_letter_code', 'year',
            'total_athletes', 'total_medals',
            'avg_age_athletes'
        )
        
        df = pd.DataFrame(list(qs))
        
        if df.empty:
            return []

        # Sort by year desc and drop duplicates to keep only latest Summer entry per country
        df = df.sort_values('year', ascending=False).drop_duplicates('country_3_letter_code')
        
        # FILTER DEFUNCT COUNTRIES
        # We want to exclude historical entities that won't participate in 2024
        defunct_codes = ['URS', 'GDR', 'FRG', 'EUN', 'ROC', 'TCH', 'YUG', 'SCG', 'BOH', 'ANZ', 'RU1', 'UAR']
        df = df[~df['country_3_letter_code'].isin(defunct_codes)]
        
        # 2. Prepare Features for Prediction
        # We need to construct a DataFrame that matches self.feature_names EXACTLY
        
        prediction_data = []
        
        for _, row in df.iterrows():
            country_code = row['country_3_letter_code']
            
            # Base dict with all features initialized to 0
            row_input = {feat: 0 for feat in self.feature_names}
            
            # --- FEATURE MAPPING & PROXIES ---
            # 1. Total Athletes (Direct)
            if 'total_athletes' in self.feature_names:
                row_input['total_athletes'] = row.get('total_athletes', 0)
            
            # 2. Avg Athlete Age (Mapped from avg_age_athletes)
            if 'avg_athlete_age' in self.feature_names:
                row_input['avg_athlete_age'] = row.get('avg_age_athletes', 24.0)

            # 3. Medalist Athletes (Missing in DB -> Proxy: Use total_medals)
            # Assumption: Number of medalists is roughly proportional to total medals
            if 'medalist_athletes' in self.feature_names:
                row_input['medalist_athletes'] = row.get('total_medals', 0)
                
            # 4. Avg Experience (Missing in DB -> Proxy: Default value)
            if 'avg_athlete_experience' in self.feature_names:
                row_input['avg_athlete_experience'] = 1.0 # Default to 1 participation
            
            # 5. AVG Games Participation (If exists)
            if 'avg_games_participation' in self.feature_names:
                row_input['avg_games_participation'] = 1.0
            
            # Host Flag (Paris 2024 -> France is host)
            if 'is_host' in row_input:
                row_input['is_host'] = 1 if country_code == 'FRA' else 0
                
            # One-Hot Encoding for Country
            # Model expects 'country_3_letter_code_USA' = 1
            ohe_col = f"country_3_letter_code_{country_code}"
            if ohe_col in row_input:
                row_input[ohe_col] = 1
            
            # Store inputs with metadata
            row_input['_country_code'] = country_code
            row_input['_total_athletes'] = row.get('total_athletes', 0) # Store for display
            prediction_data.append(row_input)
            
        pred_df = pd.DataFrame(prediction_data)
        
        if pred_df.empty:
            return []

        # 3. Create X (Features only)
        # Filter columns to only those expected by the model
        X = pred_df[self.feature_names]
        
        # 4. Predict
        preds = self.model.predict(X)
        
        # 5. Pack results
        results = []
        for idx, pred_value in enumerate(preds):
            country_code = pred_df.iloc[idx]['_country_code']
            results.append({
                'country': country_code,
                'predicted_medals': max(0, int(round(pred_value))), # Relu-like safety
                'baseline_athletes': int(pred_df.iloc[idx].get('_total_athletes', 0))
            })
            
        # Sort by predicted medals desc
        results.sort(key=lambda x: x['predicted_medals'], reverse=True)
        
        return results
