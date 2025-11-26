from fastapi import FastAPI
from pydantic import BaseModel
from prediction import make_prediction

app = FastAPI()

class PredictionRequest(BaseModel):
    tenure: float
    monthly: float
    techsupport: float

@app.post("/predict")
def predict(request: PredictionRequest):
    """Predict customer churn"""
    try:
        prediction = make_prediction(
            tenure=request.tenure,
            MonthlyCharges=request.monthly,
            TechSupport_yes=request.techsupport
        )
        return {
            "prediction": float(prediction),
            "tenure": request.tenure,
            "monthly": request.monthly,
            "techsupport": request.techsupport
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
