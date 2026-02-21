<template>
  <section class="hero-section">
    <div class="hero-container container">
      <div class="hero-content">
        <div class="hero-badge fade-in">
          <span class="pulse-dot"></span>
          Next-Gen AI Healthcare
        </div>
        
        <h1 class="hero-title slide-in-left">
          Diagnose smarter with<br>
          <span class="text-gradient">Medical AI Assistant</span>
        </h1>
        
        <p class="hero-subtitle slide-in-left" style="animation-delay: 0.1s;">
          Empowering medical professionals with instant, highly accurate AI-driven insights for X-rays, MRIs, and CT Scans. Upload, analyze, and communicate seamlessly.
        </p>
        
        <div class="hero-cta btn-group slide-in-left" style="animation-delay: 0.2s;">
          <button @click="scrollToUpload" class="btn btn-primary btn-large">
            Get Started Free
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
          </button>
          <router-link to="/about" class="btn btn-secondary btn-large">
            How it works
          </router-link>
        </div>
        
        <div class="hero-stats fade-in" style="animation-delay: 0.4s;">
          <div class="stat-item">
            <span class="stat-value">99.8%</span>
            <span class="stat-label">Model Accuracy</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-value">&lt;2s</span>
            <span class="stat-label">Analysis Time</span>
          </div>
        </div>
      </div>
      
      <div class="hero-visual slide-in-right">
        <div class="visual-wrapper">
          <div class="floating-card card-1">
            <div class="icon-box warning">⚡</div>
            <div class="card-content">
              <h4>Processing Image</h4>
              <p>Analyzing X-Ray nodes...</p>
            </div>
          </div>
          <div class="floating-card card-2">
            <div class="icon-box success">✓</div>
            <div class="card-content">
              <h4>Analysis Complete</h4>
              <p>No anomalies detected</p>
            </div>
          </div>
          <!-- Abstract Background Graphic -->
          <div class="abstract-shape shape-1"></div>
          <div class="abstract-shape shape-2"></div>
          <div class="main-mockup">
            <img src="https://images.unsplash.com/photo-1666214276389-393fb7dbc75c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Doctor using advanced medical AI scanner interface" />
            <div class="mockup-overlay"></div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'HeroSection',
  methods: {
    scrollToUpload() {
      // Small emit hack. Given Vue structure, the parent (HomePage) manages scroll via ChatSection components
      this.$emit('scroll-to-chat');
      // If run independently via route, fallback
      const el = document.querySelector('.chat-section');
      if(el) el.scrollIntoView({ behavior: 'smooth' });
    }
  }
}
</script>

<style scoped>
.hero-section {
  padding: 8rem 0 6rem;
  background-color: var(--bg-color);
  position: relative;
  overflow: hidden;
}

/* Background grid pattern */
.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: radial-gradient(var(--border-color) 1px, transparent 1px);
  background-size: 32px 32px;
  opacity: 0.5;
  pointer-events: none;
  z-index: 0;
}

.hero-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  position: relative;
  z-index: 1;
}

.hero-content {
  max-width: 600px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-full);
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 2rem;
  box-shadow: var(--shadow-sm);
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background-color: var(--success-color);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.hero-title {
  font-size: clamp(3rem, 5vw, 4.5rem);
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.03em;
  margin-bottom: 1.5rem;
  color: var(--text-main);
}

.text-gradient {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  line-height: 1.6;
  color: var(--text-muted);
  margin-bottom: 2.5rem;
  max-width: 90%;
}

.hero-cta {
  margin-bottom: 3rem;
}

.hero-cta .btn {
  padding: 1rem 2rem;
}

.hero-stats {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border-color);
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-main);
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-muted);
}

.stat-divider {
  width: 1px;
  height: 40px;
  background-color: var(--border-color);
}

/* Visual Section */
.hero-visual {
  position: relative;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.visual-wrapper {
  position: relative;
  width: 100%;
  max-width: 500px;
  aspect-ratio: 4/5;
}

.abstract-shape {
  position: absolute;
  border-radius: var(--radius-full);
  filter: blur(60px);
  z-index: 0;
  opacity: 0.6;
}

.shape-1 {
  top: -10%;
  right: -10%;
  width: 300px;
  height: 300px;
  background: var(--primary-color);
  animation: float 6s ease-in-out infinite;
}

.shape-2 {
  bottom: -10%;
  left: -10%;
  width: 250px;
  height: 250px;
  background: var(--secondary-color);
  animation: float 8s ease-in-out infinite reverse;
}

.main-mockup {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-xl);
  z-index: 1;
  border: 4px solid var(--surface-color);
}

.main-mockup img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mockup-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(17, 24, 39, 0.8) 0%, transparent 60%);
}

.floating-card {
  position: absolute;
  background: var(--surface-color);
  padding: 1rem 1.5rem;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  display: flex;
  align-items: center;
  gap: 1rem;
  z-index: 2;
  min-width: 220px;
  border: 1px solid var(--border-color);
}

.floating-card.card-1 {
  top: 15%;
  left: -15%;
  animation: float 5s ease-in-out infinite;
}

.floating-card.card-2 {
  bottom: 20%;
  right: -20%;
  animation: float 7s ease-in-out infinite 1s;
}

.icon-box {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: bold;
}

.icon-box.warning {
  background: rgba(245, 158, 11, 0.1);
  color: var(--warning-color);
}

.icon-box.success {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success-color);
}

.card-content h4 {
  font-size: 0.875rem;
  margin: 0;
  color: var(--text-main);
  font-weight: 600;
}

.card-content p {
  font-size: 0.75rem;
  margin: 0;
  color: var(--text-muted);
}

@media (max-width: 1024px) {
  .hero-container {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 5rem;
  }
  
  .hero-content {
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .hero-subtitle {
    margin-left: auto;
    margin-right: auto;
  }
  
  .hero-stats {
    justify-content: center;
  }
  
  .floating-card.card-1 { left: -5%; }
  .floating-card.card-2 { right: -5%; }
}

@media (max-width: 600px) {
  .hero-section {
    padding: 4rem 0 3rem;
  }
  
  .hero-cta {
    flex-direction: column;
    width: 100%;
  }
  
  .hero-cta .btn {
    width: 100%;
  }
  
  .floating-card {
    display: none;
  }
  
  .visual-wrapper {
    max-width: 320px;
  }
}
</style>
