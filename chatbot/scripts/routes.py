from flask import request, jsonify, Response
import uuid

def generate_session_id() -> str:
    """Generate a unique session ID."""
    return str(uuid.uuid4())


def setup_routes(app, chatbot):
    @app.route("/ai-stream", methods=["POST"])
    def stream_chat():
        data = request.json
        prompt = data.get("prompt")
        session_id = data.get("session_id")

        chatbot.logger.info(
            f"Received stream request. Prompt: {prompt[:50]}..., Session ID: {session_id}"
        )

        def generate():
            try:
                for chunk in chatbot.process_prompt(prompt, session_id):
                    yield chunk
            except Exception as e:
                chatbot.logger.error(f"An error occurred in stream_chat: {str(e)}")
                import traceback

                traceback.print_exc()
                yield f"event: stream-error\ndata: {str(e)}\n\n"

        return Response(generate(), content_type="text/event-stream")

    @app.route("/initialize-ai-chat", methods=["POST"])
    def initialize_chat():
        data = request.json
        request_session_id = data.get("session_id")

        chatbot.logger.info(
            f"Received initialize request. Session ID: {request_session_id}"
        )

        if not request_session_id:
            session_id = generate_session_id()
        else:
            session_id = request_session_id
            chatbot.logger.info(
                f"Session ID already exists. Using existing session ID: {session_id}"
            )

        return jsonify({"status": "initialized", "session_id": session_id})

    @app.route("/chatbot-status")
    def chatbot_status():
        return jsonify({"message": "Chatbot is running"})
