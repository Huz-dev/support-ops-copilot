from pathlib import Path
import json
from flask import Flask, render_template, request, jsonify
from pathlib import Path
from app.services.agent import SupportAgent
from app.services.support_chat_agent import (
    SupportChatAgent
)

support_agent = SupportChatAgent()
BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "ui" / "templates"),
    static_folder=str(BASE_DIR / "ui" / "static"),
)

chat_agent = SupportChatAgent()
agent = SupportAgent()
# Stores the ticket waiting for approval
pending_request = {}


@app.route("/")
def home():
    
    return render_template("index.html")

@app.route("/chat-page")
def chat_page():

    return render_template("chat.html")

@app.route("/sample-tickets")
def sample_tickets():

    with open(BASE_DIR / "data" / "sample_tickets.json", "r") as f:
        tickets = json.load(f)

    return jsonify(tickets)

@app.route("/analyze", methods=["POST"])
def analyze():

    global pending_request

    data = request.get_json()

    ticket = data.get("ticket", "").strip()

    if not ticket:
        return jsonify({"error": "Empty ticket"}), 400

    result = agent.process_ticket(ticket)

    if result.get("approval_required"):

        pending_request = result

        return jsonify({
            "approval_required": True,
            "tool": result["approval_tool"],
            "reason": result["approval_reason"]
        })

    return jsonify(result)


@app.route("/approve", methods=["POST"])
def approve():

    global pending_request

    if not pending_request:
        return jsonify({"error": "Nothing pending"}), 400

    result = agent.complete_after_approval(
        pending_request["ticket"],
        pending_request["plan"],
        pending_request["classification"],
        pending_request["extraction"],
    )
    print(result)
    pending_request = {}

    return jsonify(result)


@app.route("/reject", methods=["POST"])
def reject():

    global pending_request

    pending_request = {}

    return jsonify({
        "approved": False,
        "message": "Request rejected."
    })


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data["message"]

    agent.memory.add(
        "user",
        message
    )

    reply = agent.ai.chat(
        message,
        agent.memory.history()
    )

    agent.memory.add(
        "assistant",
        reply
    )

    return jsonify({
        "reply": reply
    })

@app.route("/logs")
def logs():

    sessions = []

    tools = []

    session_path = Path(
        "logs/sessions"
    )

    if session_path.exists():

        for file in session_path.glob(
            "*.json"
        ):

            with open(file, "r") as f:
                sessions.append(
                    json.load(f)
                )

    tool_path = Path(
        "logs/tool_calls.log"
    )

    if tool_path.exists():

        tools.append(
            tool_path.read_text()
        )

    return render_template(
        "logs.html",
        sessions=sessions[::-1],
        tools=tools
    )




@app.route("/support-chat")
def support_chat():
    return render_template(
        "support_chat.html"
    )


@app.route(
    "/support-agent-chat",
    methods=["POST"]
)
def support_agent_chat():

    data = request.json

    message = data["message"]

    reply = chat_agent.reply(
        message
    )

    return {
        "reply": reply
    }


if __name__ == "__main__":
    app.run(debug=True)

