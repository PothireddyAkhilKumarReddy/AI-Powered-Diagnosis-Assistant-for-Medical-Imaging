<template>
  <div class="faq-container">
    <div class="faq-content">
      <router-link to="/" class="back-link">← Get Back</router-link>

      <h1 class="faq-title">Frequently Asked Questions</h1>
      <p class="faq-subtitle">Everything you need to know about DiagnoBot and how it works.</p>

      <div class="faq-list">
        <div v-for="(faq, index) in faqs" :key="index" class="faq-item" @click="toggleFaq(index)">
          <div class="faq-question">
            <span>{{ faq.question }}</span>
            <span class="faq-icon">{{ openFaq === index ? '−' : '+' }}</span>
          </div>
          <transition name="faq-slide">
            <div class="faq-answer" v-if="openFaq === index">
              <p>{{ faq.answer }}</p>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'FaqPage',
  setup() {
    const openFaq = ref(0) // Open the first FAQ by default

    const faqs = [
      {
        question: 'Is DiagnoBot a replacement for a real doctor?',
        answer: 'No. DiagnoBot is an AI-assisted analysis tool for informational purposes only. Always consult a qualified healthcare provider for medical diagnosis and treatment.'
      },
      {
        question: 'What types of images can I upload?',
        answer: 'DiagnoBot is trained on chest X-ray images and can classify them as COVID-19, Pneumonia, Tuberculosis (TB), or Normal. For best results, upload standard frontal chest X-rays in JPG, PNG, or GIF format.'
      },
      {
        question: 'How accurate is the AI diagnosis?',
        answer: 'Our DenseNet121 model achieves high accuracy on the COVID-19 Radiography Dataset. However, AI predictions should always be verified by a medical professional. Confidence scores are provided with every prediction to show the model\'s certainty.'
      },
      {
        question: 'What is the Grad-CAM heatmap?',
        answer: 'Grad-CAM (Gradient-weighted Class Activation Mapping) is a visualization technique that highlights which regions of the X-ray the AI focused on when making its prediction. Red/yellow areas indicate high focus, while blue regions indicate low focus. This helps interpret and validate AI decisions.'
      },
      {
        question: 'Is my data secure?',
        answer: 'Yes. Uploaded images are processed in real-time and immediately deleted from active memory after the analysis is complete. We do not store any medical images permanently on our servers. Your chat conversations are completely private.'
      },
      {
        question: 'Can I download a report of my analysis?',
        answer: 'Yes! After each analysis, you can download a structured PDF report containing the prediction, confidence breakdown, and a medical disclaimer — ready to share with your healthcare provider.'
      },
      {
        question: 'How does the chat feature work?',
        answer: 'Our intelligent chat feature uses Google\'s Gemini AI. You can ask follow-up questions about your diagnosis, general medical symptoms, or preventative care. The AI acts as a knowledgeable medical assistant to help answer your questions.'
      },
      {
        question: 'What are the free and pro plans?',
        answer: 'You can see full details on our Pricing page. We offer a free starter bundle of 10 analyses, and a Pro subscription that provides unlimited analysis, PDF reports, and chat.'
      }
    ]

    const toggleFaq = (index) => {
      openFaq.value = openFaq.value === index ? null : index
    }

    return { faqs, openFaq, toggleFaq }
  }
}
</script>

<style scoped>
.faq-container {
  flex: 1;
  min-height: calc(100vh - 100px);
  background: var(--bg-secondary, #f5f7fa);
  padding: 3rem 2rem;
  transition: background 0.3s ease;
}

.faq-content {
  max-width: 800px;
  margin: 0 auto;
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

.faq-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--text-color, #2d3436);
  margin-bottom: 0.5rem;
}

.faq-subtitle {
  color: #636e72;
  font-size: 1.1rem;
  margin-bottom: 3rem;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.faq-item {
  background: var(--card-bg, white);
  border: 1px solid var(--gray, #dfe6e9);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.faq-item:hover {
  border-color: var(--primary-color, #6c5ce7);
  box-shadow: 0 4px 12px rgba(108, 92, 231, 0.08);
}

.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  font-weight: 600;
  font-size: 1.05rem;
  color: var(--text-color, #2d3436);
}

.faq-icon {
  font-size: 1.5rem;
  font-weight: 300;
  color: var(--primary-color, #6c5ce7);
  flex-shrink: 0;
  margin-left: 1rem;
}

.faq-answer {
  padding: 0 1.5rem 1.5rem;
}

.faq-answer p {
  color: #636e72;
  line-height: 1.7;
  font-size: 0.95rem;
  margin: 0;
}

.faq-slide-enter-active,
.faq-slide-leave-active {
  transition: all 0.3s ease;
  max-height: 200px;
}

.faq-slide-enter-from,
.faq-slide-leave-to {
  opacity: 0;
  max-height: 0;
  padding-bottom: 0;
}

@media (max-width: 768px) {
  .faq-title {
    font-size: 2rem;
  }
}
</style>
