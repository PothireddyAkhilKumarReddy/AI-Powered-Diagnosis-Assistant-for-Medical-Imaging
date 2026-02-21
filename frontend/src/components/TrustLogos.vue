<template>
  <section class="trust-section">
    <div class="container text-center">
      <p class="trust-title fade-in">Trusted by modern healthcare providers globally</p>
      
      <div class="logo-marquee fade-in" style="animation-delay: 0.2s;">
        <div class="marquee-content">
          <div class="logo-item" v-for="i in 2" :key="i">
            <span class="company-logo">MedCorp</span>
            <span class="company-logo" style="font-weight: 800;">Health<span style="color:var(--primary-color)">Sync</span></span>
            <span class="company-logo">Radiology<span style="font-weight: 300;">AI</span></span>
            <span class="company-logo">Clinic<span style="color:var(--secondary-color)">Os</span></span>
            <span class="company-logo" style="letter-spacing: 2px;">VITALITY</span>
            <span class="company-logo">Neuro<span style="font-weight: 700;">Diagnostics</span></span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'TrustLogos'
}
</script>

<style scoped>
.trust-section {
  padding: 4rem 0;
  background-color: var(--surface-color);
  border-bottom: 1px solid var(--border-color);
  overflow: hidden;
}

.trust-title {
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  margin-bottom: 2rem;
}

.logo-marquee {
  position: relative;
  width: 100%;
  overflow: hidden;
}

.logo-marquee::before,
.logo-marquee::after {
  content: '';
  position: absolute;
  top: 0;
  width: 15%;
  height: 100%;
  z-index: 2;
  pointer-events: none;
}

.logo-marquee::before {
  left: 0;
  background: linear-gradient(to right, var(--surface-color), transparent);
}

.logo-marquee::after {
  right: 0;
  background: linear-gradient(to left, var(--surface-color), transparent);
}

.marquee-content {
  display: flex;
  width: fit-content;
  animation: scroll 30s linear infinite;
}

.logo-item {
  display: flex;
  align-items: center;
  gap: 4rem;
  padding-right: 4rem;
}

.company-logo {
  font-size: 1.5rem;
  color: var(--text-muted);
  font-weight: 500;
  opacity: 0.6;
  transition: var(--transition);
  cursor: default;
  white-space: nowrap;
}

.company-logo:hover {
  opacity: 1;
  color: var(--text-main);
  transform: scale(1.05);
}

@keyframes scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

@media (max-width: 768px) {
  .logo-item {
    gap: 2.5rem;
    padding-right: 2.5rem;
  }
  
  .company-logo {
    font-size: 1.25rem;
  }
}
</style>
