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
        defunct_codes = ['URS', 'GDR', 'FRG', 'EUN', 'ROC', 'TCH', 'YUG', 'SCG', 'BOH', 'ANZ', 'RU1', 'UAR', 'RUS', 'BLR']
        df = df[~df['country_3_letter_code'].isin(defunct_codes)]

        results = []
        if df.empty:
            return results

        # --- PREPARE BATCH INPUT ---
        # We need a DataFrame that matches the model's expected features exactly.
        
        # 1. XGBoost Preparation
        if self.xgb_model and self.xgb_features:
            # Init with 0 using index from df
            X_xgb = pd.DataFrame(0, index=df.index, columns=self.xgb_features)
            
            # Map features available in DB
            # Note: feature names must match exactly what XGB expects
            if 'total_athletes' in self.xgb_features: X_xgb['total_athletes'] = df['total_athletes']
            if 'avg_athlete_age' in self.xgb_features: X_xgb['avg_athlete_age'] = df['avg_age_athletes'].fillna(24.0)
            if 'medalist_athletes' in self.xgb_features: X_xgb['medalist_athletes'] = df['total_medals']
            if 'avg_athlete_experience' in self.xgb_features: X_xgb['avg_athlete_experience'] = 1.0
            if 'avg_games_participation' in self.xgb_features: X_xgb['avg_games_participation'] = 1.0
            if 'gdp_per_capita' in self.xgb_features: X_xgb['gdp_per_capita'] = df.get('gdp_per_capita', 0)
            if 'population' in self.xgb_features: X_xgb['population'] = df.get('population', 0)
            
            # Host logic (France)
            if 'is_host' in self.xgb_features:
                X_xgb['is_host'] = (df['country_3_letter_code'] == 'FRA').astype(int)
            
            # OHE (Country Codes)
            # This is tricky in batch if we don't know all columns, but self.xgb_features has them.
            # We iterate only over countries present to set their specific OHE column
            for idx, row in df.iterrows():
                code = row['country_3_letter_code']
                ohe_col = f"country_3_letter_code_{code}"
                if ohe_col in self.xgb_features:
                    X_xgb.at[idx, ohe_col] = 1

            # Predict Batch
            try:
                # Ensure column order matches
                X_xgb = X_xgb[self.xgb_features]
                xgb_preds = self.xgb_model.predict(X_xgb)
                df['xgb_pred'] = [max(0, int(round(x))) for x in xgb_preds]
            except Exception as e:
                print(f"XGB Batch Error: {e}")
                df['xgb_pred'] = 0
        else:
            df['xgb_pred'] = 0

        # 2. Random Forest Preparation
        if self.rf_model and self.rf_features:
            X_rf = pd.DataFrame(0, index=df.index, columns=self.rf_features)
            
            if 'total_athletes' in self.rf_features: X_rf['total_athletes'] = df['total_athletes']
            if 'avg_age_athletes' in self.rf_features: X_rf['avg_age_athletes'] = df['avg_age_athletes'].fillna(24.0)
            if 'cumulative_medals' in self.rf_features: X_rf['cumulative_medals'] = df['cumulative_medals']
            if 'is_host' in self.rf_features: X_rf['is_host'] = (df['country_3_letter_code'] == 'FRA').astype(int)
            if 'season_Winter' in self.rf_features: X_rf['season_Winter'] = 0
            
            try:
                X_rf = X_rf[self.rf_features]
                rf_preds = self.rf_model.predict(X_rf)
                df['rf_pred'] = [max(0, int(round(x))) for x in rf_preds]
            except Exception as e:
                print(f"RF Batch Error: {e}")
                df['rf_pred'] = 0
        else:
             df['rf_pred'] = 0

        # 3. Aggregate Results
        for _, row in df.iterrows():
             xgb_p = row.get('xgb_pred', 0)
             rf_p = row.get('rf_pred', 0)
             consensus = int(round((xgb_p + rf_p) / 2))
             
             results.append({
                'country': row['country_3_letter_code'],
                'predicted_medals_xgb': xgb_p, 
                'predicted_medals_rf': rf_p,
                'predicted_medals': consensus,
                'baseline_athletes': int(row['total_athletes'])
             })

        # Sort by Consensus
        results.sort(key=lambda x: x['predicted_medals'], reverse=True)
        
        return results
