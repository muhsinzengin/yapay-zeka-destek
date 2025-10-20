// Chat Widget JavaScript
// Handles communication with Rasa server

class ChatWidget {
    constructor() {
        this.socket = null;
        this.userId = this.generateUserId();
        this.rasaUrl = 'http://localhost:5005';
        
        this.initializeElements();
        this.attachEventListeners();
        this.connectToRasa();
    }

    initializeElements() {
        this.chatWidget = document.getElementById('chatWidget');
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.minimizeBtn = document.getElementById('minimizeBtn');
        this.chatToggle = document.getElementById('chatToggle');
    }

    attachEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        this.minimizeBtn.addEventListener('click', () => this.toggleChat());
        this.chatToggle.addEventListener('click', () => this.toggleChat());
    }

    generateUserId() {
        let userId = localStorage.getItem('chatUserId');
        if (!userId) {
            userId = 'user_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('chatUserId', userId);
        }
        return userId;
    }

    toggleChat() {
        this.chatWidget.classList.toggle('minimized');
        this.chatToggle.classList.toggle('visible');
    }

    async connectToRasa() {
        // Initialize connection with Rasa
        console.log('Connecting to Rasa server...');
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;

        // Display user message
        this.addMessage(message, 'user');
        this.messageInput.value = '';

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Send message to Rasa
            const response = await fetch(`${this.rasaUrl}/webhooks/rest/webhook`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    sender: this.userId,
                    message: message
                })
            });

            const data = await response.json();

            // Remove typing indicator
            this.removeTypingIndicator();

            // Display bot responses
            if (data && data.length > 0) {
                data.forEach(msg => {
                    if (msg.text) {
                        this.addMessage(msg.text, 'bot');
                    }
                    if (msg.image) {
                        this.addImage(msg.image);
                    }
                });
            } else {
                this.addMessage('Üzgünüm, bir yanıt alamadım.', 'bot');
            }

        } catch (error) {
            console.error('Error sending message:', error);
            this.removeTypingIndicator();
            this.addMessage('Bağlantı hatası. Lütfen daha sonra tekrar deneyin.', 'bot');
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = text;
        
        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    addImage(imageUrl) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        
        const img = document.createElement('img');
        img.src = imageUrl;
        img.style.maxWidth = '100%';
        img.style.borderRadius = '8px';
        
        messageDiv.appendChild(img);
        this.chatMessages.appendChild(messageDiv);
        
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-message';
        typingDiv.innerHTML = `
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        this.chatMessages.appendChild(typingDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    removeTypingIndicator() {
        const typingMsg = this.chatMessages.querySelector('.typing-message');
        if (typingMsg) {
            typingMsg.remove();
        }
    }
}

// Initialize chat widget when page loads
document.addEventListener('DOMContentLoaded', () => {
    new ChatWidget();
});
