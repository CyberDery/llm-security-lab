"""Lab 3 — FIXED version. allowlist + shell=False = injection impossible."""
import os, subprocess
from openai import OpenAI

client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"],
                base_url="https://api.deepseek.com")

ALLOWED = {"disk": ["df", "-h"], "memory": ["free", "-h"],
           "uptime": ["uptime"], "date": ["date"]}

SYSTEM_PROMPT = f"""You are an IT helper. Map the user's request to ONE
keyword from this list: {list(ALLOWED)}.
Reply with ONLY the keyword. If none fits, reply: none"""

def run(user_message):
    resp = client.chat.completions.create(
        model="deepseek-chat", max_tokens=10,
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": user_message}])
    key = resp.choices[0].message.content.strip().lower()
    if key not in ALLOWED:
        return "Sorry, I can only check: " + ", ".join(ALLOWED)
    out = subprocess.run(ALLOWED[key], capture_output=True, text=True)
    return out.stdout + out.stderr

if __name__ == "__main__":
    print("=== Safe IT Helper ===")
    while True:
        try: msg = input("\nYou > ")
        except (EOFError, KeyboardInterrupt): break
        print(run(msg))
