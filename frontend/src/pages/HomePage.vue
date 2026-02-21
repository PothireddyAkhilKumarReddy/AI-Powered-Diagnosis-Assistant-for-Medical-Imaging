<template>
  <main class="main-content">
    <HeroSection />
    <FeaturesSection />
    <CtaSection @scroll-to-chat="scrollToChat" />
    <ChatSection ref="chatSection" />
  </main>
</template>

<script>
import { ref } from 'vue'
import HeroSection from '../components/HeroSection.vue'
import FeaturesSection from '../components/FeaturesSection.vue'
import CtaSection from '../components/CtaSection.vue'
import ChatSection from '../components/ChatSection.vue'

export default {
  name: 'HomePage',
  components: {
    HeroSection,
    FeaturesSection,
    CtaSection,
    ChatSection
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
.main-content {
  flex: 1;
}
</style>
