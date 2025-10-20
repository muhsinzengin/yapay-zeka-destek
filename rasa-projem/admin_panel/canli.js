// Live Chat Monitoring JavaScript
// Displays active conversations and allows admin intervention

class LiveChatMonitor {
    constructor() {
        this.apiUrl = 'http://localhost:5000/api';
        this.selectedUserId = null;
        this.conversations = [];
        
        this.initializeElements();
        this.attachEventListeners();
        this.loadConversations();
        
        // Refresh every 5 seconds
        setInterval(() => this.loadConversations(), 5000);
    }

    initializeElements() {
        this.conversationList = document.getElementById('conversationList');
        this.noSelection = document.getElementById('noSelection');
        this.conversationContent = document.getElementById('conversationContent');
        this.selectedUserIdEl = document.getElementById('selectedUserId');
        this.messagesContainer = document.getElementById('messagesContainer');
        this.interventionInput = document.getElementById('interventionInput');
        this.sendInterventionBtn = document.getElementById('sendInterventionBtn');
        this.refreshBtn = document.getElementById('refreshBtn');
    }

    attachEventListeners() {
        this.sendInterventionBtn.addEventListener('click', () => this.sendIntervention());
        this.refreshBtn.addEventListener('click', () => this.loadSelectedConversation());
    }

    async loadConversations() {
        try {
            const response = await fetch(`${this.apiUrl}/live-conversations`);
            if (response.ok) {
                this.conversations = await response.json();
                this.renderConversationList();
            }
        } catch (error) {
            console.error('Error loading conversations:', error);
        }
    }

    renderConversationList() {
        if (this.conversations.length === 0) {
            this.conversationList.innerHTML = '<div class="loading">Aktif konuşma yok</div>';
            return;
        }

        this.conversationList.innerHTML = this.conversations.map(conv => {
            const isActive = conv._id === this.selectedUserId;
            const timeAgo = this.getTimeAgo(conv.last_timestamp);
            
            return `
                <div class="conversation-item ${isActive ? 'active' : ''}" 
                     onclick="liveChatMonitor.selectConversation('${conv._id}')">
                    <div class="conversation-item-header">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span class="status-indicator"></span>
                            <strong>${conv._id}</strong>
                        </div>
                        <span class="conversation-time">${timeAgo}</span>
                    </div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 4px;">
                        ${conv.message_count} mesaj
                    </div>
                    <div style="font-size: 12px; color: #475569; margin-top: 4px;">
                        ${conv.last_message.substring(0, 50)}...
                    </div>
                </div>
            `;
        }).join('');
    }

    async selectConversation(userId) {
        this.selectedUserId = userId;
        this.noSelection.style.display = 'none';
        this.conversationContent.style.display = 'flex';
        this.selectedUserIdEl.textContent = userId;
        
        this.renderConversationList();
        await this.loadSelectedConversation();
    }

    async loadSelectedConversation() {
        if (!this.selectedUserId) return;

        try {
            const response = await fetch(`${this.apiUrl}/conversation/${this.selectedUserId}`);
            if (response.ok) {
                const messages = await response.json();
                this.renderMessages(messages);
            }
        } catch (error) {
            console.error('Error loading conversation:', error);
        }
    }

    renderMessages(messages) {
        if (messages.length === 0) {
            this.messagesContainer.innerHTML = '<div class="loading">Mesaj yok</div>';
            return;
        }

        this.messagesContainer.innerHTML = messages.map(msg => {
            const time = new Date(msg.timestamp).toLocaleTimeString('tr-TR');
            const sender = msg.sender || 'user';
            
            return `
                <div class="message">
                    <div class="message-header">
                        <span><strong>${sender === 'user' ? '👤 Kullanıcı' : '🤖 Bot'}</strong></span>
                        <span>${time}</span>
                    </div>
                    <div class="message-text">${msg.message || msg.text}</div>
                    ${msg.confidence ? `<div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">
                        Güven: ${(msg.confidence * 100).toFixed(1)}%
                    </div>` : ''}
                </div>
            `;
        }).join('');

        // Scroll to bottom
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    async sendIntervention() {
        const message = this.interventionInput.value.trim();
        if (!message || !this.selectedUserId) return;

        try {
            const response = await fetch(`${this.apiUrl}/intervention`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: this.selectedUserId,
                    message: message,
                    admin: true
                })
            });

            if (response.ok) {
                this.interventionInput.value = '';
                await this.loadSelectedConversation();
                alert('Mesajınız gönderildi! Bot otomatik olarak durdu.');
            } else {
                alert('Mesaj gönderilemedi!');
            }
        } catch (error) {
            console.error('Error sending intervention:', error);
            alert('Bağlantı hatası!');
        }
    }

    getTimeAgo(timestamp) {
        const now = new Date();
        const time = new Date(timestamp);
        const diffMs = now - time;
        const diffMins = Math.floor(diffMs / 60000);

        if (diffMins < 1) return 'Az önce';
        if (diffMins < 60) return `${diffMins} dakika önce`;
        
        const diffHours = Math.floor(diffMins / 60);
        if (diffHours < 24) return `${diffHours} saat önce`;
        
        const diffDays = Math.floor(diffHours / 24);
        return `${diffDays} gün önce`;
    }
}

// Initialize live chat monitor
let liveChatMonitor;
document.addEventListener('DOMContentLoaded', () => {
    liveChatMonitor = new LiveChatMonitor();
});
