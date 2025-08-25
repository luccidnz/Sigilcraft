
class SigilcraftApp {
  constructor() {
    this.state = {
      isGenerating: false,
      cooldownActive: false,
      selectedEnergy: 'mystical',
      sigilGallery: [],
      lastGeneratedImage: null,
      isPro: false,
      cooldownTimer: 10,
      currentRequestId: null
    };

    this.isMobile = window.innerWidth <= 768;
    this.energyTypes = [
      {
        id: 'mystical',
        name: 'Mystical',
        icon: '🔮',
        description: 'Ancient wisdom & sacred geometry'
      },
      {
        id: 'cosmic',
        name: 'Cosmic',
        icon: '🌌',
        description: 'Universal stellar connection'
      },
      {
        id: 'elemental',
        name: 'Elemental',
        icon: '🌿',
        description: 'Natural organic forces'
      },
      {
        id: 'crystal',
        name: 'Crystal',
        icon: '💎',
        description: 'Prismatic clarity & precision'
      },
      {
        id: 'shadow',
        name: 'Shadow',
        icon: '🌑',
        description: 'Hidden mysterious power'
      },
      {
        id: 'light',
        name: 'Light',
        icon: '✨',
        description: 'Pure divine radiance'
      },
      {
        id: 'storm',
        name: 'Storm',
        icon: '⚡',
        description: 'Raw electric chaos'
      },
      {
        id: 'void',
        name: 'Void',
        icon: '🕳️',
        description: 'Infinite recursive potential'
      }
    ];

    this.initializeDOMElements();
    this.loadPersistedData();
    this.initializeEventListeners();
    this.updateEnergyGrid();
    this.updateGenerateButton();
    this.initializeParticles();
    this.updateGalleryDisplay();

    console.log('🚀 Sigilcraft app initialized successfully!');
  }

  initializeDOMElements() {
    this.domElements = {
      phraseInput: document.getElementById('phraseInput'),
      generateBtn: document.getElementById('generateBtn'),
      energyGrid: document.getElementById('energyGrid'),
      sigilContainer: document.getElementById('sigilContainer'),
      sigilImage: document.getElementById('sigilImage'),
      sigilInfo: document.getElementById('sigilInfo'),
      galleryContainer: document.getElementById('galleryContainer'),
      unlockSection: document.getElementById('unlockSection'),
      proModal: document.getElementById('proModal'),
      proKeyInput: document.getElementById('proKeyInput'),
      toastContainer: document.getElementById('toastContainer'),
      loadingOverlay: document.getElementById('loadingOverlay'),
      phraseCounter: document.getElementById('phraseCounter')
    };
  }

  loadPersistedData() {
    try {
      const gallery = localStorage.getItem('sigilGallery');
      if (gallery) {
        this.state.sigilGallery = JSON.parse(gallery);
      }

      const proStatus = localStorage.getItem('isPro');
      if (proStatus) {
        this.state.isPro = proStatus === 'true';
      }
    } catch (e) {
      console.warn('Failed to load persisted data:', e);
    }
  }

