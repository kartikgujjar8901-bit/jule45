from flask import Flask, render_template, request, jsonify, session
import tutor

app = Flask(__name__)
# A secret key is needed to use sessions. In a real app, this should be a secure, secret value.
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    """
    Renders the main chat page.
    Initializes the session state if it's a new user.
    """
    if 'tutor_state' not in session:
        session['tutor_state'] = tutor.get_initial_state()
        # The welcome message is handled by the frontend now
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles chat messages from the user.
    """
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    # Ensure session state exists
    if 'tutor_state' not in session:
        session['tutor_state'] = tutor.get_initial_state()

    tutor_state = session['tutor_state']

    # Process the message
    responses, updated_state = tutor.process_message(user_input, tutor_state)

    # Save the updated state back to the session
    session['tutor_state'] = updated_state

    return jsonify({'responses': responses})

@app.route('/welcome', methods=['GET'])
def welcome():
    """
    Provides the initial welcome message for a new chat session.
    """
    # We don't need to reset the state here, just get the welcome text
    welcome_messages = tutor.get_welcome_message()
    return jsonify({'responses': welcome_messages})


if __name__ == '__main__':
    # This is for local development testing.
    # In production, a proper WSGI server like Gunicorn would be used.
    app.run(debug=True, port=5001)
