from flask import Flask, request, jsonify, render_template
import os
import openai

app = Flask(__name__)

# Fetch API key from environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not found in environment variables")

# Set the OpenAI API key
openai.api_key = API_KEY

# Conversation history stored in memory
conversation_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    global conversation_history

    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        # Add the user's message to the conversation history
        conversation_history.append({"role": "user", "content": user_message})

        # Send the conversation history to the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Adjust the model if needed
            messages=conversation_history
        )

        # Get the assistant's response
        assistant_message = response['choices'][0]['message']['content']

        # Add the assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": assistant_message})

        return jsonify({'response': assistant_message})

    except openai.error.OpenAIError as e:
        return jsonify({'error': 'OpenAI API error', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
