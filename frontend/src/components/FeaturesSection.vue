<template>
  <section class="features-section section">
    <div class="container">
      <div class="section-header text-center fade-in">
        <div class="badge badge-success mb-2">Capabilities</div>
        <h2>Unlock the Power of Medical AI</h2>
        <p class="text-muted" style="max-width: 600px; margin: 0 auto;">Our advanced algorithms provide unparalleled accuracy, helping you diagnose faster and with greater confidence.</p>
      </div>

      <div class="features-grid">
        <FeatureCard class="fade-in" style="animation-delay: 0.1s"
          icon="⚡"
          title="Instant Processing"
          subtitle="Real-time Analysis"
          description="Skip the wait for appointments. Our AI health assistance offers instant, accurate symptom checking and evaluations within seconds of uploading your scans."
        />

        <FeatureCard class="fade-in" style="animation-delay: 0.2s"
          icon="🩺"
          title="Doctor Validated"
          subtitle="Clinical Accuracy"
          description="Powered by LLMs fine-tuned on diverse medical data. Every recommendation, treatment plan, and anomaly detection is rigorously validated by medical professionals."
        />

        <FeatureCard class="fade-in" style="animation-delay: 0.3s"
          icon="🛡️"
          title="Second Opinion"
          subtitle="Reliable Insights"
          description="Save time and mitigate high medical bills. Whether you are a patient seeking clarity or a doctor needing a secondary confirmation, our AI provides clear, backed insights."
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
  background-color: var(--bg-color);
  position: relative;
  overflow: hidden;
}

.section-header {
  margin-bottom: 4rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2.5rem;
}

@media (max-width: 768px) {
  .section-header {
    margin-bottom: 3rem;
  }
  
  .features-grid {
    gap: 1.5rem;
  }
}
</style>
