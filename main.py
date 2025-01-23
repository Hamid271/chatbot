from flask import Flask, request, jsonify, render_template
import time
import openai
import os

app = Flask(__name__)

# Retrieve the API key and Assistant ID from environment variables
API_KEY = os.getenv("OPENAI_API_KEY", "")
ASSISTANT_ID = os.getenv("ASSISTANT_ID", "")

if not API_KEY or not ASSISTANT_ID:
    raise ValueError("OPENAI_API_KEY or ASSISTANT_ID not set in environment variables.")

# Set the OpenAI API key
openai.api_key = API_KEY

# Global thread ID to keep track of the conversation
THREAD_ID = None

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    global THREAD_ID

    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        # If THREAD_ID doesn't exist, start a new "conversation" by including the first message
        if not THREAD_ID:
            messages = [{"role": "user", "content": user_message}]
        else:
            # Continue the conversation by adding the new user message
            messages.append({"role": "user", "content": user_message})

        # Generate a response using the ChatCompletion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use OpenAI's chat model
            messages=messages
        )

        # Extract the assistant's reply
        assistant_message = response['choices'][0]['message']['content']

        return jsonify({'response': assistant_message})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
