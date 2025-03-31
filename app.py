from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS
import os

app = Flask(__name__, template_folder="templates", static_folder="static")  
CORS(app)

# Ensure API key is loaded
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    print("⚠️ Warning: DEEPSEEK_API_KEY is not set! Please configure it in Render.")

@app.route("/")
def home():
    return render_template("pg11.html")  # Ensure 'pg11.html' exists in 'templates' folder

@app.route("/ask_deepseek", methods=["GET"])
def ask_deepseek():
    user_query = request.args.get("query")

    if not DEEPSEEK_API_KEY:
        return jsonify({"error": "Missing API Key"}), 401
    
    if not user_query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Choose the correct API endpoint (DeepSeek OR OpenRouter)
    url = "https://openrouter.ai/api/v1/chat/completions"  # ✅ Correct DeepSeek API endpoint
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek/deepseek-chat-v3-0324:free",  # ✅ Use the correct model name (deepseek-chat)
        "messages": [{"role": "user", "content": user_query}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()

        if response.status_code == 200:
            return jsonify(response_json)
        elif response.status_code == 401:
            return jsonify({"error": "Unauthorized - Invalid API Key"}), 401
        else:
            return jsonify({"error": "DeepSeek API Error", "details": response_json}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to reach DeepSeek API", "details": str(e)}), 500
    except ValueError:
        return jsonify({"error": "Invalid JSON response from DeepSeek API"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