  initializeEventListeners() {
    if (this.domElements.phraseInput) {
      this.domElements.phraseInput.addEventListener('input', (e) => {
        this.updateCharacterCounter();
        this.updateGenerateButton();
      });

      this.domElements.phraseInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.generateSigil();
        }
      });
    }

    if (this.domElements.generateBtn) {
      this.domElements.generateBtn.addEventListener('click', () => {
        this.generateSigil();
      });
    }

    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('modal')) {
        this.closeModals();
      }
    });

    window.addEventListener('resize', () => {
      this.isMobile = window.innerWidth <= 768;
    });
  }

  updateCharacterCounter() {
    const counter = this.domElements.phraseCounter;
    if (!counter || !this.domElements.phraseInput) return;

    const length = this.domElements.phraseInput.value.length;
    const maxLength = 500;
    
    counter.textContent = `${length}/${maxLength}`;
    
    if (length > maxLength * 0.9) {
      counter.style.color = 'var(--error)';
    } else if (length > maxLength * 0.7) {
      counter.style.color = 'var(--warning)';
    } else {
      counter.style.color = 'var(--text-tertiary)';
    }
  }

  updateEnergyGrid() {
    if (!this.domElements.energyGrid) return;

    const availableEnergies = this.state.isPro ? 
      this.energyTypes : 
      this.energyTypes.slice(0, 3);

    this.domElements.energyGrid.innerHTML = availableEnergies.map(energy => `
      <div class="energy-option ${energy.id === this.state.selectedEnergy ? 'selected' : ''}" 
           data-energy="${energy.id}">
        <div class="energy-icon">${energy.icon}</div>
        <div class="energy-content">
          <div class="energy-name">${energy.name}</div>
          <div class="energy-desc">${energy.description}</div>
        </div>
      </div>
    `).join('');

    this.domElements.energyGrid.querySelectorAll('.energy-option').forEach(option => {
      option.addEventListener('click', () => {
        this.domElements.energyGrid.querySelectorAll('.energy-option').forEach(opt => 
          opt.classList.remove('selected'));

        option.classList.add('selected');
        this.state.selectedEnergy = option.dataset.energy;
        this.vibrate([50]);
      });
    });

    if (this.domElements.unlockSection) {
      this.domElements.unlockSection.style.display = this.state.isPro ? 'none' : 'block';
    }
  }

  async generateSigil() {
    if (this.state.isGenerating || this.state.cooldownActive) return;

    const phrase = this.domElements.phraseInput?.value?.trim();
    if (!phrase) {
      this.showToast('❌ Please enter a phrase');
      return;
    }

    if (phrase.length < 2) {
      this.showToast('❌ Phrase must be at least 2 characters');
      return;
    }

    if (phrase.length > 500) {
      this.showToast('❌ Phrase is too long (max 500 characters)');
      return;
    }

    this.state.isGenerating = true;
    this.updateGenerateButton();
    this.showLoadingOverlay(true);

    try {
      const requestData = {
        phrase: phrase,
        vibe: this.state.selectedEnergy,
        advanced: this.state.isPro
      };

      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `Server error: ${response.status}`);
      }

      this.displaySigil(data);
      this.addToGallery(data);
      this.showToast('✨ Sigil manifested successfully!');

      if (!this.state.isPro) {
        this.startCooldown();
      }

    } catch (error) {
      console.error('Generation error:', error);
      
      if (error.message.includes('timeout')) {
        this.showToast('⏱️ Generation timed out - please try again');
      } else if (error.message.includes('unavailable')) {
        this.showToast('🔧 Service temporarily unavailable');
      } else {
        this.showToast('❌ Failed to generate sigil - please try again');
      }
    } finally {
      this.state.isGenerating = false;
      this.updateGenerateButton();
      this.showLoadingOverlay(false);
    }
  }

  displaySigil(data) {
    if (!this.domElements.sigilContainer) return;

    this.domElements.sigilContainer.style.display = 'block';

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

    const phrase = this.domElements.phraseInput?.value?.trim() || '';
    const isValid = phrase.length >= 2 && phrase.length <= 500;
    const canGenerate = isValid && !this.state.isGenerating && !this.state.cooldownActive;

    this.domElements.generateBtn.disabled = !canGenerate;

    if (this.state.isGenerating) {
      this.domElements.generateBtn.textContent = '🎨 Manifesting...';
    } else if (this.state.cooldownActive) {
      this.domElements.generateBtn.textContent = `⏳ Wait ${this.state.cooldownTimer}s`;
    } else {
      this.domElements.generateBtn.textContent = '🎨 Generate Sigil';
    }
  }

  startCooldown() {
    this.state.cooldownActive = true;
    this.state.cooldownTimer = 10;

    const interval = setInterval(() => {
      this.state.cooldownTimer--;
      this.updateGenerateButton();

      if (this.state.cooldownTimer <= 0) {
        this.state.cooldownActive = false;
        clearInterval(interval);
        this.updateGenerateButton();
      }
    }, 1000);
  }

  addToGallery(data) {
    const galleryItem = {
      id: Date.now(),
      phrase: data.phrase,
      vibe: data.vibe,
      advanced: data.advanced,
      image: data.image,
      timestamp: new Date().toISOString()
    };

    this.state.sigilGallery.unshift(galleryItem);
    this.state.sigilGallery = this.state.sigilGallery.slice(0, 50); // Keep last 50

    try {
      localStorage.setItem('sigilGallery', JSON.stringify(this.state.sigilGallery));
    } catch (e) {
      console.warn('Failed to save to gallery:', e);
    }

    this.updateGalleryDisplay();
  }

  updateGalleryDisplay() {
    if (!this.domElements.galleryContainer) return;

    if (this.state.sigilGallery.length === 0) {
      this.domElements.galleryContainer.innerHTML = `
        <div class="gallery-empty">
          <p>No sigils yet. Generate your first mystical creation!</p>
        </div>
      `;
      return;
    }

    this.domElements.galleryContainer.innerHTML = `
      <div class="gallery-grid">
        ${this.state.sigilGallery.map(item => `
          <div class="gallery-item" data-id="${item.id}">
            <img src="data:image/png;base64,${item.image}" 
                 alt="Sigil: ${item.phrase}" 
                 loading="lazy">
            <div class="gallery-overlay">
              <div class="gallery-info">
                <div class="gallery-phrase">"${item.phrase}"</div>
                <div class="gallery-energy">${item.vibe} energy${item.advanced ? ' • Ultra' : ''}</div>
                <div class="gallery-date">${new Date(item.timestamp).toLocaleDateString()}</div>
              </div>
              <div class="gallery-actions">
                <button class="gallery-btn" onclick="app.downloadGalleryItem(${item.id})" title="Download">
                  📥
                </button>
                <button class="gallery-btn" onclick="app.viewGalleryItem(${item.id})" title="View Full">
                  👁️
                </button>
                <button class="gallery-btn delete" onclick="app.deleteGalleryItem(${item.id})" title="Delete">
                  🗑️
                </button>
              </div>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  downloadGalleryItem(id) {
    const item = this.state.sigilGallery.find(s => s.id === id);
    if (!item) return;

    this.downloadImage(item.image, `sigil-${item.phrase.replace(/[^a-zA-Z0-9]/g, '_')}.png`);
  }

  viewGalleryItem(id) {
    const item = this.state.sigilGallery.find(s => s.id === id);
    if (!item) return;

    this.state.lastGeneratedImage = item;
    this.displaySigil(item);
  }

  deleteGalleryItem(id) {
    if (!confirm('Delete this sigil from your gallery?')) return;

    this.state.sigilGallery = this.state.sigilGallery.filter(s => s.id !== id);
    
    try {
      localStorage.setItem('sigilGallery', JSON.stringify(this.state.sigilGallery));
    } catch (e) {
      console.warn('Failed to update gallery:', e);
    }

    this.updateGalleryDisplay();
    this.showToast('🗑️ Sigil removed from gallery');
  }

  downloadSigil() {
    if (!this.state.lastGeneratedImage) return;

    const filename = `sigil-${this.state.lastGeneratedImage.phrase.replace(/[^a-zA-Z0-9]/g, '_')}.png`;
    this.downloadImage(this.state.lastGeneratedImage.image, filename);
  }

  downloadImage(base64Data, filename) {
    try {
      const link = document.createElement('a');
      link.href = `data:image/png;base64,${base64Data}`;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      this.showToast('📥 Download started!');
    } catch (error) {
      console.error('Download error:', error);
      this.showToast('❌ Download failed');
    }
  }

  shareImage() {
    if (!this.state.lastGeneratedImage) return;

    if (navigator.share) {
      navigator.share({
        title: 'My Sigilcraft Creation',
        text: `Check out my mystical sigil for "${this.state.lastGeneratedImage.phrase}"`,
        url: window.location.href
      }).catch(console.error);
    } else {
      navigator.clipboard.writeText(window.location.href).then(() => {
        this.showToast('🔗 Link copied to clipboard!');
      }).catch(() => {
        this.showToast('❌ Unable to share');
      });
    }
  }

  openProModal() {
    if (this.domElements.proModal) {
      this.domElements.proModal.style.display = 'flex';
    }
  }

  closeModals() {
    if (this.domElements.proModal) {
      this.domElements.proModal.style.display = 'none';
    }
  }

  submitProKey() {
    const key = this.domElements.proKeyInput?.value?.trim();
    if (!key) {
      this.showToast('❌ Please enter a Pro Key');
      return;
    }

    // Simulate key validation (replace with actual validation)
    if (key === 'SIGILCRAFT_PRO_2024') {
      this.state.isPro = true;
      localStorage.setItem('isPro', 'true');
      this.updateEnergyGrid();
      this.closeModals();
      this.showToast('✨ Pro features unlocked!');
    } else {
      this.showToast('❌ Invalid Pro Key');
    }
  }

  showToast(message, type = 'info') {
    if (!this.domElements.toastContainer) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    this.domElements.toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('show');
    }, 100);

    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        if (toast.parentNode) {
          toast.parentNode.removeChild(toast);
        }
      }, 300);
    }, 3000);
  }

  showLoadingOverlay(show) {
    if (this.domElements.loadingOverlay) {
      this.domElements.loadingOverlay.style.display = show ? 'flex' : 'none';
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

  initializeParticles() {
    if (this.isMobile) return;

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
      opacity: 0.3;
    `;

    for (let i = 0; i < 15; i++) {
      const particle = document.createElement('div');
      particle.style.cssText = `
        position: absolute;
        width: 2px;
        height: 2px;
        background: rgba(138, 43, 226, ${Math.random() * 0.6});
        border-radius: 50%;
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        animation: float ${5 + Math.random() * 10}s linear infinite;
        animation-delay: ${Math.random() * 5}s;
      `;
      particleContainer.appendChild(particle);
    }

    document.body.appendChild(particleContainer);
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

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.app = new SigilcraftApp();
  console.log('🚀 Sigilcraft JavaScript loaded successfully!');
});
