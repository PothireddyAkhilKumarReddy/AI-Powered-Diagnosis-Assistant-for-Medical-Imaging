<template>
  <div class="auth-wrapper">
    <!-- Floating background decorative shapes -->
    <div class="shape shape-torus-1"></div>
    <div class="shape shape-pill-1"></div>
    <div class="shape shape-squiggle-1"></div>
    <div class="shape shape-torus-2"></div>
    <div class="shape shape-squiggle-2"></div>
    <div class="shape shape-wave-1"></div>

    <div class="glass-card slide-in-bottom">
      <div class="logo-header">
        <div class="logo-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="18" height="18" rx="4" fill="currentColor" fill-opacity="0.2"/>
            <path d="M7 16V12M11 16V8M15 16V10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        DiagnoBot
      </div>

      <h1 class="auth-title">Create Account</h1>

      <form @submit.prevent="handleSignup" class="auth-form">
        <div class="input-group">
          <label for="fullname">Full Name</label>
          <input
            id="fullname"
            v-model="form.fullName"
            type="text"
            placeholder="John Doe"
            required
            class="solid-input"
          />
        </div>

        <div class="input-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="username@gmail.com"
            required
            class="solid-input"
          />
        </div>

        <div class="input-group">
          <label for="password">Password</label>
          <div class="password-wrapper">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="••••••••"
              required
              class="solid-input"
            />
            <button type="button" class="eye-btn" @click="showPassword = !showPassword" aria-label="Toggle password visibility">
              <span v-if="showPassword">🙈</span>
              <span v-else>👁️</span>
            </button>
          </div>
        </div>

        <div class="input-group">
          <label for="confirm-password">Confirm Password</label>
          <div class="password-wrapper">
            <input
              id="confirm-password"
              v-model="form.confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              placeholder="••••••••"
              required
              class="solid-input"
            />
            <button type="button" class="eye-btn" @click="showConfirmPassword = !showConfirmPassword" aria-label="Toggle password visibility">
              <span v-if="showConfirmPassword">🙈</span>
              <span v-else>👁️</span>
            </button>
          </div>
        </div>

        <div class="input-group checkbox-group">
          <input
            id="terms"
            v-model="form.agreeTerms"
            type="checkbox"
            required
          />
          <label for="terms">
            I agree to the <a href="#" @click.prevent="handleTerms">Terms</a> and <a href="#" @click.prevent="handlePrivacy">Privacy Policy</a>
          </label>
        </div>

        <div v-if="error" class="error-text">
          {{ error }}
        </div>

        <div v-if="signupSuccess" class="success-text">
          ✓ Account created! Redirecting...
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="submit-btn"
        >
          {{ loading ? 'Creating account...' : 'Sign up' }}
        </button>
      </form>

      <div class="divider">
        <span>or continue with</span>
      </div>

      <div class="social-buttons">
        <button type="button" class="social-btn google" @click.prevent="handleGoogleLogin" title="Sign up with Google">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
          </svg>
        </button>
        <button class="social-btn github">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.49.5.092.682-.217.682-.482v-1.892c-2.782.605-3.369-1.152-3.369-1.152-.454-1.154-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852v2.75c0 .268.18.58.688.481A9.998 9.998 0 0022 12c0-5.523-4.477-10-10-10z" fill="#1C1C1C"/>
          </svg>
        </button>
      </div>

      <p class="bottom-text">
        Already have an account?
        <router-link to="/login">Sign in here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'SignupPage',
  setup() {
    const router = useRouter()
    const form = ref({
      fullName: '',
      email: '',
      password: '',
      confirmPassword: '',
      agreeTerms: false
    })
    const loading = ref(false)
    const error = ref('')
    const signupSuccess = ref(false)
    const showPassword = ref(false)
    const showConfirmPassword = ref(false)

    const validateForm = () => {
      if (form.value.password.length < 8) {
        error.value = 'Password must be at least 8 characters long.'
        return false
      }
      
      if (form.value.password !== form.value.confirmPassword) {
        error.value = 'Passwords do not match.'
        return false
      }

      if (!form.value.agreeTerms) {
        error.value = 'You must agree to the terms and conditions.'
        return false
      }

      return true
    }

    const handleSignup = async () => {
      error.value = ''
      
      if (!validateForm()) {
        return
      }

      loading.value = true

      try {
        const response = await fetch('/api/auth/signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            fullName: form.value.fullName,
            email: form.value.email,
            password: form.value.password
          })
        })

        const data = await response.json()

        if (data.success || response.ok) {
          signupSuccess.value = true
          
          setTimeout(() => {
            router.push('/login')
          }, 1500)
        } else {
          error.value = data.error || data.message || 'Signup failed. Please try again.'
        }
      } catch (err) {
        error.value = 'Connection error (make sure backend is running). Please check your internet and try again.'
        console.error('Signup error:', err)
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
                  signupSuccess.value = true
                  setTimeout(() => { window.location.href = '/dashboard' }, 1000)
                } else {
                  error.value = data.error || data.message || 'Google signup failed.'
                }
              } catch (err) {
                error.value = 'Connection error during Google signup (make sure backend is running).'
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

    const handleTerms = () => {
      alert('Terms of Service\n\nThis is a placeholder for Terms of Service.')
    }

    const handlePrivacy = () => {
      alert('Privacy Policy\n\nThis is a placeholder for Privacy Policy.')
    }

    return {
      form,
      loading,
      error,
      signupSuccess,
      handleSignup,
      handleGoogleLogin,
      handleTerms,
      handlePrivacy,
      showPassword,
      showConfirmPassword
    }
  }
}
</script>

<style scoped>
/* Animations */
@keyframes slideUpFade {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-in-bottom {
  animation: slideUpFade 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

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
  padding: 1rem;
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
  max-width: 440px;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 24px;
  padding: 3rem 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  color: white;
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.logo-header {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  font-weight: 700;
  font-size: 1.35rem;
  margin-bottom: 2rem;
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
  margin-bottom: 1.2rem;
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
  font-size: 1.2rem;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 1.5rem;
  margin-top: 0.5rem;
}

.checkbox-group label {
  margin-bottom: 0;
  font-size: 0.8rem;
  font-weight: 400;
}

.checkbox-group a {
  color: #a5b4fc;
  font-weight: 600;
  text-decoration: none;
}

.checkbox-group a:hover {
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
  margin: 0;
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
