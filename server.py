from flask import Flask, request, jsonify
from genai import ask_gemini
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/ask", methods=["POST"])
def ask():
    """Receives a question and returns an answer from Gemini API."""
    try:
        data = request.get_json()
        question = data.get("question", "")

        if not question:
            return jsonify({"error": "No question provided"}), 400

        answer = ask_gemini(question)
        return jsonify({"question": question, "answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
