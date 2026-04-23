from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Debug: print the key so we can see if it loaded
api_key = os.getenv("GROQ_API_KEY")
print("API KEY LOADED:", api_key)

client = Groq(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        system_prompt = data.get("system_prompt", "You are a helpful IT tutor.")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_message}
            ]
        )

        return jsonify({"reply": response.choices[0].message.content})

    except Exception as e:
        print("FULL ERROR:", str(e))
        return jsonify({"reply": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)