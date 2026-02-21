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

    <div class="loading" v-if="isLoading">
      <div class="spinner"></div>
      <p>🔍 Analyzing your image with AI...</p>
    </div>

    <div class="results-section" v-if="showResults && !isLoading">
      <div class="result-card" :style="{ background: resultBackground }">
        <h3 class="result-title">✓ AI Diagnosis Result</h3>
        <div class="result-confidence">{{ resultConfidence }}</div>
        <div class="result-class">{{ resultClass }}</div>
        <div class="result-description">{{ resultDescription }}</div>
        
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
        
        <div class="disclaimer">
          ⚠️ <strong>Disclaimer:</strong> This is an AI-assisted analysis for informational purposes only. 
          Always consult with a qualified healthcare provider for medical diagnosis and treatment.
        </div>
      </div>
    </div>

    <div class="chat-container">
      <h3 class="chat-header">💬 Ask Health Questions</h3>
      <div class="chat-input-container">
        <input 
          type="text" 
          class="chat-input" 
          id="chatInput"
          v-model="chatMessage"
          placeholder="Ask questions about your diagnosis or health..."
          @keypress.enter="sendMessage"
        />
        <button class="send-btn" title="Send message" @click="sendMessage">Send</button>
      </div>

      <div class="chat-response" v-if="chatResponse">
        <div class="response-bubble">
          <p>{{ chatResponse }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { ref } from 'vue'

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
    const chatResponse = ref('')

    // API Configuration
    const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
      ? ''
      : 'https://medical-ai-bot-mtg8.onrender.com'

    console.log(`API URL: ${API_BASE_URL || 'Relative Path'}`)

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

    const handleFile = async (file) => {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        alert('⚠️ Please select an image file (JPG, PNG, GIF)')
        return
      }

      // Reset previous results
      showResults.value = false
      chatResponse.value = ''

      const formData = new FormData()
      formData.append('image', file)

      // Show loading state
      isLoading.value = true

      try {
        const response = await fetch(`${API_BASE_URL}/api/predict`, {
          method: 'POST',
          body: formData
        })

        const result = await response.json()

        // Hide loading and show results
        isLoading.value = false

        if (result.success && result.prediction) {
          const prediction = result.prediction
          const confidence = prediction.confidence || 0
          const className = prediction.class || 'Unknown'

          // Update display
          resultClass.value = className
          resultConfidence.value = `${(confidence * 100).toFixed(1)}%`
          resultDescription.value = prediction.description || 'Analysis complete.'
          resultBackground.value = getColorForClass(className)

          // Show confidence breakdown
          if (prediction.all_predictions) {
            confidenceBreakdown.value = prediction.all_predictions
          } else {
            confidenceBreakdown.value = null
          }

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

    const sendMessage = async () => {
      const message = chatMessage.value.trim()
      if (!message) return

      try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message })
        })

        const result = await response.json()

        if (result.success) {
          chatResponse.value = result.response
        } else {
          chatResponse.value = 'Sorry, I could not process your message. Please try again.'
        }

        chatMessage.value = ''
      } catch (error) {
        console.error('Error sending message:', error)
        chatResponse.value = 'Network error. Please check your connection.'
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
      chatResponse,
      onDragover,
      onDragleave,
      onDrop,
      handleFileSelect,
      sendMessage
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
  background: color-mix(in srgb, var(--primary-color) 5%, white);
}

.upload-area:hover,
.upload-area.dragover {
  border-color: var(--primary-dark);
  background: color-mix(in srgb, var(--primary-color) 10%, white);
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
  color: #333;
  margin-bottom: 0.5rem;
}

.upload-hint {
  color: #999;
  font-size: 0.95rem;
}

.file-input {
  display: none;
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
  margin-bottom: 2rem;
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

.disclaimer {
  font-size: 0.85rem;
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  line-height: 1.6;
}

.chat-container {
  margin-top: 3rem;
  padding-top: 3rem;
  border-top: 2px solid var(--gray);
  animation: slideInRight 0.6s ease-out 0.3s backwards;
}

.chat-header {
  font-size: 1.5rem;
  color: var(--text-color);
  margin-bottom: 1.5rem;
  font-weight: 700;
}

.chat-input-container {
  display: flex;
  gap: 1rem;
  align-items: center;
  background: white;
  padding: 1.2rem;
  border-radius: 10px;
  border: 2px solid var(--gray);
  transition: var(--transition);
  margin-bottom: 1.5rem;
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
  color: #b2bec3;
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

.send-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.send-btn:active {
  transform: translateY(0);
}

.chat-response {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 1rem;
  animation: fadeIn 0.4s ease-out;
}

.response-bubble {
  background: var(--light-gray);
  color: var(--text-color);
  padding: 1rem 1.5rem;
  border-radius: 10px;
  max-width: 80%;
  box-shadow: var(--shadow-sm);
  border-left: 4px solid var(--primary-color);
  transition: var(--transition);
}

.response-bubble:hover {
  box-shadow: var(--shadow-md);
  transform: translateX(4px);
}

.response-bubble p {
  margin: 0;
  line-height: 1.6;
  font-size: 0.95rem;
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

  .response-bubble {
    max-width: 100%;
  }
}
</style>
