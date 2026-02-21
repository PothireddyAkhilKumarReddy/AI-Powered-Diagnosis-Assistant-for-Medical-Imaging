<template>
  <header class="header">
    <div class="logo">
      <div class="menu-icon">☰</div>
      <span>DiagnoBot</span>
    </div>
    <div class="auth-buttons">
      <button class="btn btn-outline">Sign Up</button>
      <button class="btn btn-primary">Log In</button>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header'
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.5rem;
  font-weight: bold;
  color: #6c5ce7;
}

.menu-icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.auth-buttons {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-outline {
  color: #333;
  background: transparent;
  border: 2px solid #333;
}

.btn-outline:hover {
  background: #f0f0f0;
}

.btn-primary {
  background: linear-gradient(135deg, #6c5ce7, #a29bfe);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(108, 92, 231, 0.3);
}
</style>
