<template>
  <section class="features-section">
    <div class="features-container">
      <div class="features-grid">
        <FeatureCard
          icon="🌱"
          title="Revolutionary Product"
          subtitle="Your Personal AI Health Assistant, 24/7."
          description="Skip the wait for appointments and stop searching symptoms online. Our AI health assistance chat offers instant, accurate symptom checking, personalized recommendations for medical tests, and detailed treatment plans – all created and validated by our team of experienced doctors and engineers."
        />

        <FeatureCard
          icon="💬"
          title="AI Validated by Doctors"
          subtitle="Machine Learning Meets Medicine."
          description="Our chatbot uses LLMs fine-tuned on real medical data, patient-doctor conversations, and medical protocols. Our custom-built AI system understands your symptoms and provides accurate, up-to-date medical advice. Every recommendation, treatment plan, and test is validated by medical professionals."
        />

        <FeatureCard
          icon="💎"
          title="The Value you Get"
          subtitle="Get an AI-Backed Second Opinion."
          description="With our health assistant, you save both time and money. Avoid unnecessary doctor visits and high medical bills by getting answers to your health questions immediately. Not sure about a diagnosis or treatment plan? Use our AI health chat to get a second opinion."
        />
      </div>
    </div>
  </section>
</template>

<script>
import FeatureCard from './FeatureCard.vue'

export default {
  name: 'FeaturesSection',
  components: {
    FeatureCard
  }
}
</script>

<style scoped>
.features-section {
  padding: 4rem 2rem;
  background: #f8f9fa;
}

.features-container {
  max-width: 1200px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

@media (max-width: 768px) {
  .features-section {
    padding: 2rem 1rem;
  }

  .features-grid {
    gap: 1.5rem;
  }
}
</style>
