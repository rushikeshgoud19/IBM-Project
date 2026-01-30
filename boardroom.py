import requests
import json
import time

# ======================================================
# ✅ CREDENTIALS
# ======================================================
REAL_API_KEY = "DlsN6zvlNDvx4MIIiAgj5RiGqAO09AUhazmS4MQNsvkx"
DEPLOYMENT_ID = "e77ce284-a5fa-4dd0-a891-528ee92080e4"

# ======================================================
# 🤖 THE BOARD (ADVISORS)
# ======================================================
AGENTS = [
    {
        "name": "CHIEF ARCHITECT",
        "persona": "You are the Chief Technology Architect. Focus on code stability, security, and technical debt. Be critical."
    },
    {
        "name": "CFO (FINANCE)",
        "persona": "You are the Chief Financial Officer. Focus on budget, ROI, and cutting costs. You hate risky spending."
    },
    {
        "name": "COO (OPERATIONS)",
        "persona": "You are the Chief Operating Officer. Focus on speed, logistics, and execution timelines. You want results fast."
    }
]

def get_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={api_key}"
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()["access_token"]
    except:
        pass
    return None

def call_ai(token, persona, prompt):
    # Sends data to IBM Granite
    url = f"https://us-south.ml.cloud.ibm.com/ml/v1/deployments/{DEPLOYMENT_ID}/text/chat?version=2023-05-29"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Combine Persona + Prompt into one message to avoid role errors
    full_message = f"{persona}\n\nTask: {prompt}"
    
    payload = {
        "messages": [
            {"role": "user", "content": full_message}
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

def run_sovereign_logic():
    print("\n🔮 STARTING PROJECT SOVEREIGN FULL CYCLE 🔮")
    print("==================================================")
    
    token = get_token(REAL_API_KEY)
    if not token:
        print("❌ Authentication failed.")
        return

    # ✅ UPDATED TOPIC: A safer, more efficient proposal that should get APPROVED
    topic = "Proposal: Use AI Agents to assist our human team with data entry only. Humans remain in full control."
    print(f"\n📝 TOPIC: {topic}\n")

    meeting_minutes = ""

    # 2. THE DEBATE (Phase 1)
    for agent in AGENTS:
        print(f"   ...Consulting {agent['name']}...")
        response = call_ai(token, agent["persona"], f"Analyze this proposal: '{topic}'")
        
        # Save the opinion
        formatted_response = f"[{agent['name']}]: {response.strip()}"
        meeting_minutes += formatted_response + "\n\n"
        
        print(f"\n👤 {agent['name']} OPINION:")
        print("-" * 30)
        print(response.strip()[:300] + "...") # Print preview to save space
        print("-" * 30)
        time.sleep(1)

    # 3. THE DECISION (Phase 2 - The CEO)
    print("\n👑 THE CEO IS DELIBERATING...")
    
    ceo_persona = "You are the CEO of Project Sovereign. You are decisive and bold. You listen to your advisors but make the final call."
    ceo_prompt = f"""
    Review the following opinions from your board:
    
    {meeting_minutes}
    
    Based on this feedback, make a final decision on the proposal: '{topic}'.
    Format your answer exactly like this:
    DECISION: [APPROVED / REJECTED]
    REASON: [One sentence summary]
    NEXT STEPS: [One bullet point on what to do next]
    """
    
    final_verdict = call_ai(token, ceo_persona, ceo_prompt)
    
    print("\n📢 FINAL EXECUTIVE DECREE:")
    print("==================================================")
    print(final_verdict)
    print("==================================================")

if __name__ == "__main__":
    run_sovereign_logic()