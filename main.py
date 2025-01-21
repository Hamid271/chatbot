from flask import Flask, request, jsonify, render_template
import os
import time
import openai  # Correct import

app = Flask(__name__)

# Fetch API key and Assistant ID from environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Set the OpenAI API key
openai.api_key = API_KEY

# Global thread ID to keep track of the conversation
THREAD_ID = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    global THREAD_ID

    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        # Create a new thread if none exists
        if not THREAD_ID:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Adjust the model name as needed
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            THREAD_ID = response['id']  # Save the thread ID
        else:
            # Add the user message to the existing thread
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Adjust the model name as needed
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

        # Get the assistant's response
        assistant_message = response['choices'][0]['message']['content']

        return jsonify({'response': assistant_message})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
