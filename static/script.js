document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');

    // Function to add a message to the chat box
    const addMessage = (text, sender) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.textContent = text;
        chatBox.appendChild(messageElement);
        // Scroll to the bottom
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    // Function to send a message to the backend
    const sendMessage = async (message) => {
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });
            const data = await response.json();
            if (data.responses) {
                data.responses.forEach(responseMsg => {
                    addMessage(responseMsg, 'tutor');
                });
            }
        } catch (error) {
            console.error('Error sending message:', error);
            addMessage('Sorry, something went wrong. Please try again.', 'tutor');
        }
    };

    // Handle form submission
    chatForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, 'user');
            sendMessage(message);
            userInput.value = '';
        }
    });

    // Fetch the welcome message when the page loads
    const fetchWelcomeMessage = async () => {
        try {
            const response = await fetch('/welcome');
            const data = await response.json();
            if (data.responses) {
                data.responses.forEach(responseMsg => {
                    addMessage(responseMsg, 'tutor');
                });
            }
        } catch (error) {
            console.error('Error fetching welcome message:', error);
            addMessage('Welcome! How can I help you today?', 'tutor');
        }
    };

    fetchWelcomeMessage();
});
