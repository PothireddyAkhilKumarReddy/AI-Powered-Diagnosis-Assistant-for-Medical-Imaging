<template>
  <div class="app">
    <Header />
    <main class="main-content">
      <HeroSection />
      <FeaturesSection />
      <CtaSection @scroll-to-chat="scrollToChat" />
      <ChatSection ref="chatSection" />
    </main>
    <Footer />
  </div>
</template>

<script>
import { ref } from 'vue'
import Header from './components/Header.vue'
import HeroSection from './components/HeroSection.vue'
import FeaturesSection from './components/FeaturesSection.vue'
import CtaSection from './components/CtaSection.vue'
import ChatSection from './components/ChatSection.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    Header,
    HeroSection,
    FeaturesSection,
    CtaSection,
    ChatSection,
    Footer
  },
  setup() {
    const chatSection = ref(null)

    const scrollToChat = () => {
      if (chatSection.value) {
        chatSection.value.$el.scrollIntoView({
          behavior: 'smooth'
        })
      }
    }

    return {
      chatSection,
      scrollToChat
    }
  }
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
}
</style>
