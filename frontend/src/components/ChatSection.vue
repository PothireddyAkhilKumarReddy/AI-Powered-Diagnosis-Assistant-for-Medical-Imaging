<template>
  <section class="chat-section" id="chat-section">
    <h2 class="chat-title">🏥 AI Medical Image Analysis</h2>

    <div class="upload-area" 
         id="uploadArea"
         @dragover.prevent="onDragover" 
         @dragleave="onDragleave"
         @drop.prevent="onDrop"
         @click="fileInput.click()"
         :class="{ dragover: isDragging }">
      <div class="upload-icon">📁</div>
      <div class="upload-text">Drag & Drop your chest X-ray here</div>
      <div class="upload-hint">Supported: JPG, PNG, GIF</div>
      <input 
        ref="fileInput"
        type="file" 
        class="file-input" 
        accept="image/*"
        title="Upload medical image"
        @change="handleFileSelect"
      />
    </div>

    <!-- Feature 1: Image Preview -->
    <div class="image-preview" v-if="imagePreviewUrl && !isLoading">
      <img :src="imagePreviewUrl" alt="Uploaded X-ray" class="preview-img" />
      <span class="preview-label">Uploaded Image</span>
    </div>

    <div class="loading" v-if="isLoading">
      <div class="spinner"></div>
      <p>🔍 Analyzing your image with AI...</p>
    </div>

    <div class="results-section" v-if="showResults && !isLoading">
      <div class="result-card" :style="{ background: resultBackground }">
        <h3 class="result-title">✓ AI Diagnosis Result</h3>

        <!-- Image + Result Side by Side -->
        <div class="result-body">
          <div class="result-image-col" v-if="imagePreviewUrl">
            <img :src="imagePreviewUrl" alt="Analyzed X-ray" class="result-xray" />
          </div>
          <div class="result-data-col">
            <div class="result-confidence">{{ resultConfidence }}</div>
            <div class="result-class">{{ resultClass }}</div>
            <div class="result-description">{{ resultDescription }}</div>
          </div>
        </div>
        
        <div class="confidence-details" v-if="confidenceBreakdown">
          <h4>Confidence Breakdown:</h4>
          <div class="confidence-bars">
            <div v-for="(value, label) in confidenceBreakdown" :key="label" class="confidence-bar">
              <span class="label">{{ label }}</span>
              <div class="bar-background">
                <div class="bar-fill" :style="{ width: (value * 100) + '%' }"></div>
              </div>
              <span class="percentage">{{ (value * 100).toFixed(1) }}%</span>
            </div>
          </div>
        </div>

        <!-- Feature 3 (placeholder): Download Report Button -->
        <button class="download-report-btn" @click="downloadReport" v-if="lastPrediction">
          📄 Download Report
        </button>
        
        <div class="disclaimer">
          ⚠️ <strong>Disclaimer:</strong> This is an AI-assisted analysis for informational purposes only. 
          Always consult with a qualified healthcare provider for medical diagnosis and treatment.
        </div>
      </div>
    </div>

    <!-- Feature 5: Chat Message History -->
    <div class="chat-container">
      <h3 class="chat-header">💬 Ask Health Questions</h3>

      <div class="chat-messages" ref="chatMessagesContainer">
        <div v-for="(msg, index) in chatMessages" :key="index"
             :class="['chat-bubble', msg.role === 'user' ? 'user-bubble' : 'bot-bubble']">
          <div class="bubble-role">{{ msg.role === 'user' ? '🧑 You' : '🤖 DiagnoBot' }}</div>
          <div v-if="msg.role === 'bot'" class="markdown-content" v-html="renderMarkdown(msg.text)"></div>
          <p v-else>{{ msg.text }}</p>
        </div>
        <div v-if="isChatLoading" class="chat-bubble bot-bubble typing-indicator">
          <div class="bubble-role">🤖 DiagnoBot</div>
          <div class="typing-dots"><span></span><span></span><span></span></div>
        </div>
      </div>

      <div class="chat-input-container">
        <input 
          type="text" 
          class="chat-input" 
          id="chatInput"
          v-model="chatMessage"
          placeholder="Ask questions about your diagnosis or health..."
          @keypress.enter="sendMessage"
        />
        <button class="send-btn" title="Send message" @click="sendMessage" :disabled="isChatLoading">Send</button>
      </div>
    </div>
  </section>
</template>

<script>
import { ref, computed, nextTick } from 'vue'
import { marked } from 'marked'

