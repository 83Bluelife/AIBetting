import os
import requests
import anthropic

# 1. Config keys from secure environment variables
FOOTBALL_API_KEY = os.environ.get("FOOTBALL_API_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def fetch_todays_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("matches", [])
    return []

def ask_claude_to_critique(match_data_string):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    prompt = f"""
    You are a brutally honest, data-driven football betting analyst. 
    Analyze these upcoming matches:
    {match_data_string}
    
    Calculate the implied probabilities, filter for matches with actual analytical interest, and provide a cynical, sharp critique of where the bookies might be wrong or where traps lie. Keep it concise.
    """
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def send_telegram_notification(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    matches = fetch_todays_matches()
    if matches:
        # Simplify match formatting for Claude
        match_summary = "\n".join([f"- {m['homeTeam']['name']} vs {m['awayTeam']['name']} on {m['utcDate']}" for m in matches[:15]])
        
        # Get Claude's brutal analysis
        analysis = ask_claude_to_critique(match_summary)
        
        # Send directly to your phone via Telegram
        send_telegram_notification(analysis)
