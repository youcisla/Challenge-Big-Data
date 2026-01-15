import pickle
import sys
import os
import pandas as pd
import numpy as np

# Add project root to path just in case
sys.path.append(os.getcwd())

MODEL_PATH = 'ml_models/best_xgb_model.pkl'

def inspect():
    print(f"Loading model from {MODEL_PATH}...")
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        
        print(f"Model Type: {type(model)}")
        
        if hasattr(model, 'feature_names_in_'):
            print("\n--- Feature Names ---")
            print(list(model.feature_names_in_))
        elif hasattr(model, 'get_booster'):
            print("\n--- XGBoost Features ---")
            print(model.get_booster().feature_names)
        else:
            print("Could not directly retrieve feature names. Listing attributes:")
            print(dir(model))
            
    except Exception as e:
        print(f"Error loading model: {e}")

if __name__ == "__main__":
    inspect()
