<template>
  <div class="auth-wrapper">
    <!-- 3D Floating Shapes -->
    <div class="shape shape-torus-1"></div>
    <div class="shape shape-squiggle-1"></div>
    <div class="shape shape-pill-1"></div>
    <div class="shape shape-torus-2"></div>
    <div class="shape shape-squiggle-2"></div>
    <div class="shape shape-wave-1"></div>

    <div class="glass-card">
      <div class="logo-header">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="logo-icon">
          <rect x="3" y="3" width="18" height="18" rx="4" fill="white" fill-opacity="0.9"/>
          <path d="M7 12h4l2-5 3 10 2-5h3" stroke="var(--primary-color)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>DiagnoBot</span>
      </div>

      <h2 class="auth-title">Login</h2>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="input-group">
          <label>Email</label>
          <input 
            type="email" 
            v-model="form.email" 
            placeholder="username@gmail.com" 
            class="solid-input"
            required
          />
        </div>

        <div class="input-group">
          <label>Password</label>
          <div class="password-wrapper">
            <input 
              :type="showPassword ? 'text' : 'password'" 
              v-model="form.password" 
              placeholder="Password" 
              class="solid-input"
              required
            />
            <button type="button" class="eye-btn" @click="showPassword = !showPassword">
              <svg v-if="!showPassword" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
              <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>
            </button>
          </div>
        </div>

        <a href="#" class="forgot-link" @click.prevent="handleForgotPassword">Forgot Password?</a>

        <div v-if="error" class="error-text">{{ error }}</div>
        <div v-if="loginSuccess" class="success-text">Login successful!</div>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign in' }}
        </button>
      </form>

      <div class="divider">
        <span>or continue with</span>
      </div>

      <div class="social-buttons">
        <button type="button" class="social-btn" @click.prevent="handleGoogleLogin" title="Sign in with Google">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
        </button>
        <button class="social-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="#333" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
        </button>
        <button class="social-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="#1877F2" xmlns="http://www.w3.org/2000/svg"><path d="M24 12.073C24 5.405 18.627 0 12 0S0 5.405 0 12.073C0 18.098 4.388 23.094 10.125 24v-8.437H7.078v-3.49h3.047v-2.66c0-3.005 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.267h3.328l-.532 3.49h-2.796V24C19.612 23.094 24 18.098 24 12.073z"/></svg>
        </button>
      </div>

      <div class="bottom-text">
        Don't have an account yet? <router-link to="/signup">Register for free</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'LoginPage',
  setup() {
    const router = useRouter()
    const form = ref({
      email: '',
      password: ''
    })
    const showPassword = ref(false)
    const loading = ref(false)
    const error = ref('')
    const loginSuccess = ref(false)

    const handleLogin = async () => {
      error.value = ''
      loading.value = true

      try {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(form.value)
        })

        const data = await response.json()

        if (data.success) {
          localStorage.setItem('authToken', data.token)
          localStorage.setItem('user', JSON.stringify(data.user))
          loginSuccess.value = true
          setTimeout(() => router.push('/'), 1000)
        } else {
          error.value = data.error || data.message || 'Login failed. Please try again.'
        }
      } catch (err) {
        error.value = 'Connection error (make sure backend is running).'
      } finally {
        loading.value = false
      }
    }

    const handleGoogleLogin = () => {
      error.value = ''
      loading.value = true
      
      try {
        const client = google.accounts.oauth2.initTokenClient({
          client_id: '184331640474-p8g0qjl3df8cfd6mdpibq1i6epvivkqd.apps.googleusercontent.com',
          scope: 'email profile',
          callback: async (tokenResponse) => {
            if (tokenResponse && tokenResponse.access_token) {
              try {
                const response = await fetch('/api/auth/google', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ access_token: tokenResponse.access_token })
                })
                
                const data = await response.json()
                
                if (data.success) {
                  localStorage.setItem('authToken', data.token)
                  localStorage.setItem('user', JSON.stringify(data.user))
                  loginSuccess.value = true
                  setTimeout(() => { window.location.href = '/dashboard' }, 500)
                } else {
                  error.value = data.error || data.message || 'Google authentication failed.'
                }
              } catch (err) {
                error.value = 'Connection error during Google authentication (make sure backend is running).'
                console.error(err)
              } finally {
                loading.value = false
              }
            } else {
              error.value = 'Failed to get Google authorization.'
              loading.value = false
            }
          },
          error_callback: () => {
            error.value = 'Google authentication was cancelled/failed.'
            loading.value = false
          }
        });
        client.requestAccessToken();
      } catch (err) {
        error.value = 'Google Identity Services could not be loaded.'
        console.error(err)
        loading.value = false
      }
    }

    const handleForgotPassword = () => {
      alert('Password reset link sent to your email.')
    }

    return {
      form,
      showPassword,
      loading,
      error,
      loginSuccess,
      handleLogin,
      handleGoogleLogin,
      handleForgotPassword
    }
  }
}
</script>

