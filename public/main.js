
// ===== SIGILCRAFT: REVOLUTIONARY SIGIL GENERATOR =====
// Advanced JavaScript with modern ES6+ features and enhanced functionality

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

    this.init();
  }

  init() {
    document.addEventListener('DOMContentLoaded', () => {
      this.initializeDOM();
      this.setupEventListeners();
      this.renderEnergySelection();
      this.updateGallery();
      this.checkProStatus();
      this.initializeAnimations();
    });
  }

  initializeDOM() {
    this.domElements = {
      intentInput: document.getElementById('intentInput'),
      generateBtn: document.getElementById('generateBtn'),
      downloadBtn: document.getElementById('downloadBtn'),
      charCounter: document.getElementById('charCounter'),
      textAnalysis: document.getElementById('textAnalysis'),
      sigilDisplay: document.getElementById('sigilDisplay'),
      energyGrid: document.getElementById('energyGrid'),
      galleryGrid: document.getElementById('galleryGrid'),
      proBadge: document.getElementById('proBadge'),
      proModal: document.getElementById('proModal'),
      toast: document.getElementById('toast')
    };
  }

  setupEventListeners() {
    // Mobile detection
    this.isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    this.isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);

    // Input handling
    if (this.domElements.intentInput) {
      this.domElements.intentInput.addEventListener('input', () => this.handleTextInput());
      
      // Mobile-friendly Enter key handling
      this.domElements.intentInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey && !this.isMobile) {
          e.preventDefault();
          this.generateSigil();
        }
      });

      // Prevent zoom on focus for iOS
      if (this.isMobile) {
        this.domElements.intentInput.addEventListener('focus', () => {
          if (window.innerWidth < 768) {
            this.domElements.intentInput.style.fontSize = '16px';
          }
        });
      }
    }

    // Generation button with touch feedback
    if (this.domElements.generateBtn) {
      this.domElements.generateBtn.addEventListener('click', () => this.generateSigil());
      
      if (this.isTouchDevice) {
        this.domElements.generateBtn.addEventListener('touchstart', (e) => {
          e.target.style.transform = 'scale(0.98)';
        });
        
        this.domElements.generateBtn.addEventListener('touchend', (e) => {
          setTimeout(() => {
            e.target.style.transform = '';
          }, 150);
        });
      }
    }

    // Download button
    if (this.domElements.downloadBtn) {
      this.domElements.downloadBtn.addEventListener('click', () => this.downloadSigil());
    }

    // Pro key submission
    const proKeyInput = document.getElementById('proKeyInput');
    if (proKeyInput) {
      proKeyInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          this.submitProKey();
        }
      });
    }

    // Modal close events with touch support
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('modal')) {
        this.closeModals();
      }
    });

    // Keyboard shortcuts (disabled on mobile)
    if (!this.isMobile) {
      document.addEventListener('keydown', (e) => {
        if (e.ctrlKey || e.metaKey) {
          switch (e.key) {
            case 'Enter':
              e.preventDefault();
              this.generateSigil();
              break;
            case 's':
              e.preventDefault();
              this.downloadSigil();
              break;
          }
        }
      });
    }

    // Handle orientation changes
    window.addEventListener('orientationchange', () => {
      setTimeout(() => {
        this.handleOrientationChange();
      }, 500);
    });

    // Handle viewport resize for mobile browsers
    let resizeTimeout;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        this.handleViewportResize();
      }, 250);
    });

    // Prevent double-tap zoom on specific elements
    if (this.isTouchDevice) {
      const preventDoubleTap = (e) => {
        e.preventDefault();
        e.target.click();
      };

      document.querySelectorAll('.btn, .energy-option, .gallery-btn').forEach(el => {
        el.addEventListener('touchend', preventDoubleTap);
      });
    }

    // Add pull-to-refresh prevention
    document.body.addEventListener('touchstart', e => {
      if (e.touches.length === 1 && window.scrollY === 0) {
        e.preventDefault();
      }
    }, { passive: false });
  }

  async generateSigil() {
    const phrase = this.domElements.intentInput?.value?.trim();
    
    if (!phrase) {
      this.showToast('⚠️ Please enter your intention first', 'warning');
      this.vibrate([100, 50, 100]);
      return;
    }

    if (this.state.cooldownActive && !this.state.isPro) {
      this.showToast('⏳ Please wait for cooldown', 'warning');
      this.vibrate([200]);
      return;
    }

    if (this.state.isGenerating) return;

    // Haptic feedback on generation start
    this.vibrate([50]);

    this.state.isGenerating = true;
    this.updateGenerateButton();

    const selectedEnergy = document.querySelector('.energy-option.selected')?.dataset?.vibe || 'mystical';

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          phrase, 
          vibe: selectedEnergy,
          advanced: this.state.isPro 
        })
      });

      if (!response.ok) {
        throw new Error(`Generation failed: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        const sigilData = {
          image: data.image,
          phrase,
          vibe: selectedEnergy,
          timestamp: Date.now(),
          id: Date.now()
        };

        this.displaySigil(sigilData);
        
        this.showToast('✨ Revolutionary sigil manifested!', 'success');
        this.vibrate([100, 50, 100, 50, 100]); // Success vibration pattern
        
        // Scroll to result on mobile
        if (this.isMobile && this.domElements.sigilDisplay) {
          setTimeout(() => {
            this.scrollToElement(this.domElements.sigilDisplay, 20);
          }, 300);
        }
        
        if (!this.state.isPro) {
          this.startCooldown();
        }
      } else {
        throw new Error(data.error || 'Generation failed');
      }
    } catch (error) {
      console.error('Generation error:', error);
      this.showToast(`❌ ${error.message}`, 'error');
      this.vibrate([200, 100, 200]); // Error vibration pattern
    } finally {
      this.state.isGenerating = false;
      this.updateGenerateButton();
    }
  }

  displaySigil(sigilData) {
    if (!this.domElements.sigilDisplay) return;

    this.state.lastGeneratedImage = sigilData.image;
    
    // Add to gallery
    this.state.sigilGallery.unshift(sigilData);
    if (this.state.sigilGallery.length > 20) {
      this.state.sigilGallery = this.state.sigilGallery.slice(0, 20);
    }
    
    localStorage.setItem('sigilcraft_gallery', JSON.stringify(this.state.sigilGallery));

    // Display current sigil
    this.domElements.sigilDisplay.innerHTML = `
      <div class="sigil-container">
        <img src="data:image/png;base64,${sigilData.image}" alt="Generated Sigil" class="sigil-image">
        <div class="sigil-info">
          <h3>"${sigilData.phrase}"</h3>
          <p class="sigil-vibe">${sigilData.vibe} energy</p>
        </div>
      </div>
    `;

    this.updateGallery();
    
    if (this.domElements.downloadBtn) {
      this.domElements.downloadBtn.style.display = 'block';
    }
  }

  downloadSigil() {
    if (!this.state.lastGeneratedImage) {
      this.showToast('⚠️ No sigil to download', 'warning');
      return;
    }

    try {
      const link = document.createElement('a');
      link.href = `data:image/png;base64,${this.state.lastGeneratedImage}`;
      link.download = `revolutionary-sigil-${Date.now()}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      this.showToast('📥 Sigil downloaded successfully!', 'success');
    } catch (error) {
      console.error('Download error:', error);
      this.showToast('❌ Download failed', 'error');
    }
  }

  handleTextInput() {
    this.updateCharCounter();
    this.analyzeText();
  }

  updateCharCounter() {
    if (!this.domElements.charCounter || !this.domElements.intentInput) return;

    const count = this.domElements.intentInput.value.length;
    const maxChars = this.state.isPro ? 500 : 200;
    
    this.domElements.charCounter.textContent = `${count}/${maxChars} characters`;

    if (count > maxChars * 0.8) {
      this.domElements.charCounter.style.color = '#ff6b6b';
    } else {
      this.domElements.charCounter.style.color = 'var(--text-secondary)';
    }

    if (count > maxChars) {
      this.domElements.intentInput.value = this.domElements.intentInput.value.substring(0, maxChars);
    }
  }

  analyzeText() {
    if (!this.domElements.textAnalysis || !this.domElements.intentInput) return;

    const text = this.domElements.intentInput.value.trim();

    if (!text) {
      this.domElements.textAnalysis.innerHTML = `
        <h4>📊 Text Analysis</h4>
        <p class="analysis-prompt">Enter text above to see mystical analysis...</p>
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
    const words = text.split(/\s+/).filter(word => word.length > 0);
    const chars = text.length;
    const vowels = (text.match(/[aeiouAEIOU]/g) || []).length;
    const consonants = (text.match(/[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]/g) || []).length;
    const uniqueLetters = new Set(text.toLowerCase().match(/[a-z]/g) || []).size;
    
    let complexity = 'Simple';
    if (words.length > 5) complexity = 'Medium';
    if (words.length > 10) complexity = 'Complex';
    if (words.length > 20) complexity = 'Profound';

    // Predict energy based on text characteristics
    const energyScore = {
      mystical: vowels * 2 + (text.match(/[aeiou]/g) || []).length,
      cosmic: (text.match(/[xyz]/gi) || []).length * 3 + uniqueLetters,
      elemental: consonants + (text.match(/[rlmnw]/gi) || []).length,
      crystal: uniqueLetters * 2,
      shadow: (text.match(/[kmptv]/gi) || []).length * 2,
      light: vowels + (text.match(/[aeio]/gi) || []).length,
      storm: (text.match(/[ckqxz]/gi) || []).length * 4,
      void: Math.abs(vowels - consonants)
    };

    const predictedEnergy = Object.keys(energyScore).reduce((a, b) => 
      energyScore[a] > energyScore[b] ? a : b
    );

    return {
      wordCount: words.length,
      charCount: chars,
      vowelCount: vowels,
      consonantCount: consonants,
      uniqueLetters,
      complexity,
      predictedEnergy
    };
  }

  renderEnergySelection() {
    if (!this.domElements.energyGrid) return;

    const availableEnergies = this.state.isPro ? this.energyTypes : this.energyTypes.slice(0, 3);

    this.domElements.energyGrid.innerHTML = availableEnergies.map((energy, index) => `
      <div class="energy-option ${index === 0 ? 'selected' : ''}" 
           data-vibe="${energy.id}" 
           onclick="app.selectEnergy('${energy.id}')"
           role="button"
           tabindex="0"
           aria-label="Select ${energy.name} energy: ${energy.description}">
        <i role="img" aria-label="${energy.name} icon">${energy.icon}</i>
        <div class="energy-text">
          <span class="energy-name">${energy.name}</span>
          <span class="energy-desc">${energy.description}</span>
        </div>
      </div>
    `).join('');

    // Add keyboard navigation for energy options
    document.querySelectorAll('.energy-option').forEach(option => {
      option.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          option.click();
        }
      });
    });
  }

  selectEnergy(vibeId) {
    document.querySelectorAll('.energy-option').forEach(option => {
      option.classList.remove('selected');
    });
    
    const selectedOption = document.querySelector(`[data-vibe="${vibeId}"]`);
    if (selectedOption) {
      selectedOption.classList.add('selected');
    }
  }

  updateGallery() {
    if (!this.domElements.galleryGrid) return;

    if (this.state.sigilGallery.length === 0) {
      this.domElements.galleryGrid.innerHTML = `
        <div class="no-gallery">
          <p>🎨 No sigils created yet. Generate your first revolutionary sigil above!</p>
        </div>
      `;
      return;
    }

    this.domElements.galleryGrid.innerHTML = this.state.sigilGallery.map(sigil => `
      <div class="gallery-item" 
           onclick="app.viewGalleryItem(${sigil.id})"
           role="button"
           tabindex="0"
           aria-label="View sigil: ${sigil.phrase}">
        <img src="data:image/png;base64,${sigil.image}" 
             alt="Sigil for '${sigil.phrase}'"
             loading="lazy">
        <div class="gallery-overlay">
          <div class="gallery-info">
            <div class="gallery-phrase" title="${sigil.phrase}">"${this.truncateText(sigil.phrase, this.isMobile ? 30 : 50)}"</div>
            <div class="gallery-energy">${sigil.vibe}</div>
            <div class="gallery-date">${new Date(sigil.timestamp).toLocaleDateString()}</div>
          </div>
          <div class="gallery-actions">
            <button class="gallery-btn" 
                    onclick="event.stopPropagation(); app.downloadGalleryItem(${sigil.id})"
                    aria-label="Download sigil"
                    title="Download">
              📥
            </button>
            <button class="gallery-btn delete" 
                    onclick="event.stopPropagation(); app.deleteGalleryItem(${sigil.id})"
                    aria-label="Delete sigil"
                    title="Delete">
              🗑️
            </button>
          </div>
        </div>
      </div>
    `).join('');

    // Add keyboard navigation for gallery items
    document.querySelectorAll('.gallery-item').forEach(item => {
      item.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          item.click();
        }
      });
    });
  }

  truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength - 3) + '...';
  }

  viewGalleryItem(itemId) {
    const item = this.state.sigilGallery.find(sigil => sigil.id == itemId);
    if (item) {
      this.displaySigil(item);
    }
  }

  downloadGalleryItem(itemId) {
    const item = this.state.sigilGallery.find(sigil => sigil.id == itemId);
    if (item) {
      const link = document.createElement('a');
      link.href = `data:image/png;base64,${item.image}`;
      link.download = `sigil-${item.phrase.replace(/[^a-zA-Z0-9]/g, '-')}-${itemId}.png`;
      link.click();
      this.showToast('📥 Gallery sigil downloaded!', 'success');
    }
  }

  deleteGalleryItem(itemId) {
    if (confirm('Delete this sigil from your gallery?')) {
      this.state.sigilGallery = this.state.sigilGallery.filter(sigil => sigil.id != itemId);
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
      this.updateCooldownDisplay(timeLeft);

      if (timeLeft <= 0) {
        clearInterval(timer);
        this.state.cooldownActive = false;
        this.updateCooldownDisplay(0);
        this.updateGenerateButton();
      }
    }, 1000);

    this.updateGenerateButton();
  }

  updateCooldownDisplay(timeLeft) {
    if (this.domElements.generateBtn && timeLeft > 0) {
      this.domElements.generateBtn.textContent = `⏳ Wait ${timeLeft}s (Get Pro for unlimited)`;
      this.domElements.generateBtn.disabled = true;
    }
  }

  updateGenerateButton() {
    if (!this.domElements.generateBtn) return;

    if (this.state.isGenerating) {
      this.domElements.generateBtn.textContent = 'Channeling Revolutionary Energies...';
      this.domElements.generateBtn.disabled = true;
      this.domElements.generateBtn.classList.add('generating');
    } else if (this.state.cooldownActive) {
      this.domElements.generateBtn.disabled = true;
      this.domElements.generateBtn.classList.remove('generating');
    } else {
      this.domElements.generateBtn.textContent = '🚀 Generate Revolutionary Sigil';
      this.domElements.generateBtn.disabled = false;
      this.domElements.generateBtn.classList.remove('generating');
    }
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

  initializeAnimations() {
    // Reduce particles on mobile for performance
    if (!this.isMobile) {
      this.createParticles();
    }
    
    // Add smooth scroll behavior
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Initialize intersection observer for animations (reduced on mobile)
    const observerOptions = {
      threshold: this.isMobile ? 0.1 : 0.3,
      rootMargin: this.isMobile ? '20px' : '50px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
        }
      });
    }, observerOptions);

    document.querySelectorAll('.card, .energy-option, .gallery-item').forEach(el => {
      observer.observe(el);
    });
  }

  handleOrientationChange() {
    // Force layout recalculation on orientation change
    document.body.style.height = '100vh';
    setTimeout(() => {
      document.body.style.height = 'auto';
    }, 100);

    // Update gallery layout if needed
    this.updateGallery();
  }

  handleViewportResize() {
    // Handle mobile browser address bar changes
    if (this.isMobile) {
      const vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty('--vh', `${vh}px`);
    }
  }

  // Mobile-optimized vibration feedback
  vibrate(pattern = [50]) {
    if (navigator.vibrate && this.isMobile) {
      navigator.vibrate(pattern);
    }
  }

  // Optimized scroll to element for mobile
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

  createParticles() {
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

// Export for global access
window.app = app;

console.log('🚀 Sigilcraft JavaScript loaded successfully!');
