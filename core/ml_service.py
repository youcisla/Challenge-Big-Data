import pickle
import joblib
import pandas as pd
import numpy as np
import xgboost as xgb
from django.conf import settings
from .models import OlympicStats
import os

class MLService:
    _instance = None
    xgb_model = None
    rf_model = None
    xgb_features = None
    rf_features = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLService, cls).__new__(cls)
            cls._instance.load_models()
        return cls._instance

    def load_models(self):
        # 1. Load Legacy XGBoost Model (Pickle)
        try:
            xgb_path = os.path.join(settings.BASE_DIR, 'ml_models', 'best_xgb_model.pkl')
            print(f"Loading XGBoost from: {xgb_path}")
            with open(xgb_path, 'rb') as f:
                self.xgb_model = pickle.load(f)
            
            # Extract features for XGB
            if hasattr(self.xgb_model, 'feature_names_in_'):
                self.xgb_features = list(self.xgb_model.feature_names_in_)
            elif hasattr(self.xgb_model, 'get_booster'):
                self.xgb_features = self.xgb_model.get_booster().feature_names
            else:
                self.xgb_features = []
            print(f"XGBoost loaded. Features: {len(self.xgb_features)}")
            
        except Exception as e:
            print(f"Failed to load XGBoost: {e}")
            self.xgb_model = None

        # 2. Load New Random Forest Model (Joblib)
        try:
            rf_path = os.path.join(settings.BASE_DIR, 'ml_models', 'medals_prediction_model.pkl')
            print(f"Loading Random Forest from: {rf_path}")
            # Ensure we use joblib as identified
            self.rf_model = joblib.load(rf_path)
            
            # Extract features for RF
            if hasattr(self.rf_model, 'feature_names_in_'):
                self.rf_features = list(self.rf_model.feature_names_in_)
            else:
                # Fallback based on inspection
                self.rf_features = ['total_athletes', 'avg_age_athletes', 'cumulative_medals', 'is_host', 'season_Winter']
            print(f"Random Forest loaded. Features: {len(self.rf_features)}")
            
        except Exception as e:
            print(f"Failed to load Random Forest: {e}")
            self.rf_model = None

    def predict_paris_2024(self):
        # 1. Get Baseline Data (Latest Summer Games - Tokyo 2020)
        qs = OlympicStats.objects.filter(season='Summer').values(
            'country_3_letter_code', 'year',
            'total_athletes', 'total_medals',
            'avg_age_athletes', 'cumulative_medals'
        )
        
        df = pd.DataFrame(list(qs))
        if df.empty:
            return []

        # Keep latest summer entry per country
        df = df.sort_values('year', ascending=False).drop_duplicates('country_3_letter_code')
        
        # Filter Defunct
        defunct_codes = ['URS', 'GDR', 'FRG', 'EUN', 'ROC', 'TCH', 'YUG', 'SCG', 'BOH', 'ANZ', 'RU1', 'UAR']
        df = df[~df['country_3_letter_code'].isin(defunct_codes)]
        
        results = []
        
        # Pre-process for models
        for _, row in df.iterrows():
            country_code = row['country_3_letter_code']
            
            # --- XGB PREDICTION ---
            xgb_pred = 0
            if self.xgb_model and self.xgb_features:
                # Construct XGB Input
                xgb_input = {feat: 0 for feat in self.xgb_features}
                
                # Mappings (Same as before)
                if 'total_athletes' in self.xgb_features: xgb_input['total_athletes'] = row.get('total_athletes', 0)
                if 'avg_athlete_age' in self.xgb_features: xgb_input['avg_athlete_age'] = row.get('avg_age_athletes', 24.0)
                if 'medalist_athletes' in self.xgb_features: xgb_input['medalist_athletes'] = row.get('total_medals', 0)
                if 'avg_athlete_experience' in self.xgb_features: xgb_input['avg_athlete_experience'] = 1.0
                if 'avg_games_participation' in self.xgb_features: xgb_input['avg_games_participation'] = 1.0
                
                # Host logic
                if 'is_host' in xgb_input: 
                    xgb_input['is_host'] = 1 if country_code == 'FRA' else 0
                    
                # OHE
                ohe_col = f"country_3_letter_code_{country_code}"
                if ohe_col in xgb_input: xgb_input[ohe_col] = 1
                
                # Predict XGB
                X_xgb = pd.DataFrame([xgb_input])[self.xgb_features] # Ensure order
                xgb_pred = max(0, int(round(self.xgb_model.predict(X_xgb)[0])))

            # --- RF PREDICTION ---
            rf_pred = 0
            if self.rf_model and self.rf_features:
                # Construct RF Input
                # Features: ['total_athletes', 'avg_age_athletes', 'cumulative_medals', 'is_host', 'season_Winter']
                rf_input = {}
                rf_input['total_athletes'] = row.get('total_athletes', 0)
                rf_input['avg_age_athletes'] = row.get('avg_age_athletes', 24.0)
                rf_input['cumulative_medals'] = row.get('cumulative_medals', 0)
                rf_input['is_host'] = 1 if country_code == 'FRA' else 0
                rf_input['season_Winter'] = 0 # Summer Games
                
                # Ensure all features present (in case model has more)
                for f in self.rf_features:
                    if f not in rf_input: rf_input[f] = 0
                    
                # Predict RF
                X_rf = pd.DataFrame([rf_input])[self.rf_features]
                rf_pred = max(0, int(round(self.rf_model.predict(X_rf)[0])))
                
            # Consensus / Best Estimate
            # We can take the average or choose one. Let's provide both + Average
            avg_pred = int(round((xgb_pred + rf_pred) / 2))
            
            results.append({
                'country': country_code,
                'predicted_medals_xgb': xgb_pred, # Legacy (Oracle V1)
                'predicted_medals_rf': rf_pred,   # New (Oracle V2: Random Forest)
                'predicted_medals': avg_pred,     # Consensus (Main Display)
                'baseline_athletes': int(row.get('total_athletes', 0))
            })
            
        # Sort by Consensus
        results.sort(key=lambda x: x['predicted_medals'], reverse=True)
        
        return results
