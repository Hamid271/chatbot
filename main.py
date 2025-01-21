from flask import Flask, request, jsonify, render_template
import os
import time
from openai import OpenAI

app = Flask(__name__)

# Fetch API key and Assistant ID from environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

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
        # Create a new thread if none exists
        if not THREAD_ID:
            thread = client.beta.threads.create(
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            THREAD_ID = thread.id
        else:
            # Add the user message to the existing thread
            client.beta.threads.messages.create(
                thread_id=THREAD_ID,
                role="user",
                content=user_message
            )

        # Submit a run to the assistant
        run = client.beta.threads.runs.create(thread_id=THREAD_ID, assistant_id=ASSISTANT_ID)

        # Wait for the run to complete
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=THREAD_ID, run_id=run.id)
            time.sleep(1)

        # Get the assistant's response
        message_response = client.beta.threads.messages.list(thread_id=THREAD_ID)
        latest_message = message_response.data[0].content[0].text.value

        return jsonify({'response': latest_message})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
