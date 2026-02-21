<template>
  <section class="cta-section">
    <h2 class="cta-title">Try AI Health Chat Now</h2>
    <button class="cta-button" @click="$emit('scroll-to-chat')">Upgrade Your Plan</button>
  </section>
</template>

<script>
export default {
  name: 'CtaSection'
}
</script>

<style scoped>
.cta-section {
  padding: 3rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
}

.cta-title {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  font-weight: bold;
}

.cta-button {
  padding: 0.8rem 2rem;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cta-button:hover {
  transform: scale(1.05);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}
</style>
