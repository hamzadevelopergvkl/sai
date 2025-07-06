from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "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"
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.form['message']
    model = request.form['model']
    hidden_prompt = request.form.get('system', '')

    if not user_msg.strip():
        return jsonify({'reply': '⚠️ Please type a message.'})

    payload_messages = []
    if hidden_prompt:
        payload_messages.append({"role": "system", "content": hidden_prompt})
    payload_messages.extend(chat_history)
    payload_messages.append({"role": "user", "content": user_msg})

    payload = {
        "model": model,
        "messages": payload_messages,
        "max_tokens": 512,
        "temperature": 0.7
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        res_json = res.json()
        ai_reply = res_json['choices'][0]['message']['content']
        chat_history.append({"role": "user", "content": user_msg})
        chat_history.append({"role": "assistant", "content": ai_reply})
        return jsonify({'reply': ai_reply})
    except Exception as e:
        return jsonify({'reply': f"Error: {str(e)}"})
