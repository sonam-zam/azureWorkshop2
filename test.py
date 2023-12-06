import requests
import json



# Endpoint and headers setup
endpoint_url = "https://azurepoc1.cognitiveservices.azure.com/customvision/v3.0/Prediction/6367cdde-d0f8-4cf9-b867-1b1793ad7e76/classify/iterations/Iteration1/url"
headers = {
    "Prediction-Key": "00e15d939583442eaedae66af2523e92",
    "Content-Type": "application/json",
  
}

# Image URL
payload = json.dumps({"Url": "https://www.rd.com/wp-content/uploads/2021/06/GettyImages-1205998407-e1624731290663.jpg?resize=768%2C512"})

# API call
response = requests.post(endpoint_url, headers=headers, data=payload)

# Output results
results = response.json()
print(results)