<template>
  <section class="chat-section" id="chat-section">
    <h2 class="chat-title">AI Medical Image Analysis</h2>

    <div class="upload-area" 
         id="uploadArea"
         @dragover.prevent="onDragover" 
         @dragleave="onDragleave"
         @drop.prevent="onDrop"
         @click="fileInput.click()"
         :class="{ dragover: isDragging }">
      <div class="upload-icon">📁</div>
      <div class="upload-text">Drag & Drop your medical image here</div>
      <div class="upload-hint">or click to browse files</div>
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
      <p>Analyzing your image with AI...</p>
    </div>

    <div class="results-section" v-if="showResults">
      <div class="result-card" :style="{ background: resultBackground }">
        <h3 class="result-title">AI Diagnosis Result</h3>
        <div class="result-confidence">{{ resultConfidence }}</div>
        <div class="result-description">{{ resultDescription }}</div>
      </div>
    </div>

    <div class="chat-input-container">
      <input 
        type="text" 
        class="chat-input" 
        id="chatInput"
        v-model="chatMessage"
        placeholder="Type or share photo"
        @keypress.enter="sendMessage"
      />
      <div class="chat-actions">
        <span class="attach-button">+ attach</span>
        <button class="action-btn">🎤</button>
        <button class="action-btn send-btn" @click="sendMessage">↑</button>
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
    const resultConfidence = ref('85%')
    const resultDescription = ref('')
    const resultBackground = ref('')
    const chatMessage = ref('')

    // Determine the API URL based on environment
    const API_BASE_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
      ? ''
      : 'https://medical-ai-bot-mtg8.onrender.com'

    console.log(`Using API Base URL: ${API_BASE_URL || 'Relative Path'}`)

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

    const handleFile = async (file) => {
      if (!file.type.startsWith('image/')) {
        alert('Please select an image file')
        return
      }

      const formData = new FormData()
      formData.append('image', file)

      // Show loading
      isLoading.value = true
      showResults.value = false

      try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
          method: 'POST',
          body: formData
        })

        const result = await response.json()

        // Hide loading and show results
        isLoading.value = false
        showResults.value = true

        if (result.success) {
          const prediction = result.prediction
          const confidence = Math.round(prediction.confidence * 100)

          resultConfidence.value = `${confidence}%`
          resultDescription.value = `AI Diagnosis: ${prediction.class} - ${prediction.description}`

          // Add color coding based on diagnosis
          if (prediction.class === 'COVID-19') {
            resultBackground.value = 'linear-gradient(135deg, #ff7675, #d63031)' // Red
          } else if (prediction.class === 'Pneumonia') {
            resultBackground.value = 'linear-gradient(135deg, #fab1a0, #e17055)' // Orange
          } else if (prediction.class === 'Normal') {
            resultBackground.value = 'linear-gradient(135deg, #55efc4, #00b894)' // Green
          } else {
            resultBackground.value = 'linear-gradient(135deg, #b2bec3, #636e72)' // Grey
          }
        } else {
          resultConfidence.value = 'Error'
          resultDescription.value = result.error || 'Unable to analyze image. Please try again.'
          resultBackground.value = 'linear-gradient(135deg, #ff7675, #d63031)'
        }
      } catch (error) {
        console.error('Error:', error)
        isLoading.value = false
        showResults.value = true
        resultConfidence.value = 'Error'
        resultDescription.value = 'Network error. Please check your connection.'
        resultBackground.value = 'linear-gradient(135deg, #ff7675, #d63031)'
      }
    }

    const sendMessage = async () => {
      const message = chatMessage.value.trim()
      if (!message) return

      try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message })
        })

        const result = await response.json()

        // Show the response in the results section
        showResults.value = true
        resultConfidence.value = 'AI Response'
        resultDescription.value = result.response
        resultBackground.value = 'linear-gradient(135deg, #6c5ce7, #a29bfe)'

        chatMessage.value = ''
      } catch (error) {
        console.error('Error sending message:', error)
      }
    }

    return {
      fileInput,
      isDragging,
      isLoading,
      showResults,
      resultConfidence,
      resultDescription,
      resultBackground,
      chatMessage,
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
  max-width: 1000px;
  margin: 0 auto;
  scroll-margin-top: 80px;
}

.chat-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #333;
}

.upload-area {
  border: 2px dashed #6c5ce7;
  border-radius: 10px;
  padding: 3rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 2rem;
}

.upload-area:hover,
.upload-area.dragover {
  border-color: #a29bfe;
  background: #f5f3ff;
}

.upload-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.upload-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.upload-hint {
  color: #999;
  font-size: 0.9rem;
}

.file-input {
  display: none;
}

.loading {
  text-align: center;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 10px;
  margin-bottom: 2rem;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #6c5ce7;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.results-section {
  margin-bottom: 2rem;
}

.result-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 10px;
  text-align: center;
}

.result-title {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.result-confidence {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.result-description {
  font-size: 1rem;
  line-height: 1.6;
}

.chat-input-container {
  display: flex;
  gap: 1rem;
  align-items: center;
  background: white;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.chat-input {
  flex: 1;
  border: none;
  padding: 0.8rem;
  font-size: 1rem;
  outline: none;
}

.chat-input::placeholder {
  color: #b2bec3;
}

.chat-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.attach-button {
  color: #b2bec3;
  font-size: 0.9rem;
}

.action-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: #6c5ce7;
  border-radius: 50%;
  transition: all 0.3s ease;
  font-size: 1.1rem;
}

.action-btn:hover {
  background: #f0f2ff;
}

.send-btn {
  background: linear-gradient(135deg, #6c5ce7, #a29bfe);
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-btn:hover {
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .chat-section {
    padding: 2rem 1rem;
  }

  .upload-area {
    padding: 2rem;
  }

  .chat-input-container {
    flex-direction: column;
  }

  .chat-input {
    width: 100%;
  }
}
</style>