export default {
  name: 'ChatSection',
  setup() {
    const fileInput = ref(null)
    const isDragging = ref(false)
    const isLoading = ref(false)
    const showResults = ref(false)
    const resultConfidence = ref('--')
    const resultClass = ref('')
    const resultDescription = ref('')
    const resultBackground = ref('linear-gradient(135deg, #667eea 0%, #764ba2 100%)')
    const confidenceBreakdown = ref(null)
    const chatMessage = ref('')
    const chatMessages = ref([])
    const isChatLoading = ref(false)
    const chatMessagesContainer = ref(null)
    const lastPrediction = ref(null)

    // Feature 1: Image Preview
    const imagePreviewUrl = ref(null)

    // API Configuration
    const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
      ? ''
      : 'https://medical-ai-bot-sikq.onrender.com'

    const renderMarkdown = (text) => {
      if (!text) return ''
      return marked(text)
    }

    const scrollChatToBottom = async () => {
      await nextTick()
      if (chatMessagesContainer.value) {
        chatMessagesContainer.value.scrollTop = chatMessagesContainer.value.scrollHeight
      }
    }

    const onDragover = () => {
      isDragging.value = true
    }

    const onDragleave = () => {
      isDragging.value = false
    }

    const onDrop = (event) => {
      isDragging.value = false
      const files = event.dataTransfer.files
      if (files.length > 0) {
        handleFile(files[0])
      }
    }

    const handleFileSelect = (event) => {
      if (event.target.files.length > 0) {
        handleFile(event.target.files[0])
      }
    }

    const getColorForClass = (className) => {
      const colors = {
        'COVID-19': 'linear-gradient(135deg, #ff7675, #d63031)',
        'Normal': 'linear-gradient(135deg, #55efc4, #00b894)',
        'Pneumonia': 'linear-gradient(135deg, #fab1a0, #e17055)',
        'Uncertain': 'linear-gradient(135deg, #b2bec3, #636e72)',
        'Error': 'linear-gradient(135deg, #ff7675, #d63031)'
      }
      return colors[className] || colors['Uncertain']
    }

    // Feature 4: Save analysis to history
    const saveToHistory = (prediction) => {
      try {
        const history = JSON.parse(localStorage.getItem('analysisHistory') || '[]')
        history.unshift({
          date: new Date().toISOString(),
          type: prediction.class,
          confidence: prediction.confidence,
          description: prediction.description
        })
        // Keep only last 50
        localStorage.setItem('analysisHistory', JSON.stringify(history.slice(0, 50)))
        
        // Update counters
        const count = parseInt(localStorage.getItem('analysisCount') || '0') + 1
        localStorage.setItem('analysisCount', count.toString())
        localStorage.setItem('diagnosisCount', count.toString())
      } catch (e) {
        console.error('Error saving history:', e)
      }
    }

    const handleFile = async (file) => {
      if (!file.type.startsWith('image/')) {
        alert('⚠️ Please select an image file (JPG, PNG, GIF)')
        return
      }

      // Feature 1: Show image preview
      imagePreviewUrl.value = URL.createObjectURL(file)

      showResults.value = false

      const formData = new FormData()
      formData.append('image', file)

      isLoading.value = true

      try {
        const response = await fetch(`${API_BASE_URL}/api/predict`, {
          method: 'POST',
          body: formData
        })

        const result = await response.json()
        isLoading.value = false

        if (result.success && result.prediction) {
          const prediction = result.prediction
          const confidence = prediction.confidence || 0
          const className = prediction.class || 'Unknown'

          resultClass.value = className
          resultConfidence.value = `${(confidence * 100).toFixed(1)}%`
          resultDescription.value = prediction.description || 'Analysis complete.'
          resultBackground.value = getColorForClass(className)

          if (prediction.all_predictions) {
            confidenceBreakdown.value = prediction.all_predictions
          } else {
            confidenceBreakdown.value = null
          }

          lastPrediction.value = {
            class: className,
            confidence: confidence,
            description: prediction.description,
            all_predictions: prediction.all_predictions
          }

          // Feature 4: Save to history
          saveToHistory({ class: className, confidence, description: prediction.description })

          showResults.value = true
        } else {
          resultClass.value = 'Error'
          resultConfidence.value = '--'
          resultDescription.value = result.error || 'Unable to analyze image. Please try again.'
          resultBackground.value = getColorForClass('Error')
          showResults.value = true
        }
      } catch (error) {
        console.error('Error:', error)
        isLoading.value = false
        showResults.value = true
        resultClass.value = 'Error'
        resultConfidence.value = '--'
        resultDescription.value = 'Network error. Please check your connection and try again.'
        resultBackground.value = getColorForClass('Error')
      }
    }

    // Feature 3: Download PDF report
    const downloadReport = async () => {
      if (!lastPrediction.value) return

      try {
        const response = await fetch(`${API_BASE_URL}/api/report`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            prediction: lastPrediction.value,
            imageBase64: imagePreviewUrl.value
          })
        })

        if (response.ok) {
          const blob = await response.blob()
          const url = URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = `DiagnoBot_Report_${new Date().toISOString().slice(0,10)}.pdf`
          a.click()
          URL.revokeObjectURL(url)
        } else {
          alert('Error generating report. Please try again.')
        }
      } catch (error) {
        console.error('Report error:', error)
        alert('Network error generating report.')
      }
    }

    // Feature 5: Chat with message history
    const sendMessage = async () => {
      const message = chatMessage.value.trim()
      if (!message || isChatLoading.value) return

      // Add user message to history
      chatMessages.value.push({ role: 'user', text: message })
      chatMessage.value = ''
      isChatLoading.value = true
      scrollChatToBottom()

      try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message })
        })

        const result = await response.json()

        if (result.success !== false && result.response) {
          chatMessages.value.push({ role: 'bot', text: result.response })
        } else {
          chatMessages.value.push({ role: 'bot', text: 'Sorry, I could not process your message. Please try again.' })
        }

        // Feature 4: Track chat count
        const chatCount = parseInt(localStorage.getItem('chatCount') || '0') + 1
        localStorage.setItem('chatCount', chatCount.toString())
      } catch (error) {
        console.error('Error sending message:', error)
        chatMessages.value.push({ role: 'bot', text: 'Network error. Please check your connection.' })
      } finally {
        isChatLoading.value = false
        scrollChatToBottom()
      }
    }

    return {
      fileInput,
      isDragging,
      isLoading,
      showResults,
      resultConfidence,
      resultClass,
      resultDescription,
      resultBackground,
      confidenceBreakdown,
      chatMessage,
      chatMessages,
      isChatLoading,
      chatMessagesContainer,
      imagePreviewUrl,
      lastPrediction,
      onDragover,
      onDragleave,
      onDrop,
      handleFileSelect,
      sendMessage,
      renderMarkdown,
      downloadReport
    }
  }
}
</script>

