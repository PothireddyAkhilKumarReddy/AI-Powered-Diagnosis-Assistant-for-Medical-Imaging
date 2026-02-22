<template>
  <header class="header">
    <div class="header-left">
      <router-link to="/" class="logo">
        <div class="menu-icon">📊</div>
        <span>DiagnoBot</span>
      </router-link>
      
      <nav class="main-nav">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link v-if="isAuthenticated" to="/dashboard" class="nav-link">Dashboard</router-link>
        <router-link to="/about" class="nav-link">About Us</router-link>
        <router-link to="/pricing" class="nav-link">Pricing</router-link>
        <router-link to="/faq" class="nav-link">FAQs</router-link>
        <router-link to="/terms" class="nav-link">Terms</router-link>
      </nav>
    </div>
    
    <div class="header-right">
      <button class="theme-toggle" @click="toggleTheme" :title="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'">
        {{ isDark ? '☀️' : '🌙' }}
      </button>

      <div class="auth-buttons">
        <div v-if="isAuthenticated" class="user-menu">
          <span class="user-name">{{ userName }}</span>
          <button @click="handleLogout" class="btn btn-logout">Logout</button>
        </div>
        <div v-else class="auth-links">
          <router-link to="/signup" class="btn btn-primary">Get Started</router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Header',
  setup() {
    const router = useRouter()
    const isAuthenticated = ref(false)
    const userName = ref('')
    const isDark = ref(false)

    onMounted(() => {
      checkAuthStatus()
      // Restore saved theme preference
      const savedTheme = localStorage.getItem('theme')
      if (savedTheme === 'dark') {
        isDark.value = true
        document.documentElement.setAttribute('data-theme', 'dark')
      }
    })

    const toggleTheme = () => {
      isDark.value = !isDark.value
      if (isDark.value) {
        document.documentElement.setAttribute('data-theme', 'dark')
        localStorage.setItem('theme', 'dark')
      } else {
        document.documentElement.removeAttribute('data-theme')
        localStorage.setItem('theme', 'light')
      }
    }

    const checkAuthStatus = () => {
      const authToken = localStorage.getItem('authToken')
      const user = localStorage.getItem('user')
      
      isAuthenticated.value = !!authToken
      if (user) {
        try {
          const userData = JSON.parse(user)
          userName.value = userData.fullName || userData.email || 'User'
        } catch (e) {
          console.error('Error parsing user data:', e)
        }
      }
    }

    const handleLogout = () => {
      if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('authToken')
        localStorage.removeItem('user')
        isAuthenticated.value = false
        router.push('/login')
      }
    }

    return {
      isAuthenticated,
      userName,
      isDark,
      toggleTheme,
      handleLogout
    }
  }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 2rem;
  background: var(--surface-color);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: all 0.3s ease;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-main);
  text-decoration: none;
  cursor: pointer;
  transition: color 0.3s ease;
}

.logo:hover {
  color: var(--primary-color);
}

.menu-icon {
  width: 32px;
  height: 32px;
  background: var(--primary-color);
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  box-shadow: 0 4px 10px rgba(79, 70, 229, 0.3);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 4rem;
}

.main-nav {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-link {
  color: var(--text-muted);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: color 0.3s ease;
}

.nav-link:hover, .nav-link.router-link-active {
  color: var(--text-main);
}

.header-right {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.theme-toggle {
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-full);
  width: 44px;
  height: 44px;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-sm);
  color: var(--text-main);
}

.theme-toggle svg {
  transition: transform 0.3s ease;
}

.theme-toggle:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.15);
  color: var(--primary-color);
}

.theme-toggle:hover svg {
  transform: rotate(15deg);
}

.auth-buttons {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.auth-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.user-menu {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.user-name {
  font-size: 0.95rem;
  color: var(--text-main);
  font-weight: 600;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Auth Buttons override */
.btn-outline {
  background: transparent;
  color: var(--text-main);
  border: 1px solid var(--border-color);
}

.btn-outline:hover {
  border-color: var(--text-muted);
  background: var(--bg-color);
}

.btn-logout {
  background: var(--surface-color);
  color: var(--danger-color);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.btn-logout:hover {
  background: rgba(239, 68, 68, 0.05);
  border-color: rgba(239, 68, 68, 0.5);
  box-shadow: none;
}

@media (max-width: 900px) {
  .header-left {
    gap: 2rem;
  }
  .main-nav {
    display: none;
  }
}

@media (max-width: 600px) {
  .header {
    padding: 1rem;
  }
  .logo span {
    display: none;
  }
  .user-name {
    display: none;
  }
  .header-right {
    gap: 0.75rem;
  }
  .theme-toggle {
    width: 38px;
    height: 38px;
  }
  .btn {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }
}
</style>
