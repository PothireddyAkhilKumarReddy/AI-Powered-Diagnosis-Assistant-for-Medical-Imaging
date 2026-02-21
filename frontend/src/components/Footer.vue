<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-left">
        © 2025 DiagnoBot.ai All Rights Reserved.
      </div>
      <div class="footer-center">
        <select class="language-selector" title="Select language">
          <option>Eng</option>
          <option>Esp</option>
          <option>Fra</option>
        </select>
      </div>
      <div class="footer-right">
        <a href="#" class="footer-link">Homepage</a>
        <a href="#" class="footer-link">About Us</a>
        <a href="#" class="footer-link">Terms of Use</a>
        <a href="#" class="footer-link">Privacy Policy</a>
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
}

.footer-link {
  color: #dfe6e9;
  text-decoration: none;
  transition: color 0.3s ease;
  font-size: 0.9rem;
}

.footer-link:hover {
  color: #6c5ce7;
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
