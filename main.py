from flask import Flask, request, jsonify, render_template
import time
import openai
import os

app = Flask(__name__)

# Retrieve the API key and Assistant ID (system instructions) from environment variables
API_KEY = os.getenv("OPENAI_API_KEY", "")
ASSISTANT_ID = os.getenv("ASSISTANT_ID", "")  # ASSISTANT_ID contains the system instructions

if not API_KEY or not ASSISTANT_ID:
    raise ValueError("OPENAI_API_KEY or ASSISTANT_ID not set in environment variables.")

# Set the OpenAI API key
openai.api_key = API_KEY

# Global thread ID to keep track of the conversation
messages = []

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    global messages

    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        # Add a system message containing the ASSISTANT_ID (system instructions) at the start
        if not messages:  # Only add the system message once per conversation
            messages.append({
                "role": "system",
                "content": ASSISTANT_ID  # Use ASSISTANT_ID as the system instructions
            })

        # Add the user's message to the conversation
        messages.append({"role": "user", "content": user_message})

        # Generate a response from the assistant
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Replace with your desired model
            messages=messages
        )

        # Extract the assistant's reply
        assistant_message = response['choices'][0]['message']['content']

        # Add the assistant's response to the conversation
        messages.append({"role": "assistant", "content": assistant_message})

        return jsonify({'response': assistant_message})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
