<template>
  <section class="ai-highlight-section section">
    <div class="container">
      <div class="highlight-grid">
        <div class="highlight-content slide-in-left">
          <div class="badge badge-warning mb-2">Smart Analysis</div>
          <h2 class="section-title">Diagnostics powered by <span class="text-gradient">Deep Learning</span></h2>
          <p class="section-description text-muted">
            Our medical AI assistant is fine-tuned on thousands of validated medical cases. 
            It automatically identifies microscopic anomalies in X-rays, MRIs, and CT scans that the human eye might miss.
          </p>
          
          <ul class="feature-list">
            <li>
              <div class="list-icon">🧠</div>
              <div>
                <strong>Contextual Understanding</strong>
                <p class="text-muted">Analyzes the full context of the image, not just isolated pixels.</p>
              </div>
            </li>
            <li>
              <div class="list-icon">⚡</div>
              <div>
                <strong>Real-time Recommendations</strong>
                <p class="text-muted">Get second opinions instantly to formulate treatment plans faster.</p>
              </div>
            </li>
            <li>
              <div class="list-icon">🔒</div>
              <div>
                <strong>Privacy First</strong>
                <p class="text-muted">All uploaded medical scans are processed securely and never stored.</p>
              </div>
            </li>
          </ul>
          
          <button @click="$emit('scroll-to-chat')" class="btn btn-primary mt-3">
            Try the AI Assistant
            <span style="font-size: 1.2rem; line-height: 1;">→</span>
          </button>
        </div>
        
        <div class="highlight-visual slide-in-right">
          <div class="visual-container">
            <!-- Simulated App Interface -->
            <div class="app-window card">
              <div class="app-header">
                <div class="dots">
                  <span></span><span></span><span></span>
                </div>
                <div class="app-title">Analysis Mode</div>
              </div>
              <div class="app-body">
                <div class="scan-image">
                  <img src="https://images.unsplash.com/photo-1551076805-e1869033e561?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" alt="Brain MRI Scan" />
                  <div class="scan-overlay">
                    <div class="scan-box"></div>
                    <div class="scan-line"></div>
                  </div>
                </div>
                <div class="analysis-results">
                  <div class="result-item">
                    <div class="result-header">
                      <span>Neural Assessment</span>
                      <span class="text-success">98.5% Confidence</span>
                    </div>
                    <div class="progress-bar"><div class="progress" style="width: 98.5%"></div></div>
                  </div>
                  <div class="result-item">
                    <div class="result-header">
                      <span>Tissue Abnormality</span>
                      <span class="text-warning">Low Risk</span>
                    </div>
                    <div class="progress-bar"><div class="progress warning" style="width: 15%"></div></div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Abstract decorations -->
            <div class="decor-circle"></div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'AiHighlightSection'
}
</script>

<style scoped>
.ai-highlight-section {
  background-color: var(--surface-color);
  overflow: hidden;
}

.highlight-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.section-title {
  margin-bottom: 1.5rem;
}

.section-description {
  font-size: 1.125rem;
  margin-bottom: 2.5rem;
  color: var(--text-muted);
}

.text-gradient {
  background: linear-gradient(135deg, var(--warning-color) 0%, #f97316 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feature-list li {
  display: flex;
  gap: 1rem;
}

.list-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.feature-list strong {
  display: block;
  font-size: 1.125rem;
  color: var(--text-main);
  margin-bottom: 0.25rem;
}

.feature-list p {
  margin: 0;
  font-size: 0.95rem;
}

/* Visual Side */
.highlight-visual {
  position: relative;
  width: 100%;
}

.visual-container {
  position: relative;
  z-index: 1;
  padding: 2rem;
}

.decor-circle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120%;
  aspect-ratio: 1;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(245, 158, 11, 0.1) 0%, transparent 70%);
  z-index: 0;
  pointer-events: none;
}

.app-window {
  position: relative;
  z-index: 2;
  padding: 0;
  overflow: hidden;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--border-color);
}

.app-header {
  background-color: var(--bg-color);
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.dots {
  display: flex;
  gap: 6px;
}

.dots span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: var(--border-color);
}

.dots span:nth-child(1) { background-color: #ff5f56; }
.dots span:nth-child(2) { background-color: #ffbd2e; }
.dots span:nth-child(3) { background-color: #27c93f; }

.app-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-muted);
  margin: 0 auto;
  transform: translateX(-14px); /* Offset for dots */
}

.app-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.scan-image {
  position: relative;
  width: 100%;
  height: 250px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  background-color: #000;
}

.scan-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  opacity: 0.8;
}

.scan-overlay {
  position: absolute;
  inset: 0;
}

.scan-box {
  position: absolute;
  top: 20%;
  left: 20%;
  right: 20%;
  bottom: 20%;
  border: 2px dashed var(--warning-color);
  border-radius: 8px;
  animation: pulse 2s infinite;
}

.scan-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background-color: var(--primary-color);
  box-shadow: 0 0 10px var(--primary-color);
  animation: scan 3s linear infinite;
}

@keyframes scan {
  0% { top: 0; opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { top: 100%; opacity: 0; }
}

.analysis-results {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: var(--bg-color);
  padding: 1rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
}

.result-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.result-header {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
  font-weight: 600;
}

.text-success { color: var(--success-color); }
.text-warning { color: var(--warning-color); }

.progress-bar {
  width: 100%;
  height: 6px;
  background-color: var(--border-color);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: var(--success-color);
  border-radius: var(--radius-full);
}

.progress.warning {
  background-color: var(--warning-color);
}

@media (max-width: 900px) {
  .highlight-grid {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
  
  .visual-container {
    max-width: 500px;
    margin: 0 auto;
    padding: 1rem 0;
  }
}
</style>
