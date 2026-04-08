import os
from openai import OpenAI

# ── ENV VARIABLES (REQUIRED) ─────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")  # keep as is (no default)

# ── OPENAI CLIENT ───────────────────────────────────
client = OpenAI(
    base_url=API_BASE_URL,
    api_key="sk-123456"  # dummy key (for now)
)

# ── MAIN FUNCTION ───────────────────────────────────
def run_agent(input_data):
    print("START")   # required log

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this system threat and decide BLOCK or ALLOW:\n{input_data}"
                }
            ]
        )

        print("STEP")   # required log

        output = response.choices[0].message.content

        print("END")    # required log

        return output

    except Exception as e:
        print("ERROR:", str(e))
        print("END")
        return "ERROR"


# ── TEST RUN (IMPORTANT) ────────────────────────────
if __name__ == "__main__":
    test_input = "CPU usage 95%, possible ransomware activity"
    result = run_agent(test_input)
    print("RESULT:", result)