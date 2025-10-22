# app/routes/ai_agent_route.py
from flask import Blueprint, request, jsonify
from controllers.ai_controller import ai_agent_chat

ai_agent_bp = Blueprint("ai_agent", __name__)

@ai_agent_bp.route("/api/ai/agent", methods=["POST"])
def ai_agent():
    """
    Handle AI assistant requests.
    Expects JSON: { "prompt": "your question or instruction" }
    """
    data = request.get_json(force=True) or {}
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Missing 'prompt'"}), 400

    try:
        reply = ai_agent_chat(prompt)
        return jsonify({"reply": reply}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
