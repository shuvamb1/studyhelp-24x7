from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS
import os

app = Flask(__name__, template_folder="templates", static_folder="static")  # Ensure 'templates' folder exists
CORS(app)

DEEPSEEK_API_KEY = "my_api_key"

@app.route("/")
def home():
    return render_template("pg11.html")  # Ensure 'pg11.html' is inside the 'templates' folder

@app.route("/ask_deepseek", methods=["GET"])
def ask_deepseek():
    user_query = request.args.get("query")
    if not user_query:
        return jsonify({"error": "Query parameter is required"}), 400

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [{"role": "user", "content": user_query}]
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        response_json = response.json()
        if response.status_code == 200:
            return jsonify(response_json)
        else:
            return jsonify({"error": "DeepSeek API Error", "details": response_json}), response.status_code
    except Exception as e:
        return jsonify({"error": "Failed to parse JSON response", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
