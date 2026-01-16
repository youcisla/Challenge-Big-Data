
import joblib
import sys
import sklearn

print(f"Python version: {sys.version}")
print(f"Scikit-learn version: {sklearn.__version__}")

model_path = r'C:\Users\Y.chehboub\Downloads\ChallengeBigData\ml_models\medals_prediction_model.pkl'

try:
    print("Attempting joblib.load...")
    model = joblib.load(model_path)
    
    print(f"\nType: {type(model)}")
    print(f"Model: {model}")

    if hasattr(model, 'feature_names_in_'):
        print(f"\nFeature Names in: {list(model.feature_names_in_)}")
    else:
        print("\nNo feature_names_in_ found.")
        
except Exception as e:
    print(f"Error loading model with joblib: {e}")
