# # from flask import Flask, request, jsonify
# # from genai import ask_gemini




# # app = Flask(__name__)



# # @app.route("/ask", methods=["POST"])
# # def ask():
# #     """Receives a question and returns an answer from Gemini API."""
# #     try:
# #         data = request.get_json()
# #         question = data.get("question", "")

# #         if not question:
# #             return jsonify({"error": "No question provided"}), 400

# #         answer = ask_gemini(question)
# #         return jsonify({"question": question, "answer": answer})

# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500




# # if __name__ == "__main__":
# #     app.run(host="0.0.0.0", port=5000, debug=True)

# from flask import Flask, request, jsonify
# import google.generativeai as genai

# from flask_cors import CORS


# # Initialize Flask App
# app = Flask(__name__)
# CORS(app)

# # Configure API Key
# API_KEY = "AIzaSyBknxTViPKyADxmeZpdnRV4J4PyrgFWeFM"
# genai.configure(api_key=API_KEY)

# # Model Configuration
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 40,
#     "max_output_tokens": 8192,
#     "response_mime_type": "text/plain",
# }

# # Initialize Model
# model = genai.GenerativeModel(
#     model_name="tunedModels/moment-creator-vvvnjduxt6dl",
#     generation_config=generation_config,
# )

# # Start Chat Session
# chat_session = model.start_chat(history=[])

# @app.route("/ask", methods=["POST"])
# def ask():
#     """Receives a question and returns a structured, readable answer from Gemini API."""
#     data = request.get_json()
#     question = data.get("question", "").strip()

#     if not question:
#         return jsonify({"error": "No question provided"}), 400

#     response = chat_session.send_message(question)

#     # Structured, readable response
#     result = {
#         "status": "success",
#         "message": "AI response generated successfully",
#         "data": {
#             "question": question,
#             "answer": response.text.strip()
#         }
#     }
#     return jsonify(result), 200

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)



from flask import Flask, request, jsonify
import google.generativeai as genai
import re
import urllib.parse

# Initialize Flask App
app = Flask(__name__)

# Configure Gemini API Key
API_KEY = "AIzaSyBknxTViPKyADxmeZpdnRV4J4PyrgFWeFM"  # Replace with your actual API key
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
    model_name="tunedModels/moment-creator-vvvnjduxt6dl",  # Replace with your actual model name
    generation_config=generation_config,
)

# Start Chat Session
chat_session = model.start_chat(history=[])


# -------- Location Handling Functions -------- #

# def extract_locations(text):
#     """Extract location names from AI-generated text using keyword matching."""
#     locations = []
#     lines = text.split("\n")
#     for line in lines:
#         clean_line = line.strip("-• ").strip()
#         if clean_line and any(keyword in clean_line.lower() for keyword in [
#             "lake", "viewpoint", "falls", "temple", "museum", "fort",
#             "beach", "garden", "hill", "dam", "point", "park", "zoo"
#         ]):
#             locations.append(clean_line)
#     return locations


# def get_location_image_url(location_name):
#     """Generate a Google Image Search URL for a location."""
#     query = urllib.parse.quote_plus(location_name)
#     return f"https://www.google.com/search?tbm=isch&q={query}"


# def generate_location_data(text):
#     """Create a list of location objects with map and image URLs."""
#     locations = extract_locations(text)
#     location_data = []
#     for loc in locations:
#         encoded = urllib.parse.quote_plus(loc)
#         location_data.append({
#             "name": loc,
#             "map_link": f"https://www.google.com/maps/search/{encoded}",
#             "image_url": get_location_image_url(loc)
#         })
#     return location_data


# # -------- Flask Route -------- #

# @app.route("/ask", methods=["POST"])
# def ask():
#     """Receives a question and returns AI-generated answer with location map and image links."""
#     data = request.get_json()
#     question = data.get("question", "").strip()

#     if not question:
#         return jsonify({"error": "No question provided"}), 400

#     try:
#         response = chat_session.send_message(question)
#         raw_text = response.text.strip()
#         locations = generate_location_data(raw_text)

#         result = {
#             "status": "success",
#             "message": "AI response generated successfully",
#             "data": {
#                 "question": question,
#                 "answer": raw_text,
#                 "locations": locations
#             }
#         }
#         return jsonify(result), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # -------- App Runner -------- #

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)


# -------- Detect Language -------- #
import langdetect
import requests

def detect_language(text):
    try:
        return langdetect.detect(text)
    except:
        return "en"  # fallback default

# -------- Location Extraction -------- #
def extract_locations(text):
    locations = []
    lines = text.split("\n")
    for line in lines:
        clean = line.strip("-• ").strip()
        if clean and any(w in clean.lower() for w in [
            "lake", "viewpoint", "falls", "temple", "museum", "fort",
            "beach", "garden", "hill", "dam", "point", "park", "zoo"
        ]):
            locations.append(clean)
    return locations

# -------- Image Fetching -------- #
def get_unsplash_image(location_name):
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": location_name,
        "client_id": "S7v7DH6VEMQwDJDpQDwpINrlILxme2zsi4jia94dAzg",
        "per_page": 1
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("results"):
            return data["results"][0]["urls"]["regular"]
    except Exception as e:
        print(f"Image fetch error: {e}")
    return None

# -------- Location Data Generator -------- #
def generate_location_data(text):
    locations = extract_locations(text)
    location_data = []
    for loc in locations:
        encoded = urllib.parse.quote_plus(loc)
        map_link = f"https://www.google.com/maps/search/{encoded}"
        image_url = get_unsplash_image(loc)
        location_data.append({
            "name": loc,
            "map_link": map_link,
            "image_url": image_url or "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"
        })
    return location_data

# -------- Main Route -------- #
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        # Detect input language
        input_lang = detect_language(question)

        # Ask Gemini in original language
        response = chat_session.send_message(question)
        raw_text = response.text.strip()

        # Extract location data from response
        locations = generate_location_data(raw_text)

        result = {
            "status": "success",
            "message": "AI response generated successfully",
            "language": input_lang,
            "data": {
                "question": question,
                "answer": raw_text,
                "locations": locations
            }
        }
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------- Run App -------- #
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
