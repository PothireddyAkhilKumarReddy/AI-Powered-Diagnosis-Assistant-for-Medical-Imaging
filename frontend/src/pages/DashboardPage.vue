<template>
  <div class="dashboard-container">
    <div class="container">
      <!-- Welcome Section -->
      <div class="welcome-section fade-in">
        <h1>Welcome back, {{ userName }}! 👋</h1>
        <p class="text-muted">Your AI Health Assistant is ready to help</p>
      </div>

      <!-- Stats Section -->
      <div class="stats-grid">
        <div class="stat-card fade-in">
          <div class="stat-icon">📋</div>
          <div class="stat-content">
            <h3>{{ analysisCount }}</h3>
            <p>Total Analysis</p>
          </div>
        </div>
        <div class="stat-card fade-in" style="animation-delay: 0.1s">
          <div class="stat-icon">✅</div>
          <div class="stat-content">
            <h3>{{ diagnosisCount }}</h3>
            <p>Diagnoses</p>
          </div>
        </div>
        <div class="stat-card fade-in" style="animation-delay: 0.2s">
          <div class="stat-icon">💬</div>
          <div class="stat-content">
            <h3>{{ chatCount }}</h3>
            <p>Chat Messages</p>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions">
        <h2>Quick Actions</h2>
        <div class="action-buttons">
          <button class="action-btn" @click="scrollToChat">
            <span class="action-icon">🏥</span>
            <span>Analyze X-Ray</span>
          </button>
          <button class="action-btn" @click="showChat">
            <span class="action-icon">💬</span>
            <span>Ask Doctor</span>
          </button>
          <button class="action-btn" @click="viewHistory">
            <span class="action-icon">📚</span>
            <span>View History</span>
          </button>
          <button class="action-btn" @click="editProfile">
            <span class="action-icon">⚙️</span>
            <span>Settings</span>
          </button>
        </div>
      </div>

      <!-- Recent Analysis -->
      <div class="recent-section">
        <h2>Recent Analysis</h2>
        <div v-if="recentAnalysis.length > 0" class="analysis-list">
          <div v-for="(item, index) in recentAnalysis" :key="index" class="analysis-item fade-in" :style="{ 'animation-delay': (index * 0.1) + 's' }">
            <div class="item-date">{{ formatDate(item.date) }}</div>
            <div class="item-result">
              <span class="badge" :class="`badge-${item.type.toLowerCase()}`">{{ item.type }}</span>
            </div>
            <div class="item-description">{{ item.description }}</div>
          </div>
        </div>
        <div v-else class="empty-state">
          <p>No analysis yet. Start by uploading an X-ray image!</p>
        </div>
      </div>

      <!-- Chat Section -->
      <ChatSection ref="chatSection" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import ChatSection from '../components/ChatSection.vue'

