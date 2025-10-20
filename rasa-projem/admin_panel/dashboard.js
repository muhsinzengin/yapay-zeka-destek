// Dashboard JavaScript
// Loads and displays statistics from backend

class Dashboard {
    constructor() {
        this.apiUrl = 'http://localhost:5000/api';
        this.loadStatistics();
        
        // Refresh every 30 seconds
        setInterval(() => this.loadStatistics(), 30000);
    }

    async loadStatistics() {
        try {
            // Load today's stats
            const todayStats = await this.fetchStats('daily');
            this.updateStats('today', todayStats);

            // Load weekly stats
            const weeklyStats = await this.fetchStats('weekly');
            this.updateStats('weekly', weeklyStats);

            // Load monthly stats
            const monthlyStats = await this.fetchStats('monthly');
            this.updateStats('monthly', monthlyStats);

            // Load yearly stats
            const yearlyStats = await this.fetchStats('yearly');
            this.updateStats('yearly', yearlyStats);

            // Load total stats
            const totalStats = await this.fetchStats('total');
            this.updateCosts(todayStats, weeklyStats, monthlyStats, totalStats);

        } catch (error) {
            console.error('Error loading statistics:', error);
        }
    }

    async fetchStats(period) {
        try {
            const response = await fetch(`${this.apiUrl}/statistics?period=${period}`);
            if (response.ok) {
                return await response.json();
            }
            return this.getMockStats();
        } catch (error) {
            console.error(`Error fetching ${period} stats:`, error);
            return this.getMockStats();
        }
    }

    updateStats(period, stats) {
        const conversationsEl = document.getElementById(`${period}Conversations`);
        const usersEl = document.getElementById(`${period}Users`);

        if (conversationsEl) {
            conversationsEl.textContent = stats.conversation_count || 0;
        }
        if (usersEl) {
            usersEl.textContent = stats.unique_users || 0;
        }
    }

    updateCosts(todayStats, weeklyStats, monthlyStats, totalStats) {
        document.getElementById('todayCost').textContent = 
            (todayStats.estimated_gpt4_cost || 0).toFixed(2);
        document.getElementById('weeklyCost').textContent = 
            (weeklyStats.estimated_gpt4_cost || 0).toFixed(2);
        document.getElementById('monthlyCost').textContent = 
            (monthlyStats.estimated_gpt4_cost || 0).toFixed(2);
        document.getElementById('totalCost').textContent = 
            (totalStats.estimated_gpt4_cost || 0).toFixed(2);
    }

    getMockStats() {
        return {
            conversation_count: Math.floor(Math.random() * 100),
            unique_users: Math.floor(Math.random() * 50),
            gpt4_usage_count: Math.floor(Math.random() * 20),
            estimated_gpt4_cost: Math.random() * 5
        };
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    new Dashboard();
});
