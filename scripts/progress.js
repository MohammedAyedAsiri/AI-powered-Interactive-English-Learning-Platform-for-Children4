// frontend/scripts/progress.js
class ProgressManager {
    constructor() {
        this.tokenKey = 'lang_tutor_jwt';
        this.init();
    }

    async init() {
        this.checkAuth();
        await this.loadProgressData();
    }

    checkAuth() {
        const token = localStorage.getItem(this.tokenKey);
        if (!token) {
            window.location.href = '/index.html';
            return;
        }
    }

    async loadProgressData() {
        try {
            const response = await fetch('/api/progress', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem(this.tokenKey)}`
                }
            });

            if (!response.ok) throw new Error('Failed to load progress data');
            
            const progressData = await response.json();
            this.handleProgressData(progressData);
            
        } catch (error) {
            this.handleLoadingError(error.message);
        }
    }

    handleProgressData(data) {
        document.getElementById('loading').style.display = 'none';
        
        if (data.length === 0) {
            this.showEmptyState();
            return;
        }

        this.renderProgressChart(data);
        this.renderActivityList(data);
    }

    renderProgressChart(data) {
        const ctx = document.getElementById('progressChart').getContext('2d');
        const chartData = this.prepareChartData(data);

        new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: { color: '#666' }
                    },
                    x: {
                        ticks: { color: '#666' }
                    }
                },
                plugins: {
                    legend: {
                        labels: { color: '#444' }
                    }
                }
            }
        });
    }

    prepareChartData(data) {
        return {
            labels: data.map(entry => new Date(entry.timestamp).toLocaleDateString()),
            datasets: [{
                label: 'Pronunciation Accuracy (%)',
                data: data.map(entry => entry.accuracy),
                borderColor: '#4A90E2',
                backgroundColor: 'rgba(74, 144, 226, 0.1)',
                borderWidth: 2,
                pointRadius: 4,
                tension: 0.4
            }]
        };
    }

    renderActivityList(data) {
        const list = document.getElementById('activityList');
        list.innerHTML = data.map(entry => this.createActivityItem(entry)).join('');
    }

    createActivityItem(entry) {
        return `
            <li class="activity-item">
                <div class="activity-header">
                    <span class="word">${entry.word}</span>
                    <span class="accuracy ${this.getAccuracyClass(entry.accuracy)}">
                        ${entry.accuracy.toFixed(1)}%
                    </span>
                </div>
                <p class="feedback">${entry.feedback}</p>
                <time class="timestamp">
                    ${new Date(entry.timestamp).toLocaleString()}
                </time>
            </li>
        `;
    }

    getAccuracyClass(accuracy) {
        if (accuracy >= 80) return 'high-accuracy';
        if (accuracy >= 60) return 'medium-accuracy';
        return 'low-accuracy';
    }

    handleLoadingError(message) {
        document.getElementById('loading').innerHTML = `
            <div class="error-message">
                <p>⚠️ ${message}</p>
                <button onclick="location.reload()">Try Again</button>
            </div>
        `;
    }

    showEmptyState() {
        document.getElementById('activityList').innerHTML = `
            <div class="empty-state">
                <img src="/images/empty-state.svg" alt="No data">
                <p>No practice sessions yet!</p>
                <a href="/practice.html" class="cta-btn">Start Practicing</a>
            </div>
        `;
    }
}

// Initialize when DOM loads
document.addEventListener('DOMContentLoaded', () => new ProgressManager());