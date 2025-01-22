from flask import Flask, request, jsonify, render_template
import os
import openai

app = Flask(__name__)

# Fetch API key and Assistant ID from environment variables
API_KEY = os.getenv("OPENAI_API_KEY")  # Render stores this
ASSISTANT_ID = os.getenv("ASSISTANT_ID")  # Render stores this

# Set the OpenAI API key for OpenAI's library
openai.api_key = API_KEY

@app.route('/')
def home():
    """Serve the front-end HTML page."""
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    """
    Handle POST requests to process user messages,
    send them to the OpenAI API, and return the assistant's response.
    """
    user_message = request.json.get('message', '')  # Get the user's message from the request
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400  # Error if message is missing

    try:
        # Use OpenAI's ChatCompletion API to interact with the assistant
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Specify the GPT model
            messages=[
                {"role": "system", "content": f"You are an assistant configured with ID: {ASSISTANT_ID}."},
                {"role": "user", "content": user_message},  # User's message
            ]
        )

        # Extract the assistant's response from the API response
        assistant_message = response['choices'][0]['message']['content']
        return jsonify({'response': assistant_message})  # Send the response back to the front-end

    except Exception as e:
        # Catch and handle any errors (e.g., API key issues, OpenAI API errors)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # Default to port 5000 if PORT isn't set
    app.run(host='0.0.0.0', port=port)  # Run the app
