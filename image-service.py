from fastapi import FastAPI, File, UploadFile
import requests 

app = FastAPI()

PREDICTION_KEY = "00e15d939583442eaedae66af2523e92"
ENDPOINT_URL = "https://eastus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/5a19b51b-f19e-4972-92f2-62c2fcf5f87f/classify/iterations/imagenetAzure/image"

def classify_image(image_data):
    headers = {
        "Prediction-Key": "00e15d939583442eaedae66af2523e92",
    "Content-Type": "application/json",
    }
    response = requests.post(ENDPOINT_URL, headers=headers, data=image_data)
    return response.json()


def process_results(result):
    for label in result:
        print(f"Label: {label['tagName']}, Confidence: {label['probability']}")

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # Read image data
    image_data = await file.read()

    # Call classify_image function
    result = classify_image(image_data)

    # Process and print the results
    process_results(result)