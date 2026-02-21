<template>
  <div class="pricing-container">
    <div class="pricing-content">
      <!-- Left: Features -->
      <div class="pricing-left">
        <router-link to="/" class="back-link">← Get Back</router-link>
        <h1 class="pricing-title">Upgrade Your Plan</h1>
        <p class="pricing-subtitle">Expand your analysis limit or switch to our Unlimited Plan</p>

        <ul class="feature-list">
          <li>
            <span class="check-icon">✅</span>
            <span>Chat with AI Doctor</span>
          </li>
          <li>
            <span class="check-icon">✅</span>
            <span>Upload X-rays and medical images</span>
          </li>
          <li>
            <span class="check-icon">✅</span>
            <span>Get your AI diagnosis and treatment plan</span>
          </li>
          <li>
            <span class="check-icon">✅</span>
            <span>Download detailed PDF reports</span>
          </li>
          <li>
            <span class="check-icon">✅</span>
            <span>View Grad-CAM heatmap analysis</span>
          </li>
        </ul>
      </div>

      <!-- Right: Plans -->
      <div class="pricing-right">
        <div 
          v-for="plan in plans" 
          :key="plan.id" 
          class="plan-card" 
          :class="{ selected: selectedPlan === plan.id, popular: plan.popular }"
          @click="selectedPlan = plan.id"
        >
          <div class="plan-radio">
            <div class="radio-outer">
              <div class="radio-inner" v-if="selectedPlan === plan.id"></div>
            </div>
          </div>
          <div class="plan-info">
            <div class="plan-header">
              <h3 class="plan-name">{{ plan.name }}</h3>
              <span class="plan-price">{{ plan.price }}</span>
            </div>
            <p class="plan-desc">{{ plan.description }}</p>
            <span v-if="plan.popular" class="popular-badge">Most Popular</span>
          </div>
        </div>

        <button class="continue-btn" @click="handleContinue">
          Continue
        </button>

        <p class="disclaimer-text">
          This is a demo application for academic purposes. No real payment is processed.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'PricingPage',
  setup() {
    const router = useRouter()
    const selectedPlan = ref('starter')

    const plans = [
      {
        id: 'starter',
        name: '10-Analysis Bundle',
        price: 'Free',
        description: 'Get started — 10 free AI analyses per month.',
        popular: false
      },
      {
        id: 'pro-monthly',
        name: 'Pro Monthly',
        price: '$9.99/mo',
        description: 'Unlimited AI diagnoses, chat, and PDF reports.',
        popular: true
      },
      {
        id: 'pro-annual',
        name: 'Pro Annual',
        price: '$99.99/yr',
        description: 'Everything in Pro at $8.33/month. Billed yearly.',
        popular: false
      }
    ]

    const handleContinue = () => {
      if (selectedPlan.value === 'starter') {
        router.push('/')
      } else {
        alert(`You selected the "${plans.find(p => p.id === selectedPlan.value).name}" plan. Payment integration coming soon!`)
      }
    }

    return {
      selectedPlan,
      plans,
      handleContinue
    }
  }
}
</script>

<style scoped>
.pricing-container {
  flex: 1;
  min-height: calc(100vh - 100px);
  background: var(--bg-secondary, #f5f7fa);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  transition: background 0.3s ease;
}

.pricing-content {
  max-width: 1000px;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: start;
}

.back-link {
  display: inline-block;
  margin-bottom: 2rem;
  color: var(--text-color, #2d3436);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: var(--primary-color, #6c5ce7);
}

.pricing-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--text-color, #2d3436);
  margin-bottom: 0.5rem;
}

.pricing-subtitle {
  color: #636e72;
  font-size: 1.05rem;
  margin-bottom: 3rem;
  line-height: 1.6;
}

.feature-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.05rem;
  color: var(--text-color, #2d3436);
  font-weight: 500;
}

.check-icon {
  font-size: 1.2rem;
}

/* Right Column: Plans */
.pricing-right {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.plan-card {
  background: var(--card-bg, white);
  border: 2px solid var(--gray, #dfe6e9);
  border-radius: 14px;
  padding: 1.5rem 1.8rem;
  cursor: pointer;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  transition: all 0.3s ease;
  position: relative;
}

.plan-card:hover {
  border-color: var(--primary-color, #6c5ce7);
  box-shadow: 0 4px 16px rgba(108, 92, 231, 0.12);
}

.plan-card.selected {
  border-color: var(--primary-color, #6c5ce7);
  background: color-mix(in srgb, var(--primary-color, #6c5ce7) 5%, var(--card-bg, white));
  box-shadow: 0 4px 20px rgba(108, 92, 231, 0.15);
}

.plan-radio {
  padding-top: 2px;
}

.radio-outer {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 2px solid var(--gray, #dfe6e9);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color 0.3s ease;
}

.plan-card.selected .radio-outer {
  border-color: var(--primary-color, #6c5ce7);
}

.radio-inner {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--primary-color, #6c5ce7);
  animation: radioFadeIn 0.2s ease-out;
}

@keyframes radioFadeIn {
  from { transform: scale(0); }
  to { transform: scale(1); }
}

.plan-info {
  flex: 1;
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.3rem;
}

.plan-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-color, #2d3436);
  margin: 0;
}

.plan-price {
  font-size: 1.3rem;
  font-weight: 800;
  color: var(--text-color, #2d3436);
}

.plan-desc {
  color: #636e72;
  font-size: 0.9rem;
  margin: 0;
  line-height: 1.5;
}

.popular-badge {
  display: inline-block;
  margin-top: 0.5rem;
  padding: 0.2rem 0.7rem;
  background: linear-gradient(135deg, var(--primary-color, #6c5ce7), var(--primary-dark, #764ba2));
  color: white;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.continue-btn {
  width: 100%;
  padding: 1rem;
  margin-top: 0.5rem;
  background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 50%, #f093fb 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.15rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 0.5px;
}

.continue-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(108, 92, 231, 0.4);
}

.continue-btn:active {
  transform: translateY(0);
}

.disclaimer-text {
  text-align: center;
  color: #b2bec3;
  font-size: 0.8rem;
  margin-top: 0.8rem;
}

@media (max-width: 768px) {
  .pricing-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .pricing-title {
    font-size: 1.8rem;
  }

  .feature-list {
    gap: 1rem;
  }

  .plan-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.3rem;
  }
}
</style>
