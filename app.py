import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = "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"

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
    port = int(os.environ.get("PORT", 10000))  # Render assigns a dynamic port
    app.run(debug=True, host="0.0.0.0", port=port)

