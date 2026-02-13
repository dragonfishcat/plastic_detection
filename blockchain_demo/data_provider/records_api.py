from flask import Flask, jsonify
import json
import time
import requests
app = Flask(__name__)

@app.route("/records", methods=["GET"])
def get_records():
    response = requests.post("http://api-url/predict", files={"file": open("img.jpg", "rb")})
    data = response.json()  # Convert JSONResponse to Python dict
    print(data)
    request_id = data["request_id"]
    plastic_type = data["plastic_type"]
    confidence = float(data["confidence"])
    image_hash = data["image_hash"]
    timestamp = float(data["timestamp"])
    verification_status = data["verification_status"]


    
    return jsonify([
        {
            "request_id": request_id,
            "plastic_type": plastic_type,
            "confidence": confidence,
            "image_hash": image_hash,
            "timestamp": timestamp,
            "verification_status": verification_status
        }])

if __name__ == "__main__":
    app.run(port=6000)
