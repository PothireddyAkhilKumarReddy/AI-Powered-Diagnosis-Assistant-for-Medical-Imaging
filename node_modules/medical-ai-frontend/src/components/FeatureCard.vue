<template>
  <div class="feature-card">
    <div class="feature-icon">{{ icon }}</div>
    <h3 class="feature-title">{{ title }}</h3>
    <p class="feature-subtitle">{{ subtitle }}</p>
    <p class="feature-description">{{ description }}</p>
  </div>
</template>

<script>
export default {
  name: 'FeatureCard',
  props: {
    icon: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    subtitle: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-title {
  font-size: 1.3rem;
  font-weight: bold;
  margin: 0.5rem 0;
  color: #333;
}

.feature-subtitle {
  color: #6c5ce7;
  margin: 0.5rem 0;
  font-weight: 600;
}

.feature-description {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 1rem 0 0 0;
}
</style>
