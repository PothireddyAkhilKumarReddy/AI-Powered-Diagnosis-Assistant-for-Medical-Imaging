<template>
  <div class="about-container">
    <div class="about-content">
      <router-link to="/" class="back-link">← Get Back</router-link>

      <h1 class="about-title">About Us</h1>
      
      <div class="about-section">
        <p class="about-text">
          We are a team of engineers, data scientists, and medical professionals, united by a common goal: 
          to make healthcare accessible in every corner of the world. Our mission is to create a medical AI 
          assistant that delivers analysis with the accuracy and care of a qualified doctor — available 24/7, 
          no matter where you live.
        </p>
      </div>

      <div class="divider"></div>

      <div class="about-section">
        <p class="about-text">
          Our journey combines pioneering advancements in deep learning with real-world medical expertise. 
          DiagnoBot uses a DenseNet121 neural network trained on thousands of chest X-rays to detect 
          COVID-19, Pneumonia, and Normal conditions. Combined with Google's Gemini AI for natural language 
          understanding, we offer both image-based diagnosis and intelligent health conversations.
        </p>
      </div>

      <div class="divider"></div>

      <!-- How It Works -->
      <h2 class="section-title">How It Works</h2>
      <div class="steps-grid">
        <div class="step-card">
          <div class="step-number">1</div>
          <h3>Upload Your X-Ray</h3>
          <p>Drag & drop or click to upload a chest X-ray image (JPG, PNG, or GIF format).</p>
        </div>
        <div class="step-card">
          <div class="step-number">2</div>
          <h3>AI Analyzes the Image</h3>
          <p>Our DenseNet121 model processes the image and generates a diagnosis with confidence scores.</p>
        </div>
        <div class="step-card">
          <div class="step-number">3</div>
          <h3>View Heatmap & Report</h3>
          <p>See which regions the AI focused on with Grad-CAM heatmaps. Download a PDF report.</p>
        </div>
        <div class="step-card">
          <div class="step-number">4</div>
          <h3>Chat with DiagnoBot</h3>
          <p>Ask follow-up questions about your results, symptoms, or treatment options.</p>
        </div>
      </div>

      <div class="divider"></div>

      <!-- FAQ -->
      <h2 id="faq" class="section-title">Frequently Asked Questions</h2>
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

      <div class="divider"></div>

      <!-- Contact -->
      <h2 class="section-title">Our Contacts</h2>
      <div class="contact-info">
        <p><strong>DiagnoBot AI</strong></p>
        <p>📧 support@diagnobot.ai</p>
        <p>🌐 diagnobot.ai</p>
        <p class="contact-note">Academic Research Project — Chest X-Ray Classification using Deep Learning</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'AboutPage',
  setup() {
    const openFaq = ref(null)

    const faqs = [
      {
        question: 'Is DiagnoBot a replacement for a real doctor?',
        answer: 'No. DiagnoBot is an AI-assisted analysis tool for informational purposes only. Always consult a qualified healthcare provider for medical diagnosis and treatment.'
      },
      {
        question: 'What types of images can I upload?',
        answer: 'DiagnoBot is trained on chest X-ray images and can classify them as COVID-19, Pneumonia, or Normal. For best results, upload standard frontal chest X-rays in JPG or PNG format.'
      },
      {
        question: 'How accurate is the AI diagnosis?',
        answer: 'Our DenseNet121 model achieves high accuracy on the COVID-19 Radiography Dataset. However, AI predictions should always be verified by a medical professional. Confidence scores are provided with every prediction.'
      },
      {
        question: 'What is the Grad-CAM heatmap?',
        answer: 'Grad-CAM (Gradient-weighted Class Activation Mapping) is a visualization technique that highlights which regions of the X-ray the AI focused on when making its prediction. This helps interpret and validate AI decisions.'
      },
      {
        question: 'Is my data secure?',
        answer: 'Uploaded images are processed in real-time and immediately deleted after analysis. We do not store any medical images on our servers. Chat conversations are not saved on the server either.'
      },
      {
        question: 'Can I download a report of my analysis?',
        answer: 'Yes! After each analysis, you can download a structured PDF report containing the prediction, confidence breakdown, and disclaimer — all ready to share with your healthcare provider.'
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
.about-container {
  flex: 1;
  min-height: calc(100vh - 100px);
  background: var(--bg-secondary, #f5f7fa);
  padding: 3rem 2rem;
  transition: background 0.3s ease;
}

.about-content {
  max-width: 900px;
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

.about-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--text-color, #2d3436);
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-color, #2d3436);
  margin-bottom: 1.5rem;
}

.about-section {
  margin-bottom: 1.5rem;
}

.about-text {
  font-size: 1.05rem;
  line-height: 1.8;
  color: var(--text-color, #2d3436);
  opacity: 0.85;
}

.divider {
  border: none;
  border-top: 2px dashed var(--gray, #dfe6e9);
  margin: 2.5rem 0;
}

/* How It Works Steps */
.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.step-card {
  background: var(--card-bg, white);
  border-radius: 14px;
  padding: 2rem 1.5rem;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  text-align: center;
}

.step-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-md);
}

.step-number {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--primary-color, #6c5ce7), var(--primary-dark, #764ba2));
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  font-weight: 800;
  margin: 0 auto 1rem;
}

.step-card h3 {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-color, #2d3436);
  margin-bottom: 0.5rem;
}

.step-card p {
  font-size: 0.9rem;
  color: #636e72;
  line-height: 1.5;
}

/* FAQ */
.faq-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.faq-item {
  background: var(--card-bg, white);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.faq-item:hover {
  box-shadow: var(--shadow-md);
}

.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 1.5rem;
  font-weight: 600;
  font-size: 1rem;
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
  padding: 0 1.5rem 1.2rem;
}

.faq-answer p {
  color: #636e72;
  line-height: 1.7;
  font-size: 0.95rem;
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

/* Contact */
.contact-info {
  background: var(--card-bg, white);
  border-radius: 14px;
  padding: 2rem;
  box-shadow: var(--shadow-sm);
}

.contact-info p {
  color: var(--text-color, #2d3436);
  font-size: 1rem;
  line-height: 1.8;
  margin: 0;
}

.contact-note {
  margin-top: 1rem !important;
  font-size: 0.85rem !important;
  color: #636e72 !important;
  font-style: italic;
}

@media (max-width: 768px) {
  .about-title {
    font-size: 1.8rem;
  }

  .steps-grid {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
