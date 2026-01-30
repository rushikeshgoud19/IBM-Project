import requests
import json

# ======================================================
# ✅ CREDENTIALS
# ======================================================
REAL_API_KEY = "DlsN6zvlNDvx4MIIiAgj5RiGqAO09AUhazmS4MQNsvkx"
DEPLOYMENT_ID = "e77ce284-a5fa-4dd0-a891-528ee92080e4"

def get_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={api_key}"
    
    print("1. Authenticating...")
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"❌ Auth Failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Network Error: {e}")
        return None

def call_boardroom(token):
    # Endpoint
    url = f"https://us-south.ml.cloud.ibm.com/ml/v1/deployments/{DEPLOYMENT_ID}/text/chat?version=2023-05-29"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Simple Payload to test connection
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Act as Project Sovereign Architect. Confirm systems online."
            }
        ]
    }

    print("2. Connecting to Boardroom...")
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # ✅ DEBUG PRINT: Shows us exactly what happened
        print(f"   (Status Code: {response.status_code})")
        
        if response.status_code == 200:
            return response.json() # Return dictionary if success
        else:
            return {"error": response.text} # Return dictionary with error text if fail
            
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    token = get_token(REAL_API_KEY)
    if token:
        result = call_boardroom(token)
        
        print("\n=== RAW RESPONSE START ===")
        # This will print the result SAFELY without crashing
        print(json.dumps(result, indent=2))
        print("=== RAW RESPONSE END ===")