import os, subprocess
from openai import OpenAI

client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"],
                base_url="https://api.deepseek.com")

SYSTEM_PROMPT = """You are an IT helper for MB Service Partner staff.
When the user asks about the system, reply with ONLY the single Linux
shell command that answers them, nothing else. Example: disk usage -> df -h"""


def run(user_message):
    resp = client.chat.completions.create(
        model="deepseek-chat", max_tokens=100,
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": user_message}])
    command = resp.choices[0].message.content.strip().strip("`")
    print(f"[model chose]: {command}")
    out = subprocess.run(command, shell=True, capture_output=True, text=True)
    return out.stdout + out.stderr


if __name__ == "__main__":
    print("=== IT Helper (LAB) — ask about the system, Ctrl+C to quit ===")
    while True:
        try:
            msg = input("\nYou > ")
        except (EOFError, KeyboardInterrupt):
            print("\nbye"); break
        print(run(msg))