<style scoped>
.chat-section {
  padding: 3rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
  scroll-margin-top: 80px;
  animation: fadeIn 0.6s ease-out;
}

.chat-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 2rem;
  color: var(--text-color);
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.upload-area {
  border: 3px dashed var(--primary-color);
  border-radius: 15px;
  padding: 4rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: var(--transition);
  margin-bottom: 2rem;
  background: color-mix(in srgb, var(--primary-color) 5%, var(--bg-color, white));
}

.upload-area:hover,
.upload-area.dragover {
  border-color: var(--primary-dark);
  background: color-mix(in srgb, var(--primary-color) 10%, var(--bg-color, white));
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.upload-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.upload-text {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-color, #333);
  margin-bottom: 0.5rem;
}

.upload-hint {
  color: var(--text-muted);
  font-size: 0.95rem;
}

.file-input {
  display: none;
}

/* Feature 1: Image Preview */
.image-preview {
  text-align: center;
  margin-bottom: 2rem;
  animation: fadeIn 0.4s ease-out;
}

.preview-img {
  max-width: 300px;
  max-height: 300px;
  border-radius: 12px;
  box-shadow: var(--shadow-lg);
  border: 3px solid var(--primary-color);
  object-fit: contain;
  background: #000;
}

.preview-label {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: var(--text-muted);
  font-weight: 500;
}

.loading {
  text-align: center;
  padding: 3rem 2rem;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  color: white;
  border-radius: 10px;
  margin-bottom: 2rem;
  animation: slideInLeft 0.6s ease-out;
}

.spinner {
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.results-section {
  margin-bottom: 2rem;
  animation: fadeIn 0.6s ease-out 0.2s backwards;
}

.result-card {
  color: white;
  padding: 2.5rem;
  border-radius: 15px;
  text-align: center;
  box-shadow: var(--shadow-lg);
  transition: var(--transition);
  transform: translateY(0);
}

.result-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
}

.result-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Image + Result Side-by-Side */
.result-body {
  display: flex;
  gap: 2rem;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.result-image-col {
  flex: 0 0 auto;
}

.result-xray {
  width: 180px;
  height: 180px;
  object-fit: contain;
  border-radius: 12px;
  border: 3px solid rgba(255, 255, 255, 0.4);
  background: rgba(0, 0, 0, 0.3);
}

.result-data-col {
  flex: 1;
  min-width: 200px;
}

.result-confidence {
  font-size: 4rem;
  font-weight: 900;
  margin-bottom: 0.5rem;
}

.result-class {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.result-description {
  font-size: 1.1rem;
  line-height: 1.8;
  opacity: 0.95;
}

.confidence-details {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid rgba(255, 255, 255, 0.3);
  text-align: left;
}

.confidence-details h4 {
  margin-bottom: 1rem;
  font-size: 1rem;
}

.confidence-bars {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.confidence-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.label {
  flex: 0 0 120px;
  text-align: right;
  font-size: 0.9rem;
  font-weight: 600;
}

.bar-background {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.percentage {
  flex: 0 0 60px;
  text-align: right;
  font-weight: 600;
  font-size: 0.9rem;
}

/* Download Report Button */
.download-report-btn {
  margin-top: 1.5rem;
  padding: 0.8rem 2rem;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(4px);
}

.download-report-btn:hover {
  background: rgba(255, 255, 255, 0.35);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.disclaimer {
  font-size: 0.85rem;
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  line-height: 1.6;
}

/* Chat Container */
.chat-container {
  margin-top: 3rem;
  padding-top: 3rem;
  border-top: 2px solid var(--gray);
  animation: slideInRight 0.6s ease-out 0.3s backwards;
}

.chat-header {
  font-size: 1.5rem;
  color: var(--text-main);
  margin-bottom: 1.5rem;
  font-weight: 700;
}

/* Feature 5: Chat Messages Thread */
.chat-messages {
  max-height: 500px;
  overflow-y: auto;
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-color);
  border-radius: 12px;
  min-height: 60px;
  border: 1px solid var(--border-color);
}

.chat-bubble {
  padding: 1rem 1.5rem;
  border-radius: 12px;
  max-width: 80%;
  box-shadow: var(--shadow-sm);
  animation: fadeIn 0.3s ease-out;
}

.user-bubble {
  align-self: flex-end;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  color: white;
  border-bottom-right-radius: 4px;
}

.bot-bubble {
  align-self: flex-start;
  background: var(--surface-color);
  color: var(--text-main);
  border-bottom-left-radius: 4px;
  border-left: 4px solid var(--primary-color);
  border: 1px solid var(--border-color);
  border-left: 4px solid var(--primary-color);
}

.bubble-role {
  font-size: 0.75rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
  opacity: 0.8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.chat-bubble p {
  margin: 0;
  line-height: 1.6;
  font-size: 0.95rem;
  color: inherit;
}

/* Typing indicator */
.typing-indicator .typing-dots {
  display: flex;
  gap: 4px;
  padding: 0.5rem 0;
}

.typing-dots span {
  width: 8px;
  height: 8px;
  background: var(--primary-color);
  border-radius: 50%;
  animation: typingBounce 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typingBounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}

.chat-input-container {
  display: flex;
  gap: 1rem;
  align-items: center;
  background: var(--bg-color, white);
  padding: 1.2rem;
  border-radius: 10px;
  border: 2px solid var(--gray);
  transition: var(--transition);
  box-shadow: var(--shadow-sm);
}

.chat-input-container:focus-within {
  border-color: var(--primary-color);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.chat-input {
  flex: 1;
  border: none;
  padding: 0.8rem;
  font-size: 1rem;
  outline: none;
  background: transparent;
  color: var(--text-color);
}

.chat-input::placeholder {
  color: var(--text-muted);
}

.send-btn {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
  font-size: 0.95rem;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.send-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.send-btn:active {
  transform: translateY(0);
}

/* Markdown styling in bot bubbles */
.markdown-content :deep(p) {
  margin: 0 0 0.8rem 0;
  line-height: 1.6;
  font-size: 0.95rem;
}

.markdown-content :deep(p:last-child) {
  margin-bottom: 0;
}

.markdown-content :deep(strong) {
  font-weight: 700;
  color: var(--primary-color);
}

.markdown-content :deep(ul), .markdown-content :deep(ol) {
  margin: 0.5rem 0 1rem 1.5rem;
  padding: 0;
}

.markdown-content :deep(li) {
  margin-bottom: 0.4rem;
  line-height: 1.5;
}

.markdown-content :deep(h1), .markdown-content :deep(h2), .markdown-content :deep(h3) {
  margin: 1rem 0 0.5rem 0;
  font-weight: 700;
  color: var(--text-main);
}

@media (max-width: 768px) {
  .chat-section {
    padding: 2rem 1rem;
  }

  .chat-title {
    font-size: 1.8rem;
  }

  .upload-area {
    padding: 2rem 1rem;
  }

  .result-card {
    padding: 1.5rem;
  }

  .result-body {
    flex-direction: column;
  }

  .result-confidence {
    font-size: 3rem;
  }

  .result-class {
    font-size: 1.3rem;
  }

  .chat-input-container {
    flex-direction: column;
    align-items: stretch;
  }

  .chat-input {
    width: 100%;
  }

  .send-btn {
    width: 100%;
  }

  .chat-bubble {
    max-width: 95%;
  }

  .preview-img {
    max-width: 200px;
  }
}
</style>
