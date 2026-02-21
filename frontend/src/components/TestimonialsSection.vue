<template>
  <section class="testimonials-section section">
    <div class="container">
      <div class="section-header text-center fade-in">
        <div class="badge badge-primary mb-2">Trusted Reviews</div>
        <h2>What medical professionals say</h2>
        <p class="text-muted" style="max-width: 600px; margin: 0 auto;">Join thousands of doctors, radiologists, and clinics who rely on our AI assistant daily.</p>
      </div>

      <div class="testimonials-grid">
        <div class="testimonial-card card fade-in" style="animation-delay: 0.1s">
          <div class="quote-icon">"</div>
          <div class="rating">
            <span v-for="i in 5" :key="i">★</span>
          </div>
          <p class="testimonial-text">
            "This AI tool has completely transformed our clinic's workflow. The accuracy in detecting early signs of anomalies in chest X-Rays has saved countless hours for our radiology department."
          </p>
          <div class="testimonial-author">
            <img src="https://images.unsplash.com/photo-1559839734-2b71ea197ec2?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80" alt="Dr. Sarah Jenkins" class="author-avatar" />
            <div class="author-info">
              <h4>Dr. Sarah Jenkins</h4>
              <span>Chief Radiologist, Metro Health</span>
            </div>
          </div>
        </div>

        <div class="testimonial-card card fade-in" style="animation-delay: 0.2s">
          <div class="quote-icon">"</div>
          <div class="rating">
            <span v-for="i in 5" :key="i">★</span>
          </div>
          <p class="testimonial-text">
            "I use the assistant as a reliable second opinion. The speed at which it processes complex MRIs and highlights areas of concern is nothing short of remarkable. It's an indispensable tool."
          </p>
          <div class="testimonial-author">
            <img src="https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80" alt="Dr. Michael Chang" class="author-avatar" />
            <div class="author-info">
              <h4>Dr. Michael Chang</h4>
              <span>Neurologist, Pacific Clinic</span>
            </div>
          </div>
        </div>

        <div class="testimonial-card card fade-in" style="animation-delay: 0.3s">
          <div class="quote-icon">"</div>
          <div class="rating">
            <span v-for="i in 5" :key="i">★</span>
          </div>
          <p class="testimonial-text">
            "Our diagnostic accuracy has improved by over 15% since integrating this platform. It catches subtle patterns that are incredibly easy to miss during a busy shift. Highly recommended."
          </p>
          <div class="testimonial-author">
            <img src="https://images.unsplash.com/photo-1594824432258-f4ee0b93808a?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80" alt="Dr. Elena Rodriguez" class="author-avatar" />
            <div class="author-info">
              <h4>Dr. Elena Rodriguez</h4>
              <span>ER Physician, City Hospital</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'TestimonialsSection'
}
</script>

<style scoped>
.testimonials-section {
  background-color: var(--bg-color);
  position: relative;
  overflow: hidden;
}

/* Background blob */
.testimonials-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 1000px;
  height: 500px;
  background: radial-gradient(ellipse, rgba(79, 70, 229, 0.05) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
}

.section-header {
  margin-bottom: 4rem;
  position: relative;
  z-index: 1;
}

.badge-primary {
  background: rgba(79, 70, 229, 0.1);
  color: var(--primary-color);
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  position: relative;
  z-index: 1;
}

.testimonial-card {
  padding: 2.5rem 2rem;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.quote-icon {
  font-size: 4rem;
  line-height: 1;
  color: var(--border-color);
  font-family: serif;
  margin-bottom: -1rem;
}

.rating {
  color: #fbbf24;
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
  letter-spacing: 2px;
}

.testimonial-text {
  font-size: 1rem;
  line-height: 1.7;
  color: var(--text-main);
  flex: 1;
  margin-bottom: 2rem;
  font-style: italic;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 1rem;
  border-top: 1px solid var(--border-color);
  padding-top: 1.5rem;
}

.author-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--surface-color);
  box-shadow: var(--shadow-sm);
}

.author-info h4 {
  font-size: 1rem;
  margin: 0 0 0.25rem 0;
  color: var(--text-main);
}

.author-info span {
  font-size: 0.875rem;
  color: var(--text-muted);
}

@media (max-width: 768px) {
  .section-header {
    margin-bottom: 3rem;
  }
}
</style>
