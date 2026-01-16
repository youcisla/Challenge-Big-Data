
import pickle
import sys
import os
import pandas as pd
import sklearn

print(f"Python version: {sys.version}")
print(f"Scikit-learn version: {sklearn.__version__}")

model_path = r'C:\Users\Y.chehboub\Downloads\ChallengeBigData\ml_models\medals_prediction_model.pkl'

try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    print(f"\nType: {type(model)}")
    print(f"Model: {model}")

    if hasattr(model, 'feature_names_in_'):
        print(f"\nFeature Names in: {model.feature_names_in_}")
        print(f"Number of features: {len(model.feature_names_in_)}")
    elif hasattr(model, 'get_booster'):
        print(f"\nXGBoost Booster Feature Names: {model.get_booster().feature_names}")
    
except Exception as e:
    print(f"Error loading model: {e}")
