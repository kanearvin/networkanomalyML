import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import uvicorn

app = FastAPI(
    title="Network Intrusion Detection API",
    description="Real-time network anomaly detection engine.",
    version="1.0"
)

# 1. Resolve the absolute path to the models directory
# This ensures it finds the models no matter where you run the script from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# If your models are in a folder named 'models' at the same level as this script:
MODEL_PATH = os.path.join(BASE_DIR, "models", "unsw_lgbm.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "unsw_scaler.pkl")

# If your 'models' folder is one directory up from 'src/app.py', use this instead:
# MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "unsw_lgbm.pkl")
# SCALER_PATH = os.path.join(BASE_DIR, "..", "models", "unsw_scaler.pkl")

# 2. Load the artifacts securely
try:
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        raise FileNotFoundError(f"Missing files. Looking for models at:\n{MODEL_PATH}\n{SCALER_PATH}")
        
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("✅ Model and scaler loaded successfully.")
except Exception as e:
    # If they fail to load, define them as None so the server doesn't crash on startup,
    # but the /predict endpoint will know why it failed.
    print(f"❌ Error loading model artifacts: {e}")
    model = None
    scaler = None

class NetworkFlow(BaseModel):
    features: dict

@app.get("/")
def health_check():
    return {"status": "Active", "message": "API is up and running."}

@app.post("/predict")
def predict_anomaly(flow: NetworkFlow):
    # Check if the scaler and model actually loaded
    if scaler is None or model is None:
         raise HTTPException(status_code=500, detail="Server Error: Model or Scaler failed to load on startup. Check terminal logs for the exact path it searched.")

    try:
        df_features = pd.DataFrame([flow.features])
        
        # Ensure the column order matches exactly what the scaler expects
        # (Assuming 'scaler.feature_names_in_' is available from Scikit-Learn 1.0+)
        if hasattr(scaler, 'feature_names_in_'):
            df_features = df_features[scaler.feature_names_in_]
            
        scaled_features = scaler.transform(df_features)
        
        prediction = model.predict(scaled_features)[0]
        probability = model.predict_proba(scaled_features)[0][1]
        
        return {
            "status": "success",
            "is_anomaly": bool(prediction == 1),
            "threat_probability": round(float(probability), 4),
            "alert_level": "CRITICAL" if prediction == 1 else "NORMAL"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Inference error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)