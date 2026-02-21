<template>
  <header class="header">
    <div class="header-left">
      <router-link to="/" class="logo">
        <div class="menu-icon">📊</div>
        <span>DiagnoBot</span>
      </router-link>
      
      <nav class="main-nav">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/about" class="nav-link">About Us</router-link>
        <router-link to="/pricing" class="nav-link">Pricing</router-link>
        <router-link to="/about#faq" class="nav-link">FAQs</router-link>
        <router-link to="/about" class="nav-link">Terms</router-link>
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
          <router-link to="/signup" class="btn btn-outline">Sign Up</router-link>
          <router-link to="/login" class="btn btn-primary">Log In</router-link>
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
  padding: 1rem 2rem;
  background: var(--bg-color, white);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: background 0.3s ease;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-color, #6c5ce7);
  text-decoration: none;
  cursor: pointer;
  transition: color 0.3s ease;
}

.logo:hover {
  color: var(--primary-dark, #764ba2);
}

.menu-icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.main-nav {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-link {
  color: var(--text-color, #2d3436);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: var(--primary-color, #6c5ce7);
}

.nav-link.router-link-active {
  color: var(--primary-color, #6c5ce7);
  font-weight: 700;
}

.header-right {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.theme-toggle {
  background: none;
  border: 2px solid var(--gray, #dfe6e9);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.theme-toggle:hover {
  border-color: var(--primary-color);
  transform: rotate(20deg) scale(1.1);
  box-shadow: 0 2px 8px rgba(108, 92, 231, 0.3);
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
  font-size: 14px;
  color: var(--text-color, #2d3436);
  font-weight: 500;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}

.btn-outline {
  color: var(--text-color, #333);
  background: transparent;
  border: 2px solid var(--text-color, #333);
}

.btn-outline:hover {
  background: color-mix(in srgb, var(--primary-color) 10%, transparent);
  border-color: var(--primary-color, #6c5ce7);
  color: var(--primary-color, #6c5ce7);
}

.btn-primary {
  background: linear-gradient(135deg, #6c5ce7, #a29bfe);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(108, 92, 231, 0.4);
}

.btn-logout {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #d63031, #fab1a0);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-logout:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(214, 48, 49, 0.4);
}

@media (max-width: 600px) {
  .header {
    padding: 0.75rem 1rem;
  }

  .logo {
    font-size: 1.2rem;
  }

  .user-name {
    display: none;
  }

  .header-right {
    gap: 0.5rem;
  }

  .btn {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }

  .theme-toggle {
    width: 34px;
    height: 34px;
    font-size: 1rem;
  }

  .main-nav {
    display: none; /* Hide top nav on mobile, could move to a hamburger menu later */
  }
}
</style>
