class SigilcraftApp {
  constructor() {
    this.state = {
      isPro: localStorage.getItem('sigilcraft_pro') === 'true',
      isGenerating: false,
      cooldownActive: false,
      cooldownTime: 10,
      lastGeneratedImage: null,
      sigilGallery: JSON.parse(localStorage.getItem('sigilcraft_gallery') || '[]'),
      currentTheme: 'cosmic'
    };

    this.domElements = {};
    this.energyTypes = [
      { id: 'mystical', icon: '🔮', name: 'Mystical', description: 'Ancient wisdom & mystery' },
      { id: 'cosmic', icon: '🌌', name: 'Cosmic', description: 'Universal connection' },
      { id: 'elemental', icon: '🌿', name: 'Elemental', description: 'Natural forces' },
      { id: 'crystal', icon: '💎', name: 'Crystal', description: 'Clarity & healing' },
      { id: 'shadow', icon: '🌑', name: 'Shadow', description: 'Hidden power' },
      { id: 'light', icon: '☀️', name: 'Light', description: 'Pure radiance' },
      { id: 'storm', icon: '⚡', name: 'Storm', description: 'Raw electric energy' },
      { id: 'void', icon: '🕳️', name: 'Void', description: 'Infinite potential' }
    ];

    this.isMobile = window.innerWidth <= 768;
    this.init();
  }

  init() {
    document.addEventListener('DOMContentLoaded', () => {
      this.initializeDOM();
      this.setupEventListeners();
      this.renderEnergySelection();
      this.updateGallery();
      this.checkProStatus();
      this.initializeParticles();
      this.initializeMobileOptimizations();
    });

    // If DOM already loaded
    if (document.readyState === 'loading') {
      // Wait for DOMContentLoaded
    } else {
      // DOM already loaded
      this.initializeDOM();
      this.setupEventListeners();
      this.renderEnergySelection();
      this.updateGallery();
      this.checkProStatus();
      this.initializeParticles();
      this.initializeMobileOptimizations();
    }
  }

  initializeDOM() {
    this.domElements = {
      phraseInput: document.getElementById('phraseInput'),
      energyGrid: document.getElementById('energyGrid'),
      generateBtn: document.getElementById('generateBtn'),
      sigilContainer: document.getElementById('sigilContainer'),
      sigilImage: document.getElementById('sigilImage'),
      sigilInfo: document.getElementById('sigilInfo'),
      galleryContainer: document.getElementById('galleryContainer'),
      proBadge: document.querySelector('.pro-badge'),
      textAnalysis: document.getElementById('textAnalysis')
    };
  }

