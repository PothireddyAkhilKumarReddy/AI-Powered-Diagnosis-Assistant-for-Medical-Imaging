<template>
  <div class="app">
    <Header v-if="!['/login', '/signup'].includes($route.path)" />
    <main class="main-content">
      <router-view />
    </main>
    <Footer v-if="!['/login', '/signup'].includes($route.path)" />
  </div>
</template>

<script>
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    Header,
    Footer
  }
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
}

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
}
</style>
