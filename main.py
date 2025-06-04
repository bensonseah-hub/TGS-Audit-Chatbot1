from flask import Flask, request, jsonify, send_file
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()

    if not user_input or len(user_input) > 500:
        return jsonify({"error": "Invalid input"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an audit assistant helping staff with MFRS, MPERS, ISA and firm policy."},
                {"role": "user", "content": user_input}
            ]
        )
        return jsonify({"reply": response.choices[0].message["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
