from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import Flask-CORS
import os
import openai

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Fetch API key and Assistant ID from environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Set OpenAI API key
openai.api_key = API_KEY

@app.route('/')
def home():
    """Serve the front-end HTML page."""
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    """Process user messages and return assistant responses."""
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        # Use OpenAI's ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are an assistant configured with ID {ASSISTANT_ID}."},
                {"role": "user", "content": user_message},
            ]
        )
        assistant_message = response['choices'][0]['message']['content']
        return jsonify({'response': assistant_message})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
