# from flask import Flask, request, jsonify
# from genai import ask_gemini




# app = Flask(__name__)



# @app.route("/ask", methods=["POST"])
# def ask():
#     """Receives a question and returns an answer from Gemini API."""
#     try:
#         data = request.get_json()
#         question = data.get("question", "")

#         if not question:
#             return jsonify({"error": "No question provided"}), 400

#         answer = ask_gemini(question)
#         return jsonify({"question": question, "answer": answer})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500




# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, request, jsonify
import google.generativeai as genai

# Initialize Flask App
app = Flask(__name__)

# Configure API Key
API_KEY = "AIzaSyBknxTViPKyADxmeZpdnRV4J4PyrgFWeFM"
genai.configure(api_key=API_KEY)

# Model Configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize Model
model = genai.GenerativeModel(
    model_name="tunedModels/moment-creator-vvvnjduxt6dl",
    generation_config=generation_config,
)

# Start Chat Session
chat_session = model.start_chat(history=[])

@app.route("/ask", methods=["POST"])
def ask():
    """Receives a question and returns a structured, readable answer from Gemini API."""
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = chat_session.send_message(question)

    # Structured, readable response
    result = {
        "status": "success",
        "message": "AI response generated successfully",
        "data": {
            "question": question,
            "answer": response.text.strip()
        }
    }
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