  setupEventListeners() {
    // Generate button
    if (this.domElements.generateBtn) {
      this.domElements.generateBtn.addEventListener('click', () => this.generateSigil());
    }

    // Phrase input
    if (this.domElements.phraseInput) {
      this.domElements.phraseInput.addEventListener('input', (e) => {
        this.updateTextAnalysis(e.target.value);
      });

      this.domElements.phraseInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          this.generateSigil();
        }
      });
    }

    // Mobile optimizations
    window.addEventListener('resize', () => this.handleViewportResize());
    window.addEventListener('orientationchange', () => {
      setTimeout(() => this.handleViewportResize(), 100);
    });

    // Modal close handlers
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('modal')) {
        this.closeModals();
      }
    });
  }

  renderEnergySelection() {
    if (!this.domElements.energyGrid) return;

    const availableEnergies = this.state.isPro ? this.energyTypes : this.energyTypes.slice(0, 3);

    this.domElements.energyGrid.innerHTML = availableEnergies.map(energy => `
      <div class="energy-option" data-energy="${energy.id}">
        <div class="energy-icon">${energy.icon}</div>
        <div class="energy-name">${energy.name}</div>
        <div class="energy-description">${energy.description}</div>
      </div>
    `).join('');

    // Add event listeners for energy selection
    this.domElements.energyGrid.querySelectorAll('.energy-option').forEach(option => {
      option.addEventListener('click', () => {
        // Remove previous selection
        this.domElements.energyGrid.querySelectorAll('.energy-option').forEach(opt => 
          opt.classList.remove('selected'));

        // Add selection to clicked option
        option.classList.add('selected');

        // Store selected energy
        this.state.selectedEnergy = option.dataset.energy;

        // Vibration feedback for mobile
        this.vibrate([50]);
      });
    });

    // Select first energy by default
    const firstOption = this.domElements.energyGrid.querySelector('.energy-option');
    if (firstOption) {
      firstOption.classList.add('selected');
      this.state.selectedEnergy = firstOption.dataset.energy;
    }
  }

  async generateSigil() {
    if (this.state.isGenerating || this.state.cooldownActive) return;

    const phrase = this.domElements.phraseInput?.value?.trim();
    if (!phrase) {
      this.showToast('❌ Please enter a phrase', 'error');
      return;
    }

    if (phrase.length < 2) {
      this.showToast('❌ Phrase must be at least 2 characters', 'error');
      return;
    }

    const selectedEnergy = this.state.selectedEnergy || 'mystical';

    try {
      this.state.isGenerating = true;
      this.updateGenerateButton();
      this.vibrate([100, 50, 100]);

      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          phrase,
          vibe: selectedEnergy,
          advanced: this.state.isPro
        })
      });

      const data = await response.json();

      if (data.success) {
        this.displaySigil(data);
        this.addToGallery(data);
        this.showToast('✨ Sigil manifested successfully!', 'success');

        if (!this.state.isPro) {
          this.startCooldown();
        }
      } else {
        throw new Error(data.error || 'Generation failed');
      }

    } catch (error) {
      console.error('Generation error:', error);
      this.showToast('❌ Generation failed: ' + error.message, 'error');
    } finally {
      this.state.isGenerating = false;
      this.updateGenerateButton();
    }
  }

  displaySigil(data) {
    if (!this.domElements.sigilContainer) return;

    this.domElements.sigilContainer.style.display = 'block';

    if (this.domElements.sigilImage) {
      this.domElements.sigilImage.src = `data:image/png;base64,${data.image}`;
      this.domElements.sigilImage.alt = `Sigil for "${data.phrase}"`;
    }

    if (this.domElements.sigilInfo) {
      this.domElements.sigilInfo.innerHTML = `
        <h3>"${data.phrase}"</h3>
        <div class="sigil-vibe">${data.vibe} energy</div>
        <div class="sigil-actions">
          <button class="btn btn-primary" onclick="app.downloadSigil()">
            📥 Download
          </button>
          <button class="btn btn-secondary" onclick="app.addToGallery()">
            🖼️ Save to Gallery
          </button>
        </div>
      `;
    }

    this.state.lastGeneratedImage = data;

    // Scroll to sigil
    this.scrollToElement(this.domElements.sigilContainer);
  }

  updateGenerateButton() {
    if (!this.domElements.generateBtn) return;

    if (this.state.isGenerating) {
      this.domElements.generateBtn.innerHTML = '✨ Manifesting...';
      this.domElements.generateBtn.disabled = true;
    } else if (this.state.cooldownActive) {
      this.domElements.generateBtn.disabled = true;
    } else {
      this.domElements.generateBtn.innerHTML = '🎨 Generate Sigil';
      this.domElements.generateBtn.disabled = false;
    }
  }

  downloadSigil() {
    if (!this.state.lastGeneratedImage) return;

    const link = document.createElement('a');
    link.href = `data:image/png;base64,${this.state.lastGeneratedImage.image}`;
    link.download = `sigil-${this.state.lastGeneratedImage.phrase.replace(/\s+/g, '-')}.png`;
    link.click();

    this.showToast('📥 Sigil downloaded!', 'success');
  }

  addToGallery(data = null) {
    const sigilData = data || this.state.lastGeneratedImage;
    if (!sigilData) return;

    const galleryItem = {
      id: Date.now(),
      phrase: sigilData.phrase,
      vibe: sigilData.vibe,
      image: sigilData.image,
      timestamp: new Date().toISOString()
    };

    this.state.sigilGallery.unshift(galleryItem);

    // Limit gallery size
    if (this.state.sigilGallery.length > 20) {
      this.state.sigilGallery = this.state.sigilGallery.slice(0, 20);
    }

    localStorage.setItem('sigilcraft_gallery', JSON.stringify(this.state.sigilGallery));
    this.updateGallery();
    this.showToast('🖼️ Added to gallery!', 'success');
  }

  updateGallery() {
    if (!this.domElements.galleryContainer) return;

    if (this.state.sigilGallery.length === 0) {
      this.domElements.galleryContainer.innerHTML = `
        <div class="gallery-empty">
          <p>Your sigil gallery is empty. Generate your first sigil to begin your collection!</p>
        </div>
      `;
      return;
    }

    this.domElements.galleryContainer.innerHTML = `
      <div class="gallery-grid">
        ${this.state.sigilGallery.map(item => `
          <div class="gallery-item" data-id="${item.id}">
            <img src="data:image/png;base64,${item.image}" alt="Sigil: ${item.phrase}">
            <div class="gallery-overlay">
              <div class="gallery-phrase">${item.phrase}</div>
              <div class="gallery-vibe">${item.vibe}</div>
              <div class="gallery-actions">
                <button class="gallery-btn" onclick="app.downloadGalleryItem(${item.id})">📥</button>
                <button class="gallery-btn" onclick="app.deleteGalleryItem(${item.id})">🗑️</button>
              </div>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  downloadGalleryItem(id) {
    const item = this.state.sigilGallery.find(i => i.id === id);
    if (!item) return;

    const link = document.createElement('a');
    link.href = `data:image/png;base64,${item.image}`;
    link.download = `sigil-${item.phrase.replace(/\s+/g, '-')}.png`;
    link.click();

    this.showToast('📥 Sigil downloaded!', 'success');
  }

  deleteGalleryItem(id) {
    if (confirm('Delete this sigil from your gallery?')) {
      this.state.sigilGallery = this.state.sigilGallery.filter(item => item.id !== id);
      localStorage.setItem('sigilcraft_gallery', JSON.stringify(this.state.sigilGallery));
      this.updateGallery();
      this.showToast('🗑️ Sigil deleted', 'info');
    }
  }

  async checkProStatus() {
    try {
      const response = await fetch('/api/pro-status');
      if (response.ok) {
        const data = await response.json();
        this.state.isPro = data.isPro || false;
      }
    } catch (error) {
      console.log('Pro status check failed, using local storage');
    }

    this.updateProStatus();
  }

  updateProStatus() {
    if (this.domElements.proBadge) {
      this.domElements.proBadge.style.display = this.state.isPro ? 'flex' : 'none';
    }
    this.renderEnergySelection();
  }

  submitProKey() {
    const keyInput = document.getElementById('proKeyInput');
    if (!keyInput) return;

    const key = keyInput.value.trim();
    if (key === 'changeme_super_secret') {
      this.state.isPro = true;
      localStorage.setItem('sigilcraft_pro', 'true');
      this.updateProStatus();
      this.closeModals();
      this.showToast('✨ Pro features activated!', 'success');
      keyInput.value = '';
    } else {
      this.showToast('❌ Invalid pro key', 'error');
    }
  }

  closeModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => modal.style.display = 'none');
  }

  startCooldown() {
    if (this.state.isPro) return;

    this.state.cooldownActive = true;
    let timeLeft = this.state.cooldownTime;

    const timer = setInterval(() => {
      timeLeft--;

      if (this.domElements.generateBtn) {
        this.domElements.generateBtn.innerHTML = `⏳ Cooldown: ${timeLeft}s`;
        this.domElements.generateBtn.disabled = true;
      }

      if (timeLeft <= 0) {
        clearInterval(timer);
        this.state.cooldownActive = false;
        this.updateGenerateButton();
      }
    }, 1000);
  }

  updateTextAnalysis(text) {
    if (!this.domElements.textAnalysis) return;

    if (!text || text.length < 2) {
      this.domElements.textAnalysis.innerHTML = `
        <p class="analysis-prompt">Enter a phrase to see advanced analysis...</p>
      `;
      return;
    }

    const analysis = this.performTextAnalysis(text);

    this.domElements.textAnalysis.innerHTML = `
      <h4>📊 Advanced Text Analysis</h4>
      <div class="analysis-grid">
        <div class="analysis-item">
          <span class="label">Words</span>
          <span class="value">${analysis.wordCount}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Characters</span>
          <span class="value">${analysis.charCount}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Vowels</span>
          <span class="value">${analysis.vowelCount}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Consonants</span>
          <span class="value">${analysis.consonantCount}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Unique Letters</span>
          <span class="value">${analysis.uniqueLetters}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Complexity</span>
          <span class="value complexity-${analysis.complexity}">${analysis.complexity}</span>
        </div>
      </div>
      <div class="energy-prediction">
        <span class="label">Predicted Energy:</span>
        <span class="value">${analysis.predictedEnergy}</span>
      </div>
    `;
  }

  performTextAnalysis(text) {
    const words = text.trim().split(/\s+/);
    const chars = text.replace(/\s/g, '');
    const vowels = chars.match(/[aeiouAEIOU]/g) || [];
    const consonants = chars.match(/[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]/g) || [];
    const uniqueLetters = new Set(chars.toLowerCase().match(/[a-z]/g) || []).size;

    let complexity = 'Simple';
    if (words.length > 3 || uniqueLetters > 8) complexity = 'Medium';
    if (words.length > 6 || uniqueLetters > 12) complexity = 'Complex';
    if (words.length > 10 || uniqueLetters > 15) complexity = 'Profound';

    // Predict energy based on text characteristics
    let predictedEnergy = 'mystical';
    if (text.toLowerCase().includes('star') || text.toLowerCase().includes('space')) predictedEnergy = 'cosmic';
    if (text.toLowerCase().includes('nature') || text.toLowerCase().includes('earth')) predictedEnergy = 'elemental';
    if (text.toLowerCase().includes('light') || text.toLowerCase().includes('bright')) predictedEnergy = 'light';
    if (text.toLowerCase().includes('shadow') || text.toLowerCase().includes('dark')) predictedEnergy = 'shadow';

    return {
      wordCount: words.length,
      charCount: chars.length,
      vowelCount: vowels.length,
      consonantCount: consonants.length,
      uniqueLetters,
      complexity,
      predictedEnergy
    };
  }

  showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add('show'), 100);
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => document.body.removeChild(toast), 300);
    }, 3000);
  }

  initializeMobileOptimizations() {
    if (this.isMobile) {
      // Set CSS custom property for mobile viewport height
      const setVH = () => {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
      };

      setVH();
      window.addEventListener('resize', setVH);

      // Add mobile class to body
      document.body.classList.add('mobile');

      // Optimize touch interactions
      document.addEventListener('touchstart', () => {}, { passive: true });
    }
  }

  handleViewportResize() {
    // Update mobile status
    this.isMobile = window.innerWidth <= 768;

    // Debounce resize updates
    clearTimeout(this.resizeTimeout);
    this.resizeTimeout = setTimeout(() => {
      this.updateGallery();

      if (this.isMobile) {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
      }
    }, 100);
  }

  vibrate(pattern = [50]) {
    if (navigator.vibrate && this.isMobile) {
      navigator.vibrate(pattern);
    }
  }

  scrollToElement(element, offset = 0) {
    if (!element) return;

    const elementPosition = element.offsetTop - offset;
    const offsetPosition = elementPosition - (this.isMobile ? 80 : 100);

    if ('scrollBehavior' in document.documentElement.style) {
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    } else {
      window.scrollTo(0, offsetPosition);
    }
  }

  initializeParticles() {
    const particleContainer = document.createElement('div');
    particleContainer.className = 'particle-container';
    particleContainer.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: -1;
    `;

    // Add CSS for particle animation
    const style = document.createElement('style');
    style.textContent = `
      @keyframes float {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
      }
    `;
    document.head.appendChild(style);

    for (let i = 0; i < 50; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.cssText = `
        position: absolute;
        width: 2px;
        height: 2px;
        background: rgba(138, 43, 226, ${Math.random() * 0.5});
        border-radius: 50%;
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        animation: float ${3 + Math.random() * 4}s linear infinite;
        animation-delay: ${Math.random() * 2}s;
      `;
      particleContainer.appendChild(particle);
    }

    document.body.appendChild(particleContainer);
  }
}

// Global functions for HTML onclick handlers
window.openProModal = function() {
  const modal = document.getElementById('proModal');
  if (modal) modal.style.display = 'flex';
};

window.closeProModal = function() {
  const modal = document.getElementById('proModal');
  if (modal) modal.style.display = 'none';
};

window.submitProKey = function() {
  app.submitProKey();
};

// Initialize the application
const app = new SigilcraftApp();

// Log successful load
console.log('🚀 Sigilcraft JavaScript loaded successfully!');