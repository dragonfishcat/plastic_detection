from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

app = FastAPI()

# Allow connections from anywhere (for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Backend running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Simulate processing delay
    time.sleep(0.5)

    return JSONResponse({
        "plastic_type": "PET",
        "confidence": 0.93,
        "timestamp": time.time()
    })
