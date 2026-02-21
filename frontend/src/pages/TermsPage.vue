<template>
  <div class="legal-container">
    <div class="legal-content">
      <router-link to="/" class="back-link">← Get Back</router-link>

      <h1 class="legal-title">Terms of Use</h1>
      <p class="legal-updated">Last Updated: February 2026</p>

      <div class="legal-body">
        <h2>1. Acceptance of Terms</h2>
        <p>
          By accessing and using DiagnoBot, you agree to be bound by these Terms of Use. If you do not agree to these terms, please do not use the service.
        </p>

        <h2>2. Medical Disclaimer</h2>
        <p>
          <strong>DiagnoBot is for informational and educational purposes only.</strong> It is an academic project and should <em>not</em> be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read on DiagnoBot.
        </p>

        <h2>3. Use of AI and Accuracy</h2>
        <p>
          DiagnoBot utilizes artificial intelligence (DenseNet121 and Google Gemini AI) to analyze images and provide information. While we strive for accuracy, AI models can make mistakes. The prediction confidence scores and heatmaps are algorithmic outputs and not absolute truths. We do not guarantee the accuracy, completeness, or usefulness of the analysis.
        </p>

        <h2>4. Data Privacy</h2>
        <p>
          We respect your privacy. Uploaded medical images are processed temporarily for analysis and are deleted immediately after the session. We do not perpetually store your X-ray images. Please review our Privacy Policy for more detailed information.
        </p>

        <h2>5. Limitation of Liability</h2>
        <p>
          In no event shall DiagnoBot, its creators, or affiliated institutions be liable for any direct, indirect, incidental, special, consequential, or exemplary damages arising out of or in connection with your use or inability to use the platform.
        </p>

        <h2>6. Changes to Terms</h2>
        <p>
          We reserve the right to modify these terms at any time. We will indicate that changes have been made by updating the "Last Updated" date at the top of this document. Your continued use of the platform after changes have been made constitutes your acceptance of the new terms.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TermsPage'
}
</script>

<style scoped>
.legal-container {
  flex: 1;
  min-height: calc(100vh - 100px);
  background: var(--bg-secondary, #f5f7fa);
  padding: 3rem 2rem;
  transition: background 0.3s ease;
}

.legal-content {
  max-width: 800px;
  margin: 0 auto;
  background: var(--card-bg, white);
  padding: 3rem;
  border-radius: 14px;
  box-shadow: var(--shadow-sm);
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

.legal-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--text-color, #2d3436);
  margin-bottom: 0.5rem;
}

.legal-updated {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-bottom: 2.5rem;
  font-style: italic;
}

.legal-body h2 {
  font-size: 1.3rem;
  color: var(--text-color, #2d3436);
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.legal-body p {
  line-height: 1.7;
  color: var(--text-muted);
  margin-bottom: 1.5rem;
  font-size: 1.05rem;
}

html[data-theme='dark'] .legal-body p {
  color: var(--text-muted);
}

@media (max-width: 768px) {
  .legal-content {
    padding: 2rem 1.5rem;
  }
  
  .legal-title {
    font-size: 2rem;
  }
}
</style>
