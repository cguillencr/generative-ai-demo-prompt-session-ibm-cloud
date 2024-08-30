import requests
import json
import os
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from datetime import datetime, timezone

access_token = None
token_file = "access_token.json"
api_key = os.getenv("IBM_API_KEY")
region = os.getenv("IBM_REGION")
project_id = os.getenv("IBM_PROJECT_ID")

def is_token_valid(token):
    try:
        # Decode the JWT without verifying the signature
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        
        # Get the expiration time from the token (exp claim)
        exp_timestamp = decoded_token.get("exp")
        
        if exp_timestamp:
            # Convert the expiration time to a datetime object
            exp_time = datetime.fromtimestamp(exp_timestamp, timezone.utc)
            # Check if the token is still valid
            return exp_time > datetime.now(timezone.utc)
        return False
    except (ExpiredSignatureError, DecodeError):
        return False


# Check if the access_token.json file exists
if os.path.exists(token_file):
    # Load the access token from the file
    with open(token_file, "r") as file:
        data = json.load(file)
        access_token = data.get("access_token")
        
        # Check if the token is valid
        if access_token and is_token_valid(access_token):
            print("Access token loaded from access_token.json and is still valid.")
        else:
            print("Access token has expired or is invalid.")
            access_token = None
        

# If access_token is not loaded, request a new one
if not access_token:
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }

    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        response_data = response.json()
        
        # Extract the access token
        access_token = response_data.get("access_token")
        
        if access_token:
            # Serialize the access token into a file
            with open(token_file, "w") as file:
                json.dump({"access_token": access_token}, file)
            print("Access token saved to access_token.json")
        else:
            print("Access token not found in the response.")
    else:
        print(f"Failed to retrieve access token. Status code: {response.status_code}")
        print(response.text)
else:
    print("Access token loaded from access_token.json")

# Now you can use the access_token as needed
print(f"Access Token: {access_token}")


url = f"https://{region}.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

body = {
	"input": """Answer the following question using only information from the article. If there is no good answer in the article, say \"I don'\''t know\".

Article: 
###
Tomatoes are one of the most popular plants for vegetable gardens. Tip for success: If you select varieties that are resistant to disease and pests, growing tomatoes can be quite easy. For experienced gardeners looking for a challenge, there are endless heirloom and specialty varieties to cultivate. Tomato plants come in a range of sizes. There are varieties that stay very small, less than 12 inches, and grow well in a pot or hanging basket on a balcony or patio. Some grow into bushes that are a few feet high and wide, and can be grown is larger containers. Other varieties grow into huge bushes that are several feet wide and high in a planter or garden bed. Still other varieties grow as long vines, six feet or more, and love to climb trellises. Tomato plants do best in full sun. You need to water tomatoes deeply and often. Using mulch prevents soil-borne disease from splashing up onto the fruit when you water. Pruning suckers and even pinching the tips will encourage the plant to put all its energy into producing fruit.
###

Question: Is growing tomatoes easy?
Answer: Yes, if you select varieties that are resistant to disease and pests.

Question: What varieties of tomatoes are there?
Answer: There are endless heirloom and specialty varieties.

Question: Why should you use mulch when growing tomatoes?
Answer:""",
	"parameters": {
		"decoding_method": "greedy",
		"max_new_tokens": 100,
		"stop_sequences": ["\n\n"],
		"repetition_penalty": 1
	},
	"model_id": "ibm/granite-13b-chat-v2",
	"project_id": f"{project_id}"
}

headers = {
	"Accept": "application/json",
	"Content-Type": "application/json",
	"Authorization":f"Bearer {access_token}"
}

response = requests.post(
	url,
	headers=headers,
	json=body
)

if response.status_code != 200:
	raise Exception("Non-200 response: " + str(response.text))

data = response.json()
print(data)