import requests

# Define the API endpoint
url = 'http://127.0.0.1:5000/predict'

# Path to the image file
image_path = '/Users/onkar/Downloads/joel_photos/2023-11-10_10-20-31890.jpg'

# Send the image in a POST request
with open(image_path, 'rb') as img:
    files = {'file': img}
    response = requests.post(url, files=files)

# Output the result
if response.status_code == 200:
    print("Prediction:", response.json().get("prediction"))
else:
    print(f"Error: {response.status_code}, {response.text}")
