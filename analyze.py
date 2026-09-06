import os
import requests
from google import genai

# Config keys from secure environment variables
FOOTBALL_API_KEY = os.environ.get("FOOTBALL_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def fetch_todays_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("matches", [])
    print("API Error:", response.status_code, response.text)
    return []

def analyze_matches_with_ai(match_data_string):
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    You are a brutally honest, data-driven football betting analyst. 
    Analyze these upcoming matches:
    {match_data_string}
    
    Calculate the implied probabilities, filter for matches with actual analytical interest, and provide a cynical, sharp critique of where the bookies might be wrong or where traps lie. Keep it concise.
    """
    
    # Using the free, fast Gemini Flash model
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text

if __name__ == "__main__":
    matches = fetch_todays_matches()
    if matches:
        match_summary = "\n".join([f"- {m['homeTeam']['name']} vs {m['awayTeam']['name']} on {m['utcDate']}" for m in matches[:15]])
        analysis = analyze_matches_with_ai(match_summary)
        print("--- AI BETTING ANALYSIS ---")
        print(analysis)
    else:
        print("No matches found or failed to fetch data.")
