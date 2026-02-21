<template>
  <div class="auth-container">
    <div class="auth-box">
      <h1>Create Account</h1>
      <p class="subtitle">Join DiagnoBot Today</p>

      <form @submit.prevent="handleSignup" class="auth-form">
        <div class="form-group">
          <label for="fullname">Full Name</label>
          <input
            id="fullname"
            v-model="form.fullName"
            type="text"
            placeholder="John Doe"
            required
            class="form-input"
          />
        </div>

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
          <label for="phone">Phone Number (Optional)</label>
          <input
            id="phone"
            v-model="form.phone"
            type="tel"
            placeholder="+1 (555) 000-0000"
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
          <small class="password-hint">At least 8 characters</small>
        </div>

        <div class="form-group">
          <label for="confirm-password">Confirm Password</label>
          <input
            id="confirm-password"
            v-model="form.confirmPassword"
            type="password"
            placeholder="••••••••"
            required
            class="form-input"
          />
        </div>

        <div class="form-group checkbox">
          <input
            id="terms"
            v-model="form.agreeTerms"
            type="checkbox"
            required
          />
          <label for="terms">
            I agree to the
            <a href="#" @click.prevent="handleTerms" class="auth-link">Terms of Service</a>
            and
            <a href="#" @click.prevent="handlePrivacy" class="auth-link">Privacy Policy</a>
          </label>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div v-if="signupSuccess" class="success-message">
          ✓ Account created! Redirecting...
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="auth-button"
        >
          {{ loading ? 'Creating account...' : 'Sign Up' }}
        </button>
      </form>

      <p class="toggle-text">
        Already have an account?
        <router-link to="/login" class="auth-link">Login here</router-link>
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
      phone: '',
      password: '',
      confirmPassword: '',
      agreeTerms: false
    })
    const loading = ref(false)
    const error = ref('')
    const signupSuccess = ref(false)

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
            phone: form.value.phone,
            password: form.value.password
          })
        })

        const data = await response.json()

        if (data.success) {
          signupSuccess.value = true
          
          setTimeout(() => {
            router.push('/login')
          }, 1500)
        } else {
          error.value = data.message || 'Signup failed. Please try again.'
        }
      } catch (err) {
        error.value = 'Connection error. Please check your internet and try again.'
        console.error('Signup error:', err)
      } finally {
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
      handleTerms,
      handlePrivacy
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
  max-width: 450px;
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
  margin-bottom: 18px;
}

.form-group.checkbox {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 15px;
}

.form-group.checkbox input {
  margin-top: 4px;
  cursor: pointer;
}

.form-group.checkbox label {
  margin: 0;
  font-size: 13px;
  color: #636e72;
  line-height: 1.4;
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

.password-hint {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: #a29bfe;
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

.toggle-text {
  text-align: center;
  color: #636e72;
  font-size: 14px;
  margin: 0;
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

@media (max-width: 600px) {
  .auth-box {
    padding: 30px 20px;
  }

  h1 {
    font-size: 24px;
  }
}
</style>
