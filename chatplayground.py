from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS  # ✅ Add this import
from langchain_groq import ChatGroq
import os
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS on all routes

# Initialize the Groq client once
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # api_key=os.getenv("GROQ_API_KEY")  # Use if authentication is needed
)

# GET route with a predefined prompt
@app.route("/generate", methods=["GET"])
def generate():
    try:
        prompt = request.args.get("prompt", "What is Google?")
        response = llm.invoke(prompt)
        return jsonify({
            "prompt": prompt,
            "response": str(response)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# POST route that accepts user prompt and returns Groq response
@app.route("/generate", methods=["POST"])
def generate_from_input():
    try:
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Missing 'prompt' in request body"}), 400

        prompt = data["prompt"]
        response = llm.invoke(prompt)
        onlycontent = response.model_dump_json()
        jsonfor = json.loads(onlycontent)
        print(jsonfor['content'])
        return jsonify({
            "prompt": prompt,
            "response": str(jsonfor['content'])
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8000, debug=True)
