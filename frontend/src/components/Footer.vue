<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <router-link to="/" class="logo">
            <div class="menu-icon">📊</div>
            <span>DiagnoBot</span>
          </router-link>
          <p class="brand-description">
            Empowering healthcare professionals with next-generation AI diagnostic tools for faster, more accurate patient care.
          </p>
          <div class="social-links">
            <a href="#" class="social-icon">𝕏</a>
            <a href="#" class="social-icon">in</a>
            <a href="#" class="social-icon">f</a>
          </div>
        </div>

        <div class="footer-links-group">
          <h4>Product</h4>
          <router-link to="/features" class="footer-link">Features</router-link>
          <router-link to="/pricing" class="footer-link">Pricing</router-link>
          <router-link to="/security" class="footer-link">Security</router-link>
          <router-link to="/updates" class="footer-link">Updates</router-link>
        </div>

        <div class="footer-links-group">
          <h4>Company</h4>
          <router-link to="/about" class="footer-link">About Us</router-link>
          <router-link to="/careers" class="footer-link">Careers</router-link>
          <router-link to="/contact" class="footer-link">Contact</router-link>
          <router-link to="/partners" class="footer-link">Partners</router-link>
        </div>

        <div class="footer-links-group">
          <h4>Legal</h4>
          <router-link to="/terms" class="footer-link">Terms of Service</router-link>
          <router-link to="/privacy" class="footer-link">Privacy Policy</router-link>
          <router-link to="/compliance" class="footer-link">HIPAA Compliance</router-link>
        </div>
      </div>

      <div class="footer-bottom">
        <p class="copyright">© 2026 DiagnoBot.ai. All rights reserved.</p>
        <div class="footer-bottom-links">
           <select class="language-selector" title="Select language">
            <option>English</option>
            <option>Español</option>
            <option>Français</option>
          </select>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.footer {
  background-color: var(--surface-color);
  padding: 6rem 0 2rem;
  border-top: 1px solid var(--border-color);
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 4rem;
  margin-bottom: 4rem;
}

.footer-brand {
  max-width: 300px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-main);
  text-decoration: none;
  margin-bottom: 1.5rem;
}

.menu-icon {
  width: 32px;
  height: 32px;
  background: var(--primary-color);
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
}

.brand-description {
  color: var(--text-muted);
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  text-decoration: none;
  transition: var(--transition);
}

.social-icon:hover {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

.footer-links-group h4 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 1.5rem;
}

.footer-link {
  display: block;
  color: var(--text-muted);
  text-decoration: none;
  margin-bottom: 1rem;
  font-size: 0.95rem;
  transition: var(--transition);
}

.footer-link:hover {
  color: var(--primary-color);
  transform: translateX(4px);
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 2rem;
  border-top: 1px solid var(--border-color);
}

.copyright {
  color: var(--text-muted);
  font-size: 0.875rem;
  margin: 0;
}

.language-selector {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  background: var(--bg-color);
  color: var(--text-main);
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  cursor: pointer;
  outline: none;
  transition: var(--transition);
}

.language-selector:focus {
  border-color: var(--primary-color);
}

@media (max-width: 1024px) {
  .footer-grid {
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
  }
}

@media (max-width: 600px) {
  .footer {
    padding: 4rem 0 2rem;
  }
  
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }
  
  .footer-bottom {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }
}
</style>
