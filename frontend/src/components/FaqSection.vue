<template>
  <section class="faq-section section">
    <div class="container">
      <div class="faq-layout fade-in">
        <div class="faq-header">
          <div class="badge badge-warning mb-2">Common Questions</div>
          <h2>Frequently Asked Questions</h2>
          <p class="text-muted mb-4">Everything you need to know about our Medical AI diagnostic tools.</p>
          <router-link to="/about" class="btn btn-primary">Find more answers</router-link>
        </div>

        <div class="faq-list">
          <div 
            v-for="(faq, index) in faqs" 
            :key="index"
            class="faq-item"
            :class="{ active: activeIndex === index }"
          >
            <button class="faq-question" @click="toggleFaq(index)">
              <span>{{ faq.question }}</span>
              <div class="faq-icon-wrapper">
                <span v-if="activeIndex === index" class="icon-minus">−</span>
                <span v-else class="icon-plus">+</span>
              </div>
            </button>
            <div 
              class="faq-answer-wrapper"
              :style="{ height: activeIndex === index ? 'auto' : '0' }"
            >
              <p class="faq-answer">
                {{ faq.answer }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'FaqSection',
  data() {
    return {
      activeIndex: 0,
      faqs: [
        {
          question: 'How accurate is the AI diagnostic tool?',
          answer: 'Our AI model has been trained on over 5 million peer-reviewed medical images and achieves a 99.8% accuracy rate in detecting common anomalies like fractures, pneumonia, and tumors, performing on par with leading human radiologists.'
        },
        {
          question: 'Is my patients\' data secure and HIPAA compliant?',
          answer: 'Yes. We employ end-to-end encryption and strict data anonymization protocols. No personal patient data is stored permanently on our servers after the analysis is complete, ensuring full HIPAA and GDPR compliance.'
        },
        {
          question: 'Can this replace a human doctor or radiologist?',
          answer: 'No. Our AI is designed as a powerful assistive tool for medical professionals, not a replacement. It acts as a highly accurate second opinion to reduce human error, speed up workflows, and prioritize critical cases.'
        },
        {
          question: 'What types of imaging does DiagnoBot support?',
          answer: 'Currently, the system fully supports chest and bone X-rays, Brain MRIs, and lung CT scans. We are constantly expanding our models to cover additional modalities.'
        },
        {
          question: 'How fast will I receive the analysis results?',
          answer: 'Analysis is nearly instantaneous. Once an image is uploaded and processed, the detailed diagnostic report and highlighted anomaly map are generated in under 2 seconds.'
        }
      ]
    }
  },
  methods: {
    toggleFaq(index) {
      if (this.activeIndex === index) {
        this.activeIndex = null;
      } else {
        this.activeIndex = index;
      }
    }
  }
}
</script>

<style scoped>
.faq-section {
  background-color: var(--surface-color);
  padding: 8rem 0;
  border-top: 1px solid var(--border-color);
}

.faq-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6rem;
  align-items: start;
}

.faq-header {
  position: sticky;
  top: 120px;
}

.faq-header h2 {
  font-size: clamp(2rem, 4vw, 3rem);
  margin-bottom: 1rem;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.faq-item {
  border-radius: var(--radius-md);
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  overflow: hidden;
  transition: var(--transition);
}

.faq-item:hover, .faq-item.active {
  border-color: var(--primary-color);
  box-shadow: var(--shadow-sm);
}

.faq-question {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: none;
  border: none;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-main);
  text-align: left;
  cursor: pointer;
  outline: none;
  gap: 1.5rem;
}

.faq-icon-wrapper {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-color);
  font-size: 1.25rem;
  font-weight: 400;
  transition: var(--transition);
}

.faq-item.active .faq-icon-wrapper {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.faq-answer-wrapper {
  overflow: hidden;
  transition: height 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.faq-answer {
  padding: 0 2rem 1.5rem 2rem;
  color: var(--text-muted);
  font-size: 1rem;
  line-height: 1.6;
  margin: 0;
}

@media (max-width: 900px) {
  .faq-layout {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
  
  .faq-header {
    position: static;
    text-align: center;
  }
  
  .faq-header p {
    margin: 0 auto 1.5rem auto;
  }
}
</style>
