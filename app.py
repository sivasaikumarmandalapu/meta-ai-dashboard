from inference import run_agent
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import psutil
import random
import os

app = Flask(__name__)
CORS(app)

# ── STATE ─────────────────────────
current_threats = []
blocked_count = 0

THREATS = [
    "SQL Injection",
    "DDoS Attack",
    "Ransomware",
    "Brute Force",
    "Unauthorized Access"
]

# ── SYSTEM STATE ─────────────────
def get_state():
    return {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "blocked": blocked_count
    }

# ── AUTO DECISION (AI CONNECTED) ─
def auto_decision(state):
    input_data = f"CPU: {state['cpu']}%, Memory: {state['memory']}%"

    try:
        ai_response = run_agent(input_data)

        if "BLOCK" in ai_response.upper():
            return "BLOCK"
        else:
            return "ALLOW"

    except:
        # 🔥 fallback if AI fails
        if state["cpu"] > 80 or state["memory"] > 85:
            return "BLOCK"
        return "ALLOW"

# ── STEP FUNCTION ────────────────
def step(action):
    global blocked_count

    if not current_threats:
        return {"msg": "No threats", "state": get_state()}

    threat = current_threats.pop(0)

    if action == "BLOCK":
        blocked_count += 1
        decision = "BLOCKED"
    else:
        decision = "ALLOWED"

    return {
        "threat": threat,
        "decision": decision,
        "state": get_state()
    }

# ── ROUTES ──────────────────────

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api/state')
def state():
    return jsonify(get_state())

# 🔥 REQUIRED FOR OPENENV CHECK
@app.route('/reset', methods=['POST'])
def reset():
    global current_threats, blocked_count

    current_threats = []
    blocked_count = 0

    return jsonify({
        "status": "reset successful",
        "state": {
            "cpu": 0,
            "memory": 0,
            "blocked": blocked_count
        }
    })

# OPTIONAL (for your UI)
@app.route('/api/reset', methods=['POST'])
def reset_api():
    return reset()

@app.route('/api/threat')
def threat():
    threat = random.choice(THREATS)
    current_threats.append(threat)

    state = get_state()
    action = auto_decision(state)
    result = step(action)

    return jsonify({
        "threat": threat,
        "decision": result["decision"],
        "state": result["state"]
    })

# ── RUN (IMPORTANT FOR HUGGING FACE) ─
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
