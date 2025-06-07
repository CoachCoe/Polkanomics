document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const clearButton = document.getElementById('clear-chat');

    // Function to add a message to the chat
    function addMessage(content, type = 'bot') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to send a message to the API
    async function sendMessage(message) {
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            addMessage(data.response);
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your request. Please try again.', 'system');
        }
    }

    // Function to clear chat history
    async function clearChat() {
        try {
            const response = await fetch('/clear', {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            // Clear the chat messages container
            chatMessages.innerHTML = '';
            // Add the welcome message back
            addMessage('Welcome! I\'m your economics expert assistant. Ask me anything about economics, game theory, or Polkadot tokenomics.', 'system');
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, there was an error clearing the chat history.', 'system');
        }
    }

    // Event listener for send button
    sendButton.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, 'user');
            sendMessage(message);
            userInput.value = '';
        }
    });

    // Event listener for Enter key
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendButton.click();
        }
    });

    // Event listener for clear button
    clearButton.addEventListener('click', clearChat);

    // Auto-resize textarea
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = userInput.scrollHeight + 'px';
    });
}); 