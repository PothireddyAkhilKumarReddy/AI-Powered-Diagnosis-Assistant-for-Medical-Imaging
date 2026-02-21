<template>
  <div class="auth-container">
    <div class="auth-box">
      <h1>Welcome Back</h1>
      <p class="subtitle">Login to DiagnoBot</p>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label for="email">Email Address</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="your@email.com"
            required
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="••••••••"
            required
            class="form-input"
          />
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div v-if="loginSuccess" class="success-message">
          ✓ Login successful! Redirecting...
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="auth-button"
        >
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <div class="divider">or</div>

      <div class="social-login">
        <button class="social-button google">
          <span>Google</span>
        </button>
        <button class="social-button github">
          <span>GitHub</span>
        </button>
      </div>

      <p class="toggle-text">
        Don't have an account?
        <router-link to="/signup" class="auth-link">Sign up here</router-link>
      </p>

      <p class="forgot-password">
        <a href="#" @click.prevent="handleForgotPassword" class="auth-link">Forgot password?</a>
      </p>
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
          
          setTimeout(() => {
            router.push('/')
          }, 1000)
        } else {
          error.value = data.message || 'Login failed. Please try again.'
        }
      } catch (err) {
        error.value = 'Connection error. Please check your internet and try again.'
        console.error('Login error:', err)
      } finally {
        loading.value = false
      }
    }

    const handleForgotPassword = () => {
      alert('Password reset link would be sent to your email.')
    }

    return {
      form,
      loading,
      error,
      loginSuccess,
      handleLogin,
      handleForgotPassword
    }
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 100px);
  background: linear-gradient(135deg, #6c5ce7 0%, #764ba2 100%);
  padding: 20px;
}

.auth-box {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

h1 {
  font-size: 28px;
  color: #2d3436;
  margin: 0 0 10px 0;
  text-align: center;
}

.subtitle {
  color: #636e72;
  text-align: center;
  margin: 0 0 30px 0;
  font-size: 14px;
}

.auth-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #2d3436;
  font-weight: 500;
  font-size: 14px;
}

.form-input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #dfe6e9;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #6c5ce7;
  box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.1);
}

.form-input::placeholder {
  color: #b2bec3;
}

.auth-button {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #6c5ce7 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 15px;
}

.auth-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(108, 92, 231, 0.4);
}

.auth-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  background: #fab1a0;
  color: #d63031;
  padding: 10px 12px;
  border-radius: 6px;
  margin-bottom: 15px;
  font-size: 13px;
  text-align: center;
}

.success-message {
  background: #a8e6cf;
  color: #27ae60;
  padding: 10px 12px;
  border-radius: 6px;
  margin-bottom: 15px;
  font-size: 13px;
  text-align: center;
}

.divider {
  text-align: center;
  color: #b2bec3;
  margin: 25px 0;
  position: relative;
}

.divider::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  width: 40%;
  height: 1px;
  background: #dfe6e9;
}

.divider::after {
  content: '';
  position: absolute;
  right: 0;
  top: 50%;
  width: 40%;
  height: 1px;
  background: #dfe6e9;
}

.social-login {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 25px;
}

.social-button {
  padding: 12px;
  border: 1px solid #dfe6e9;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.social-button:hover {
  border-color: #6c5ce7;
  background: #f5f5f5;
}

.toggle-text {
  text-align: center;
  color: #636e72;
  font-size: 14px;
  margin: 0 0 15px 0;
}

.auth-link {
  color: #6c5ce7;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.auth-link:hover {
  color: #764ba2;
}

.forgot-password {
  text-align: center;
  margin: 0;
}

@media (max-width: 600px) {
  .auth-box {
    padding: 30px 20px;
  }

  h1 {
    font-size: 24px;
  }

  .social-login {
    grid-template-columns: 1fr;
  }
}
</style>
