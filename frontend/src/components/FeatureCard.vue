<template>
  <div class="card feature-card">
    <div class="feature-icon-wrapper">
      <span class="feature-icon">{{ icon }}</span>
    </div>
    <div class="feature-content">
      <h3 class="feature-title">{{ title }}</h3>
      <p class="feature-subtitle">{{ subtitle }}</p>
      <p class="feature-description">{{ description }}</p>
    </div>
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
  padding: 2.5rem 2rem;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.feature-icon-wrapper {
  width: 56px;
  height: 56px;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
  transition: var(--transition);
}

.feature-card:hover .feature-icon-wrapper {
  background: var(--primary-color);
  border-color: var(--primary-color);
  transform: scale(1.05) rotate(-5deg);
}

.feature-icon {
  font-size: 1.75rem;
  transition: var(--transition);
}

.feature-card:hover .feature-icon {
  filter: brightness(0) invert(1);
}

.feature-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.feature-title {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.feature-subtitle {
  color: var(--primary-color);
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.feature-description {
  color: var(--text-muted);
  font-size: 1rem;
  line-height: 1.6;
  margin: 0;
}
</style>
