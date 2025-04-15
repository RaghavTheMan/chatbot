from flask import Flask, request, jsonify, render_template_string
import random
app = Flask(__name__)
qa_pairs = {
    "hello": ["Hi there!", "Hello! How can I assist you?", "Hey! Need help?"],
    "bye": ["Goodbye!", "See you later!", "Take care!"],
    "help": ["Sure, ask me anything!", "I'm here to assist you.", "Let me know what you need help with."],
    "how are you": ["I'm a bot, but I'm doing great!", "All systems operational!", "Feeling helpful today!"],
    "what is your name": ["I'm ChatBot 1.0!", "They call me FlaskBot.", "Just your friendly assistant."]
}
# Basic chatbot logic
def get_bot_response(message):
    message = message.lower()

    # Check for exact or partial match in keys
    for key in qa_pairs:
        if key in message:
            return random.choice(qa_pairs[key])

    return "I'm not sure how to respond to that. Try asking something else!"

# Serve the chatbot page
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Chatbot</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            #chatbox { width: 100%; height: 300px; border: 1px solid #ccc; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
            .user { color: blue; }
            .bot { color: green; }
        </style>
    </head>
    <body>
        <h2>Chat with Bot</h2>
        <div id="chatbox"></div>
        <input type="text" id="message" placeholder="Type your message..." style="width: 80%;">
        <button onclick="sendMessage()">Send</button>

        <script>
            function sendMessage() {
                const msg = document.getElementById("message").value;
                if (msg.trim() === "") return;

                const chatbox = document.getElementById("chatbox");
                chatbox.innerHTML += "<div class='user'><b>You:</b> " + msg + "</div>";

                fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: msg })
                })
                .then(res => res.json())
                .then(data => {
                    chatbox.innerHTML += "<div class='bot'><b>Bot:</b> " + data.response + "</div>";
                    chatbox.scrollTop = chatbox.scrollHeight;
                    document.getElementById("message").value = "";
                });
            }
        </script>
    </body>
    </html>
    ''')

# Chat API
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    bot_response = get_bot_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8088)
