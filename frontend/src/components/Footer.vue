<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-left">
        © 2026 DiagnoBot.ai All Rights Reserved.
      </div>
      <div class="footer-center">
        <select class="language-selector" title="Select language">
          <option>Eng</option>
          <option>Esp</option>
          <option>Fra</option>
        </select>
      </div>
      <div class="footer-right">
        <router-link to="/" class="footer-link">Homepage</router-link>
        <router-link to="/about" class="footer-link">About Us</router-link>
        <router-link to="/pricing" class="footer-link">Pricing</router-link>
        <router-link to="/terms" class="footer-link">Terms of Use</router-link>
        <router-link to="/terms" class="footer-link">Privacy Policy</router-link>
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
  background: #2d3436;
  color: white;
  padding: 2rem;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 2rem;
}

.footer-left {
  flex: 1;
  min-width: 200px;
  font-size: 0.9rem;
}

.footer-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.language-selector {
  padding: 0.5rem;
  border: 1px solid #555;
  background: #363d41;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.footer-right {
  flex: 1;
  display: flex;
  gap: 1.5rem;
  justify-content: flex-end;
  flex-wrap: wrap;
  row-gap: 0.8rem;
}

.footer-link {
  color: #dfe6e9;
  text-decoration: none;
  transition: color 0.3s ease;
  font-size: 0.9rem;
  white-space: nowrap;
}

.footer-link:hover {
  color: #a29bfe;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    text-align: center;
  }

  .footer-center {
    justify-content: center;
  }

  .footer-right {
    justify-content: center;
  }
}
</style>
