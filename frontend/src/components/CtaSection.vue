<template>
  <section class="cta-section section">
    <div class="container">
      <div class="cta-box card fade-in">
        <div class="cta-content">
          <h2 class="cta-title">Ready to transform your diagnostics?</h2>
          <p class="cta-subtitle">Join the growing community of healthcare professionals using our AI assistant to deliver faster, more accurate patient care.</p>
          
          <div class="btn-group cta-buttons">
            <button @click="$emit('scroll-to-chat')" class="btn btn-primary btn-large">
              Start Free Trial
            </button>
            <router-link to="/pricing" class="btn btn-secondary btn-large" style="background: rgba(255,255,255,0.1); color: white; border-color: rgba(255,255,255,0.2);">
              View Pricing
            </router-link>
          </div>
        </div>
        
        <!-- Background graphics -->
        <div class="cta-bg-shape shape-1"></div>
        <div class="cta-bg-shape shape-2"></div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'CtaSection'
}
</script>

<style scoped>
.cta-section {
  padding: 4rem 0 8rem 0;
  background-color: var(--bg-color);
}

.cta-box {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
  color: white;
  text-align: center;
  padding: 5rem 2rem;
  overflow: hidden;
  border-radius: var(--radius-lg);
  border: none;
  box-shadow: 0 20px 40px -10px rgba(79, 70, 229, 0.4);
}

.cta-box::before {
  display: none; /* Override standard card ::before */
}

.cta-box:hover {
  transform: translateY(-4px);
  box-shadow: 0 30px 50px -10px rgba(79, 70, 229, 0.5);
}

.cta-content {
  position: relative;
  z-index: 2;
  max-width: 700px;
  margin: 0 auto;
}

.cta-title {
  color: white;
  font-size: clamp(2rem, 4vw, 3rem);
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
}

.cta-subtitle {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.125rem;
  margin-bottom: 3rem;
}

.cta-buttons {
  justify-content: center;
}

.cta-buttons .btn-primary {
  background: white;
  color: var(--primary-dark);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.cta-buttons .btn-primary:hover {
  background: var(--surface-color);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

/* Background graphics */
.cta-bg-shape {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
  z-index: 1;
}

.shape-1 {
  width: 400px;
  height: 400px;
  top: -200px;
  left: -100px;
}

.shape-2 {
  width: 500px;
  height: 500px;
  bottom: -250px;
  right: -100px;
}

@media (max-width: 600px) {
  .cta-box {
    padding: 3rem 1.5rem;
  }
  
  .cta-buttons {
    flex-direction: column;
    width: 100%;
  }
  
  .cta-buttons .btn {
    width: 100%;
  }
}
</style>
