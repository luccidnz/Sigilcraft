class SigilcraftApp {
  constructor() {
    this.state = {
      isPro: this.loadProStatus(),
      isGenerating: false,
      cooldownActive: false,
      cooldownTime: 10,
      lastGeneratedImage: null,
      sigilGallery: JSON.parse(localStorage.getItem('sigilcraft_gallery') || '[]'),
      currentTheme: 'cosmic',
      selectedEnergy: 'mystical'
    };

    this.domElements = {};
    this.energyTypes = [
      { id: 'mystical', icon: '🔮', name: 'Mystical', description: 'Ancient wisdom & sacred curved geometry' },
      { id: 'cosmic', icon: '🌌', name: 'Cosmic', description: 'Universal stellar radiant burst patterns' },
      { id: 'elemental', icon: '🌿', name: 'Elemental', description: 'Natural organic flowing growth' },
      { id: 'crystal', icon: '💎', name: 'Crystal', description: 'Prismatic angular geometric precision' },
      { id: 'shadow', icon: '🌑', name: 'Shadow', description: 'Hidden jagged consuming power' },
      { id: 'light', icon: '☀️', name: 'Light', description: 'Divine emanating luminous radiance' },
      { id: 'storm', icon: '⚡', name: 'Storm', description: 'Electric explosive lightning chaos' },
      { id: 'void', icon: '🕳️', name: 'Void', description: 'Infinite recursive impossible geometry' }
    ];

    this.isMobile = window.innerWidth <= 768;
    this.debouncedAnalysis = this.debounce(this.performTextAnalysis.bind(this), 500);
    this.init();
  }

  init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        this.setupApp();
      });
    } else {
      this.setupApp();
    }
  }

  setupApp() {
    this.initializeDOM();
    this.setupEventListeners();
    this.renderEnergySelection();
    this.updateGallery();
    this.updateProStatus();
    this.initializeParticles();
    this.initializeMobileOptimizations();
    console.log('🚀 Sigilcraft app initialized successfully!');
  }

  loadProStatus() {
    const storedPro = localStorage.getItem('sigilcraft_pro');
    return storedPro === 'true';
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
      textAnalysis: document.getElementById('textAnalysis'),
      proModal: document.getElementById('proModal'),
      proKeyInput: document.getElementById('proKeyInput'),
      unlockSection: document.querySelector('.unlock-section'),
      charCounter: document.getElementById('charCounter')
    };

    this.updateCharCounter();
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
        this.updateCharCounter();
        this.debouncedAnalysis(e.target.value);
      });

      this.domElements.phraseInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.generateSigil();
        }
      });
    }

    // Pro key input
    if (this.domElements.proKeyInput) {
      this.domElements.proKeyInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          this.submitProKey();
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

    // Touch handling for better mobile experience
    if (this.isMobile) {
      document.addEventListener('touchstart', () => {}, { passive: true });
    }
  }

  renderEnergySelection() {
    if (!this.domElements.energyGrid) return;

    const availableEnergies = this.state.isPro ? this.energyTypes : this.energyTypes.slice(0, 4);

    this.domElements.energyGrid.innerHTML = availableEnergies.map(energy => `
      <div class="energy-card ${this.state.selectedEnergy === energy.id ? 'selected' : ''} ${!this.state.isPro && this.energyTypes.indexOf(energy) >= 4 ? 'locked' : ''}"
           onclick="app.selectEnergy('${energy.id}')" 
           data-energy="${energy.id}">
        <div class="energy-icon">${energy.icon}</div>
        <div class="energy-name">${energy.name}</div>
        <div class="energy-description">${energy.description}</div>
        ${!this.state.isPro && this.energyTypes.indexOf(energy) >= 4 ? '<div class="energy-lock">🔒</div>' : ''}
      </div>
    `).join('');
  }

  selectEnergy(energyId) {
    const energy = this.energyTypes.find(e => e.id === energyId);
    if (!energy) return;

    const energyIndex = this.energyTypes.indexOf(energy);
    if (!this.state.isPro && energyIndex >= 4) {
      this.openProModal();
      this.showToast('🔒 Premium energy type - Pro Key required!', 'warning');
      return;
    }

    this.state.selectedEnergy = energyId;
    this.renderEnergySelection();
    this.vibrate([50]);
    this.showToast(`✨ Selected ${energy.name} energy`, 'success');
  }

  async generateSigil() {
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

      console.log('🎨 Generating sigil:', { phrase, vibe: selectedEnergy, advanced: this.state.isPro });

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
        this.showToast('✨ Revolutionary sigil manifested!', 'success');
        this.vibrate([200]);
        this.startCooldown();
      } else {
        this.showToast(`❌ ${data.error || 'Generation failed'}`, 'error');
        this.vibrate([300]);
      }
    } catch (error) {
      console.error('Generation error:', error);
      this.showToast('❌ Network error occurred', 'error');
      this.vibrate([300]);
    } finally {
      this.state.isGenerating = false;
      this.updateGenerateButton();
    }
  }

  displaySigil(data) {
    if (!this.domElements.sigilContainer) return;

    this.domElements.sigilContainer.classList.add('visible');

    if (this.domElements.sigilImage) {
      this.domElements.sigilImage.src = `data:image/png;base64,${data.image}`;
      this.domElements.sigilImage.alt = `Ultra-unique sigil for "${data.phrase}"`;
    }

    if (this.domElements.sigilInfo) {
      this.domElements.sigilInfo.innerHTML = `
        <h3>"${data.phrase}"</h3>
        <div class="sigil-vibe">${data.vibe} energy • ${data.advanced ? 'Ultra-Advanced' : 'Enhanced'}</div>
        <div class="sigilActions">
          <button class="btn btn-primary" onclick="app.downloadSigil()">
            📥 Download PNG
          </button>
          <button class="btn btn-secondary" onclick="app.shareImage()">
            🔗 Share
          </button>
        </div>
      `;
    }

    this.state.lastGeneratedImage = data;
    this.scrollToElement(this.domElements.sigilContainer);
  }

  updateGenerateButton() {
    if (!this.domElements.generateBtn) return;

    if (this.state.isGenerating) {
      this.domElements.generateBtn.innerHTML = '✨ Manifesting Ultra-Unique Sigil...';
      this.domElements.generateBtn.disabled = true;
      this.domElements.generateBtn.classList.add('generating');
    } else if (this.state.cooldownActive) {
      this.domElements.generateBtn.disabled = true;
      this.domElements.generateBtn.classList.remove('generating');
    } else {
      this.domElements.generateBtn.innerHTML = '🎨 Generate Ultra-Unique Sigil';
      this.domElements.generateBtn.disabled = false;
      this.domElements.generateBtn.classList.remove('generating');
    }
  }

  downloadSigil() {
    if (!this.state.lastGeneratedImage) {
      this.showToast('❌ No sigil to download', 'error');
      return;
    }

    const data = this.state.lastGeneratedImage;
    const link = document.createElement('a');
    link.href = `data:image/png;base64,${data.image}`;
    const filename = `sigilcraft-${data.phrase.replace(/\s+/g, '-').toLowerCase()}-${data.vibe}.png`;
    link.download = filename;
    link.click();

    this.showToast('📥 Sigil downloaded!', 'success');
  }

  shareImage() {
    if (!this.state.lastGeneratedImage) {
      this.showToast('❌ No sigil to share', 'error');
      return;
    }

    const text = `Check out this mystical sigil I created for "${this.state.lastGeneratedImage.phrase}" using Sigilcraft! 🔮✨`;

    if (navigator.share) {
      navigator.share({
        title: 'Sigilcraft - Revolutionary Sigil',
        text: text,
        url: window.location.href
      }).catch(err => console.log('Error sharing:', err));
    } else {
      navigator.clipboard.writeText(`${text} ${window.location.href}`);
      this.showToast('🔗 Share text copied to clipboard!', 'success');
    }
  }

  addToGallery(data) {
    const galleryItem = {
      id: Date.now(),
      phrase: data.phrase,
      vibe: data.vibe,
      image: data.image,
      advanced: data.advanced || false,
      timestamp: new Date().toISOString()
    };

    this.state.sigilGallery.unshift(galleryItem);

    // Keep only last 20 items
    if (this.state.sigilGallery.length > 20) {
      this.state.sigilGallery = this.state.sigilGallery.slice(0, 20);
    }

    localStorage.setItem('sigilcraft_gallery', JSON.stringify(this.state.sigilGallery));
    this.updateGallery();
  }

  updateGallery() {
    if (!this.domElements.galleryContainer) return;

    if (this.state.sigilGallery.length === 0) {
      this.domElements.galleryContainer.innerHTML = `
        <div class="gallery-empty">
          <div class="empty-icon">🌌</div>
          <p>Your sigil gallery awaits...</p>
          <p class="empty-subtitle">Generate your first revolutionary sigil to begin your collection</p>
        </div>
      `;
      return;
    }

    this.domElements.galleryContainer.innerHTML = this.state.sigilGallery.map(item => `
      <div class="gallery-item" data-id="${item.id}">
        <img src="data:image/png;base64,${item.image}" 
             alt="Sigil: ${item.phrase}" 
             onclick="app.viewGalleryItem(${item.id})" />
        <div class="gallery-info">
          <div class="gallery-phrase">"${item.phrase}"</div>
          <div class="gallery-vibe">${item.vibe}</div>
        </div>
        <div class="gallery-actions">
          <button onclick="app.downloadGalleryItem(${item.id})" title="Download">📥</button>
          <button onclick="app.deleteGalleryItem(${item.id})" title="Delete">🗑️</button>
        </div>
      </div>
    `).join('');
  }

  downloadGalleryItem(id) {
    const item = this.state.sigilGallery.find(i => i.id === id);
    if (!item) return;

    const link = document.createElement('a');
    link.href = `data:image/png;base64,${item.image}`;
    const filename = `sigilcraft-${item.phrase.replace(/\s+/g, '-').toLowerCase()}-${item.vibe}.png`;
    link.download = filename;
    link.click();

    this.showToast('📥 Sigil downloaded!', 'success');
  }

  viewGalleryItem(id) {
    const item = this.state.sigilGallery.find(sigil => sigil.id === id);
    if (!item) return;

    this.state.lastGeneratedImage = item;
    this.displaySigil(item);
    this.scrollToElement(this.domElements.sigilContainer);
  }

  deleteGalleryItem(id) {
    if (!confirm('Delete this sigil from your gallery?')) return;

    this.state.sigilGallery = this.state.sigilGallery.filter(item => item.id !== id);
    localStorage.setItem('sigilcraft_gallery', JSON.stringify(this.state.sigilGallery));
    this.updateGallery();
    this.showToast('🗑️ Sigil deleted', 'info');
  }

  updateProStatus() {
    if (this.domElements.proBadge) {
      this.domElements.proBadge.style.display = this.state.isPro ? 'block' : 'none';
    }

    if (this.domElements.unlockSection) {
      this.domElements.unlockSection.style.display = this.state.isPro ? 'none' : 'block';
    }

    this.renderEnergySelection();
  }

  openProModal() {
    if (this.domElements.proModal) {
      this.domElements.proModal.style.display = 'flex';
      if (this.domElements.proKeyInput) {
        this.domElements.proKeyInput.focus();
      }
    }
  }

  closeModals() {
    if (this.domElements.proModal) {
      this.domElements.proModal.style.display = 'none';
    }
  }

  submitProKey() {
    const key = this.domElements.proKeyInput?.value?.trim();
    if (!key) return;

    const validKeys = [
      process.env.PRO_KEY || 'changeme_super_secret',
      'sigilcraft_pro_2024',
      'ultra_revolutionary',
      'mystic_master_key'
    ];

    if (validKeys.includes(key)) {
      this.state.isPro = true;
      localStorage.setItem('sigilcraft_pro', 'true');
      this.updateProStatus();
      this.closeModals();
      this.showToast('🎉 Pro features unlocked! Welcome to the revolution!', 'success');
      this.vibrate([100, 100, 200]);
    } else {
      this.showToast('❌ Invalid Pro Key', 'error');
      this.vibrate([300]);
    }

    if (this.domElements.proKeyInput) {
      this.domElements.proKeyInput.value = '';
    }
  }

  startCooldown() {
    if (this.state.isPro) return; // No cooldown for Pro users

    this.state.cooldownActive = true;
    let timeLeft = this.state.cooldownTime;

    const countdown = setInterval(() => {
      if (timeLeft <= 0) {
        clearInterval(countdown);
        this.state.cooldownActive = false;
        this.updateGenerateButton();
        return;
      }

      if (this.domElements.generateBtn) {
        this.domElements.generateBtn.innerHTML = `⏳ Cooldown: ${timeLeft}s`;
      }
      timeLeft--;
    }, 1000);
  }

  updateCharCounter() {
    if (!this.domElements.phraseInput || !this.domElements.charCounter) return;

    const length = this.domElements.phraseInput.value.length;
    const maxLength = 500;

    this.domElements.charCounter.textContent = `${length}/${maxLength}`;
    this.domElements.charCounter.style.color = length > maxLength * 0.9 ? '#f44336' : 'var(--text-secondary)';
  }

  updateTextAnalysis(text) {
    if (!this.domElements.textAnalysis) return;

    if (!text || text.length < 2) {
      this.domElements.textAnalysis.innerHTML = `
        <h4>✨ Text Analysis</h4>
        <div class="analysis-prompt">Enter your phrase to see mystical analysis...</div>
      `;
      return;
    }

    const analysis = this.analyzeText(text);

    this.domElements.textAnalysis.innerHTML = `
      <h4>✨ Mystical Text Analysis</h4>
      <div class="analysis-grid">
        <div class="analysis-item">
          <span class="label">Length:</span>
          <span class="value">${analysis.length}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Words:</span>
          <span class="value">${analysis.words}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Energy:</span>
          <span class="value">${analysis.energy}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Complexity:</span>
          <span class="value complexity-${analysis.complexity}">${analysis.complexity}</span>
        </div>
      </div>
    `;
  }

  analyzeText(text) {
    const words = text.trim().split(/\s+/);
    const energy = text.split('').reduce((sum, char) => sum + char.charCodeAt(0), 0);

    let complexity = 'Simple';
    if (text.length > 50) complexity = 'Complex';
    else if (text.length > 20) complexity = 'Moderate';
    if (words.length > 10) complexity = 'Profound';

    return {
      length: text.length,
      words: words.length,
      energy: energy % 1000,
      complexity
    };
  }

  performTextAnalysis(text) {
    // Extended analysis for advanced users
    if (this.state.isPro) {
      // Additional Pro analysis features would go here
    }
  }

  scrollToElement(element) {
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  vibrate(pattern) {
    if (navigator.vibrate && this.isMobile) {
      navigator.vibrate(pattern);
    }
  }

  showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    // Style the toast
    toast.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: var(--bg-card);
      color: var(--text-primary);
      padding: var(--spacing-md) var(--spacing-lg);
      border-radius: var(--radius-md);
      border-left: 4px solid ${type === 'success' ? '#4caf50' : type === 'error' ? '#f44336' : type === 'warning' ? '#ff9800' : '#2196f3'};
      box-shadow: var(--shadow-lg);
      z-index: 10000;
      max-width: 300px;
      word-wrap: break-word;
      animation: slideInRight 0.3s ease-in;
    `;

    document.body.appendChild(toast);

    // Remove after 4 seconds
    setTimeout(() => {
      toast.style.animation = 'slideOutRight 0.3s ease-in';
      setTimeout(() => {
        if (toast.parentNode) {
          toast.parentNode.removeChild(toast);
        }
      }, 300);
    }, 4000);
  }

  handleViewportResize() {
    this.isMobile = window.innerWidth <= 768;
    // Adjust UI for mobile/desktop
  }

  initializeParticles() {
    // Placeholder for particle effects
  }

  initializeMobileOptimizations() {
    if (this.isMobile) {
      document.body.classList.add('mobile');
    }
  }

  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  resetAfterError() {
    this.state.isGenerating = false;
    this.state.cooldownActive = false;
    this.updateGenerateButton();
  }
}

// Global functions for HTML onclick handlers
window.openProModal = function() {
  if (window.app) {
    window.app.openProModal();
  }
};

window.closeProModal = function() {
  if (window.app) {
    window.app.closeModals();
  }
};

window.submitProKey = function() {
  if (window.app) {
    window.app.submitProKey();
  }
};

// Initialize the application
window.app = new SigilcraftApp();

// CSS for animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideInRight {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }

  @keyframes slideOutRight {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
  }

  @keyframes float {
    0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
  }
`;
document.head.appendChild(style);