<style scoped>
/* Base Container */
.auth-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1e1b4b 0%, #3730a3 50%, #4338ca 100%);
  position: relative;
  overflow: hidden;
  font-family: 'Inter', sans-serif;
}

/* 3D Shapes Styling to match reference image */
.shape {
  position: absolute;
  filter: drop-shadow(0 20px 30px rgba(0,0,0,0.4));
  z-index: 1;
}

.shape-torus-1 {
  width: 120px;
  height: 120px;
  border: 35px solid #6366f1;
  border-radius: 50%;
  top: 8%;
  left: 20%;
  box-sizing: border-box;
  box-shadow: inset 10px 10px 20px rgba(0,0,0,0.2), 10px 10px 20px rgba(255,255,255,0.1);
  transform: rotate(20deg);
}

.shape-pill-1 {
  width: 140px;
  height: 60px;
  background: linear-gradient(135deg, #a5b4fc, #818cf8);
  border-radius: 30px;
  top: 30%;
  left: 12%;
  transform: rotate(40deg);
  box-shadow: inset -10px -10px 20px rgba(0,0,0,0.2), inset 10px 10px 20px rgba(255,255,255,0.4);
}

.shape-squiggle-1 {
  width: 250px;
  height: 250px;
  border: 45px solid transparent;
  border-top-color: #312e81;
  border-right-color: #312e81;
  border-radius: 50%;
  bottom: -5%;
  left: 5%;
  transform: rotate(-10deg);
  filter: drop-shadow(15px 15px 25px rgba(0,0,0,0.5));
}

.shape-torus-2 {
  width: 200px;
  height: 200px;
  border: 50px solid #4f46e5;
  border-radius: 50%;
  border-bottom-color: transparent;
  top: 15%;
  right: 15%;
  transform: rotate(35deg);
  filter: drop-shadow(-15px 15px 30px rgba(0,0,0,0.5));
}

.shape-squiggle-2 {
  width: 120px;
  height: 35px;
  background: #a5b4fc;
  border-radius: 17px;
  bottom: 30%;
  right: 18%;
  transform: rotate(-15deg);
  box-shadow: inset -5px -5px 10px rgba(0,0,0,0.2), inset 5px 5px 10px rgba(255,255,255,0.4);
}

.shape-wave-1 {
  width: 200px;
  height: 200px;
  border: 50px solid transparent;
  border-bottom-color: #818cf8;
  border-right-color: #818cf8;
  border-radius: 50%;
  bottom: 0%;
  right: 5%;
  transform: rotate(-30deg);
  filter: drop-shadow(-15px 15px 25px rgba(0,0,0,0.4));
}


/* Glass Card Main Container */
.glass-card {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 24px;
  padding: 3rem 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  color: white;
}

.logo-header {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  font-weight: 700;
  font-size: 1.35rem;
  margin-bottom: 2.5rem;
  letter-spacing: -0.02em;
}

.auth-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-align: left;
}

/* Form Styles */
.input-group {
  margin-bottom: 1.25rem;
  text-align: left;
}

.input-group label {
  display: block;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 500;
}

.solid-input {
  width: 100%;
  padding: 0.875rem 1rem;
  border-radius: 10px;
  border: none;
  background: var(--surface-color);
  color: var(--text-main);
  font-size: 0.95rem;
  font-family: inherit;
  box-sizing: border-box;
}

.solid-input::placeholder {
  color: var(--text-muted);
}

.solid-input:focus {
  outline: 3px solid rgba(129, 140, 248, 0.5);
}

.password-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.eye-btn {
  position: absolute;
  right: 12px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  display: flex;
}

.forgot-link {
  display: block;
  text-align: left;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  margin-bottom: 1.5rem;
  margin-top: 0.5rem;
}

.forgot-link:hover {
  text-decoration: underline;
}

.submit-btn {
  width: 100%;
  padding: 0.875rem;
  background: #1e1b4b; /* Dark indigo */
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.submit-btn:hover {
  background: #312e81;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

/* Divider */
.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin-bottom: 1.5rem;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.divider span {
  padding: 0 15px;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.8);
}

/* Social Buttons */
.social-buttons {
  display: flex;
  justify-content: center;
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.social-btn {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  background: var(--surface-color);
  border: none;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.social-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

.bottom-text {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.9);
  text-align: center;
}

.bottom-text a {
  color: white;
  font-weight: 700;
  text-decoration: none;
}

.bottom-text a:hover {
  text-decoration: underline;
}

.error-text {
  color: #fca5a5;
  font-size: 0.85rem;
  margin-bottom: 1rem;
  text-align: center;
}

.success-text {
  color: #6ee7b7;
  font-size: 0.85rem;
  margin-bottom: 1rem;
  text-align: center;
}

@media (max-width: 480px) {
  .shape {
    display: none; /* Hide complex shapes on mobile to keep it clean */
  }
  .glass-card {
    border: none;
    background: transparent;
    box-shadow: none;
    backdrop-filter: none;
  }
}

</style>

