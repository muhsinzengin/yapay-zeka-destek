// Training Management JavaScript
// Handles adding, editing, and deleting training data

class TrainingManager {
    constructor() {
        this.apiUrl = 'http://localhost:5000/api';
        this.trainingData = [];
        
        this.initializeElements();
        this.attachEventListeners();
        this.loadTrainingData();
    }

    initializeElements() {
        this.form = document.getElementById('trainingForm');
        this.questionInput = document.getElementById('questionInput');
        this.answerInput = document.getElementById('answerInput');
        this.intentInput = document.getElementById('intentInput');
        this.trainingList = document.getElementById('trainingList');
        this.searchInput = document.getElementById('searchInput');
        this.trainModelBtn = document.getElementById('trainModelBtn');
    }

    attachEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.searchInput.addEventListener('input', () => this.filterTrainingData());
        this.trainModelBtn.addEventListener('click', () => this.trainModel());
    }

    async handleSubmit(e) {
        e.preventDefault();

        const questions = this.questionInput.value
            .split(',')
            .map(q => q.trim())
            .filter(q => q.length > 0);

        const answer = this.answerInput.value.trim();
        const intent = this.intentInput.value.trim() || 'custom_' + Date.now();

        const trainingData = {
            intent: intent,
            questions: questions,
            answer: answer,
            created_at: new Date().toISOString()
        };

        try {
            const response = await fetch(`${this.apiUrl}/training-data`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(trainingData)
            });

            if (response.ok) {
                alert('Eğitim verisi kaydedildi!');
                this.form.reset();
                this.loadTrainingData();
            } else {
                alert('Hata oluştu!');
            }
        } catch (error) {
            console.error('Error saving training data:', error);
            alert('Bağlantı hatası!');
        }
    }

    async loadTrainingData() {
        try {
            const response = await fetch(`${this.apiUrl}/training-data`);
            if (response.ok) {
                this.trainingData = await response.json();
                this.renderTrainingData();
            }
        } catch (error) {
            console.error('Error loading training data:', error);
            this.trainingList.innerHTML = '<div class="loading">Veri yüklenemedi</div>';
        }
    }

    renderTrainingData(data = this.trainingData) {
        if (data.length === 0) {
            this.trainingList.innerHTML = '<div class="loading">Henüz eğitim verisi yok</div>';
            return;
        }

        this.trainingList.innerHTML = data.map(item => `
            <div class="training-item">
                <div class="training-item-header">
                    <span class="intent-badge">${item.intent}</span>
                    <button class="delete-btn" onclick="trainingManager.deleteItem('${item._id || item.id}')">
                        🗑️ Sil
                    </button>
                </div>
                <div class="questions-list">
                    ${item.questions.map(q => `<span class="question-tag">${q}</span>`).join('')}
                </div>
                <div class="answer-text">
                    ${item.answer}
                </div>
            </div>
        `).join('');
    }

    filterTrainingData() {
        const searchTerm = this.searchInput.value.toLowerCase();
        const filtered = this.trainingData.filter(item => {
            return item.intent.toLowerCase().includes(searchTerm) ||
                   item.questions.some(q => q.toLowerCase().includes(searchTerm)) ||
                   item.answer.toLowerCase().includes(searchTerm);
        });
        this.renderTrainingData(filtered);
    }

    async deleteItem(itemId) {
        if (!confirm('Bu eğitim verisini silmek istediğinize emin misiniz?')) {
            return;
        }

        try {
            const response = await fetch(`${this.apiUrl}/training-data/${itemId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                alert('Silindi!');
                this.loadTrainingData();
            } else {
                alert('Silme hatası!');
            }
        } catch (error) {
            console.error('Error deleting training data:', error);
            alert('Bağlantı hatası!');
        }
    }

    async trainModel() {
        if (!confirm('Modeli eğitmek istediğinize emin misiniz? Bu işlem birkaç dakika sürebilir.')) {
            return;
        }

        this.trainModelBtn.disabled = true;
        this.trainModelBtn.textContent = '⏳ Eğitiliyor...';

        try {
            const response = await fetch(`${this.apiUrl}/train-model`, {
                method: 'POST'
            });

            if (response.ok) {
                alert('Model eğitimi başlatıldı!');
            } else {
                alert('Eğitim başlatılamadı!');
            }
        } catch (error) {
            console.error('Error training model:', error);
            alert('Bağlantı hatası!');
        } finally {
            this.trainModelBtn.disabled = false;
            this.trainModelBtn.textContent = '🚀 Modeli Eğit';
        }
    }
}

// Initialize training manager
let trainingManager;
document.addEventListener('DOMContentLoaded', () => {
    trainingManager = new TrainingManager();
});
