<template>
  <section class="hero-section">
    <h1 class="hero-title">
      Welcome to<br>
      <span>your AI Health Chat</span>
    </h1>
  </section>
</template>

<script>
export default {
  name: 'HeroSection'
}
</script>

<style scoped>
.hero-section {
  padding: 4rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-title {
  font-size: 3rem;
  font-weight: bold;
  line-height: 1.2;
  margin: 0;
}

.hero-title span {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

@media (max-width: 768px) {
  .hero-section {
    padding: 2rem 1rem;
    min-height: 300px;
  }

  .hero-title {
    font-size: 2rem;
  }
}
</style>