export default {
  name: 'DashboardPage',
  components: {
    ChatSection
  },
  setup() {
    const userName = ref('User')
    const analysisCount = ref(0)
    const diagnosisCount = ref(0)
    const chatCount = ref(0)
    const recentAnalysis = ref([])
    const chatSection = ref(null)

    onMounted(() => {
      loadUserData()
      loadAnalysisHistory()
    })

    const loadUserData = () => {
      const user = localStorage.getItem('user')
      if (user) {
        try {
          const userData = JSON.parse(user)
          userName.value = userData.fullName || userData.email || 'User'
        } catch (e) {
          console.error('Error parsing user data:', e)
        }
      }

      // Get stats from localStorage or API
      analysisCount.value = parseInt(localStorage.getItem('analysisCount') || '0')
      diagnosisCount.value = parseInt(localStorage.getItem('diagnosisCount') || '0')
      chatCount.value = parseInt(localStorage.getItem('chatCount') || '0')
    }

    const loadAnalysisHistory = () => {
      const history = localStorage.getItem('analysisHistory')
      if (history) {
        try {
          recentAnalysis.value = JSON.parse(history).slice(0, 5)
        } catch (e) {
          console.error('Error loading history:', e)
        }
      }
    }

    const scrollToChat = () => {
      if (chatSection.value) {
        chatSection.value.$el.scrollIntoView({ behavior: 'smooth' })
      }
    }

    const showChat = () => {
      scrollToChat()
    }

    const viewHistory = () => {
      alert('Analysis history feature coming soon!')
    }

    const editProfile = () => {
      alert('Profile settings feature coming soon!')
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }

    return {
      userName,
      analysisCount,
      diagnosisCount,
      chatCount,
      recentAnalysis,
      chatSection,
      scrollToChat,
      showChat,
      viewHistory,
      editProfile,
      formatDate
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  flex: 1;
  padding: 2rem 0;
  background: var(--bg-secondary, #f5f7fa);
  transition: background 0.3s ease;
}

.welcome-section {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem;
  background: linear-gradient(135deg, #6c5ce7 0%, #764ba2 100%);
  border-radius: 16px;
  color: white;
  animation: fadeIn 0.6s ease-out;
}

.welcome-section h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.welcome-section p {
  font-size: 1.1rem;
  opacity: 0.9;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: var(--card-bg, white);
  border-radius: 12px;
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px rgba(108, 92, 231, 0.2);
}

.stat-icon {
  font-size: 3rem;
  min-width: 80px;
  text-align: center;
}

.stat-content h3 {
  margin: 0;
  font-size: 2.5rem;
  color: var(--primary-color, #6c5ce7);
}

.stat-content p {
  margin: 0.25rem 0 0 0;
  color: #636e72;
  font-size: 0.95rem;
}

.quick-actions {
  margin-bottom: 3rem;
}

.quick-actions h2 {
  margin-bottom: 1.5rem;
  color: var(--text-color, #2d3436);
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.action-btn {
  background: var(--card-bg, white);
  border: 2px solid var(--gray, #dfe6e9);
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  color: var(--text-color, #2d3436);
}

.action-btn:hover {
  border-color: var(--primary-color, #6c5ce7);
  background: linear-gradient(135deg, rgba(108, 92, 231, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  transform: translateY(-4px);
}

.action-icon {
  font-size: 2rem;
}

.recent-section {
  margin-bottom: 3rem;
}

.recent-section h2 {
  margin-bottom: 1.5rem;
  color: var(--text-color, #2d3436);
}

.analysis-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.analysis-item {
  background: var(--card-bg, white);
  border-radius: 12px;
  padding: 1.5rem;
  display: grid;
  grid-template-columns: 120px auto 1fr;
  align-items: center;
  gap: 1rem;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
}

.analysis-item:hover {
  box-shadow: var(--shadow-md);
}

.item-date {
  font-size: 0.9rem;
  color: #636e72;
  font-weight: 500;
}

.item-result {
  display: flex;
  gap: 0.5rem;
}

.item-description {
  color: var(--text-color, #2d3436);
  font-size: 0.95rem;
}

.badge {
  display: inline-block;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.badge-normal {
  background: rgba(39, 174, 96, 0.1);
  color: #27ae60;
}

.badge-covid-19 {
  background: rgba(214, 48, 49, 0.1);
  color: #d63031;
}

.badge-pneumonia {
  background: rgba(243, 156, 18, 0.1);
  color: #f39c12;
}

.badge-tuberculosis {
  background: rgba(230, 126, 34, 0.1);
  color: #e67e22;
}

.badge-success {
  background: rgba(39, 174, 96, 0.1);
  color: #27ae60;
}

.badge-warning {
  background: rgba(243, 156, 18, 0.1);
  color: #f39c12;
}

.badge-danger {
  background: rgba(214, 48, 49, 0.1);
  color: #d63031;
}

.empty-state {
  background: var(--card-bg, white);
  border-radius: 12px;
  padding: 3rem;
  text-align: center;
  box-shadow: var(--shadow-sm);
  color: #636e72;
}

@media (max-width: 768px) {
  .welcome-section h1 {
    font-size: 1.75rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .analysis-item {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .action-buttons {
    grid-template-columns: repeat(2, 1fr);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
