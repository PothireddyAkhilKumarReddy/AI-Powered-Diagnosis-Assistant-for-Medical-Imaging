<template>
  <main class="main-content">
    <HeroSection @scroll-to-chat="scrollToChat" />
    <TrustLogos />
    <FeaturesSection />
    <AiHighlightSection @scroll-to-chat="scrollToChat" />
    <TestimonialsSection />
    <FaqSection />
    <CtaSection @scroll-to-chat="scrollToChat" />
    
    <!-- Chat Section moved towards the bottom as the core app interaction -->
    <div class="chat-wrapper" id="chat">
      <div class="container pb-5">
        <div class="text-center mb-4 fade-in">
          <div class="badge badge-success mb-2">Live Demo</div>
          <h2>Experience the AI Assistant</h2>
          <p class="text-muted">Upload a scan or describe symptoms below to see it in action.</p>
        </div>
        <ChatSection ref="chatSection" />
      </div>
    </div>
  </main>
</template>

<script>
import { ref } from 'vue'
import HeroSection from '../components/HeroSection.vue'
import TrustLogos from '../components/TrustLogos.vue'
import FeaturesSection from '../components/FeaturesSection.vue'
import AiHighlightSection from '../components/AiHighlightSection.vue'
import TestimonialsSection from '../components/TestimonialsSection.vue'
import FaqSection from '../components/FaqSection.vue'
import CtaSection from '../components/CtaSection.vue'
import ChatSection from '../components/ChatSection.vue'

export default {
  name: 'HomePage',
  components: {
    HeroSection,
    TrustLogos,
    FeaturesSection,
    AiHighlightSection,
    TestimonialsSection,
    FaqSection,
    CtaSection,
    ChatSection
  },
  setup() {
    const chatSection = ref(null)

    const scrollToChat = () => {
      // In a real app we'd scroll to the wrapper
      const el = document.getElementById('chat')
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' })
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

.chat-wrapper {
  background-color: var(--surface-color);
  padding: 6rem 0;
  border-top: 1px solid var(--border-color);
  scroll-margin-top: 80px; /* Offset for sticky header */
}

/* Global Container Utility (Should be moved to style.css in next step if not already there) */
</style>
