from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load chat pairs from text
def load_conversations():
    path = "data/my_chats.txt"
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    conversations = {}
    for i in range(0, len(lines)-1, 2):
        user_input = lines[i].strip().lower()
        twin_response = lines[i+1].strip()
        conversations[user_input] = twin_response
    return conversations

chat_pairs = load_conversations()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/start')
def start_chat():
    session['chat_history'] = []
    return redirect(url_for('chat'))

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        user_msg = request.form['user_input']
        session['chat_history'].append(("user", user_msg))

        reply = chat_pairs.get(user_msg.lower(), "😄")
        session['chat_history'].append(("bot", reply))
        session.modified = True

    return render_template("chat.html", chat_history=session['chat_history'])

if __name__ == '__main__':
    app.run(debug=True)