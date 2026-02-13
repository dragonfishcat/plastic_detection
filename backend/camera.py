import cv2
import requests

API_URL = "http://127.0.0.1:8000/predict"

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imwrite("temp.jpg", frame)

    with open("temp.jpg", "rb") as f:
        response = requests.post(API_URL, files={"file": f})

    result = response.json()
    print(result)

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1000) & 0xFF == ord('q'):  # 1 photo per second
        break

cap.release()
cv2.destroyAllWindows()
