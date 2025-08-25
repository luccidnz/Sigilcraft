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
      unlockSection: document.querySelector('.unlock-section')
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

    const availableEnergies = this.state.isPro ? this.energyTypes : this.energyTypes.slice(0, 3);

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

    // Add click handlers
    this.domElements.energyGrid.querySelectorAll('.energy-option').forEach(option => {
      option.addEventListener('click', () => {
        // Remove previous selection
        this.domElements.energyGrid.querySelectorAll('.energy-option').forEach(opt => 
          opt.classList.remove('selected'));

        // Add selection to clicked option
        option.classList.add('selected');
        this.state.selectedEnergy = option.dataset.energy;
        this.vibrate([50]);
      });
    });

    // Show/hide unlock section based on pro status
    if (this.domElements.unlockSection) {
      this.domElements.unlockSection.style.display = this.state.isPro ? 'none' : 'block';
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

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        this.displaySigil(data);
        this.addToGallery(data);
        this.showToast('✨ Ultra-unique sigil manifested!', 'success');

        if (!this.state.isPro) {
          this.startCooldown();
        }
      } else {
        throw new Error(data.error || 'Generation failed');
      }

    } catch (error) {
      console.error('❌ Generation error:', error);
      console.error('Error details:', error.message, error.stack);
      throw error;
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
    if (!this.state.lastGeneratedImage) return;

    const link = document.createElement('a');
    link.href = `data:image/png;base64,${this.state.lastGeneratedImage.image}`;
    const filename = `sigilcraft-${this.state.lastGeneratedImage.phrase.replace(/\s+/g, '-').toLowerCase()}-${this.state.lastGeneratedImage.vibe}.png`;
    link.download = filename;
    link.click();

    this.showToast('📥 Ultra-unique sigil downloaded!', 'success');
  }

  shareImage() {
    if (!this.state.lastGeneratedImage) return;

    if (navigator.share && this.isMobile) {
      // Convert base64 to blob for native sharing
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new Image();

      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);

        canvas.toBlob((blob) => {
          const file = new File([blob], 'sigil.png', { type: 'image/png' });
          navigator.share({
            title: 'My Ultra-Unique Sigil',
            text: `Generated with Sigilcraft: "${this.state.lastGeneratedImage.phrase}"`,
            files: [file]
          });
        });
      };

      img.src = `data:image/png;base64,${this.state.lastGeneratedImage.image}`;
    } else {
      // Fallback: copy image to clipboard
      this.copyImageToClipboard();
    }
  }

  async copyImageToClipboard() {
    try {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new Image();

      img.onload = async () => {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);

        canvas.toBlob(async (blob) => {
          try {
            await navigator.clipboard.write([
              new ClipboardItem({ 'image/png': blob })
            ]);
            this.showToast('📋 Sigil copied to clipboard!', 'success');
          } catch (err) {
            this.showToast('🔗 Use download button to save', 'info');
          }
        });
      };

      img.src = `data:image/png;base64,${this.state.lastGeneratedImage.image}`;
    } catch (error) {
      this.showToast('🔗 Use download button to save', 'info');
    }
  }

  addToGallery(data = null) {
    const sigilData = data || this.state.lastGeneratedImage;
    if (!sigilData) return;

    const galleryItem = {
      id: Date.now(),
      phrase: sigilData.phrase,
      vibe: sigilData.vibe,
      image: sigilData.image,
      advanced: sigilData.advanced || false,
      timestamp: new Date().toISOString()
    };

    this.state.sigilGallery.unshift(galleryItem);

    // Limit gallery size
    if (this.state.sigilGallery.length > 50) {
      this.state.sigilGallery = this.state.sigilGallery.slice(0, 50);
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
          <p>✨ Your ultra-unique sigil gallery awaits...</p>
          <p>Generate your first revolutionary sigil to begin your mystical collection!</p></div>our mystical collection!</p>
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
    const item = this.state.sigilGallery.find(sigil => sigil.id === id);
    if (!item) return;

    const link = document.createElement('a');
    link.href = `data:image/png;base64,${item.image}`;
    link.download = `sigil-${item.phrase.replace(/\s+/g, '-').toLowerCase()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    this.showToast('📥 Sigil downloaded!', 'success');
  }

  viewGalleryItem(id) {
    const item = this.state.sigilGallery.find(sigil => sigil.id === id);
    if (!item) return;

    const modal = document.createElement('div');
    modal.className = 'gallery-modal';
    modal.innerHTML = `
      <div class="gallery-modal-content">
        <span class="gallery-modal-close">&times;</span>
        <img src="data:image/png;base64,${item.image}" alt="Sigil: ${item.phrase}">
        <div class="gallery-modal-info">
          <h3>"${item.phrase}"</h3>
          <p>${item.vibe} energy${item.advanced ? ' • Ultra' : ''}</p>
          <p>Created: ${new Date(item.timestamp).toLocaleString()}</p>
        </div>
      </div>
    `;

    modal.addEventListener('click', (e) => {
      if (e.target === modal || e.target.className === 'gallery-modal-close') {
        document.body.removeChild(modal);
      }
    });

    document.body.appendChild(modal);
  }

  deleteGalleryItem(id) {
    if (!confirm('Delete this sigil from your gallery?')) return;

    this.state.sigilGallery = this.state.sigilGallery.filter(item => item.id !== id);
    localStorage.setItem('sigilcraft_gallery', JSON.stringify(this.state.sigilGallery));
    this.updateGallery();
    this.showToast('🗑️ Sigil deleted', 'info');
  }

  // Missing method implementations
  resetAfterError() {
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
    const item = this.state.sigilGallery.find(i => i.id === id);
    if (!item) return;

    // Set as current image for display
    this.state.lastGeneratedImage = item;
    this.displaySigil(item);
    this.scrollToElement(this.domElements.sigilContainer);
  }

  deleteGalleryItem(id) {
    if (confirm('Delete this sigil from your gallery?')) {
      this.state.sigilGallery = this.state.sigilGallery.filter(item => item.id !== id);
      localStorage.setItem('sigilcraft_gallery', JSON.stringify(this.state.sigilGallery));
      this.updateGallery();
      this.showToast('🗑️ Sigil deleted', 'info');
    }
  }

  updateProStatus() {
    if (this.domElements.proBadge) {
      this.domElements.proBadge.style.display = this.state.isPro ? 'flex' : 'none';
    }

    if (this.domElements.unlockSection) {
      this.domElements.unlockSection.style.display = this.state.isPro ? 'none' : 'block';
    }

    this.renderEnergySelection();
  }

  openProModal() {
    if (this.domElements.proModal) {
      this.domElements.proModal.style.display = 'flex';
      setTimeout(() => {
        if (this.domElements.proKeyInput) {
          this.domElements.proKeyInput.focus();
        }
      }, 100);
    }
  }

  closeModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => modal.style.display = 'none');

    // Clear pro key input
    if (this.domElements.proKeyInput) {
      this.domElements.proKeyInput.value = '';
    }
  }

  submitProKey() {
    if (!this.domElements.proKeyInput) return;

    const key = this.domElements.proKeyInput.value.trim();
    const validKeys = ['changeme_super_secret', 'sigilcraft_pro_2024', 'ultra_revolutionary'];

    if (validKeys.includes(key)) {
      this.state.isPro = true;
      localStorage.setItem('sigilcraft_pro', 'true');
      this.updateProStatus();
      this.closeModals();
      this.showToast('✨ Pro features activated! All energies unlocked!', 'success');
      this.vibrate([100, 50, 100, 50, 100]);
    } else {
      this.showToast('❌ Invalid pro key. Try: changeme_super_secret', 'error');
      this.domElements.proKeyInput.value = '';
    }
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
        <div class="analysis-prompt">
          <h4>📊 Ultra-Advanced Text Analysis</h4>
          <p>Enter a phrase to see how it will create your ultra-unique sigil...</p>
        </div>
      `;
      return;
    }

    const analysis = this.performAdvancedTextAnalysis(text);

    this.domElements.textAnalysis.innerHTML = `
      <h4>📊 Ultra-Advanced Text Analysis</h4>
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
          <span class="label">Unique Letters</span>
          <span class="value">${analysis.uniqueLetters}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Vowel Flow</span>
          <span class="value">${analysis.vowelRatio}%</span>
        </div>
        <div class="analysis-item">
          <span class="label">Energy Signature</span>
          <span class="value">${analysis.energySignature}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Uniqueness</span>
          <span class="value complexity-${analysis.uniquenessLevel}">${analysis.uniquenessLevel}</span>
        </div>
      </div>
      <div class="semantic-analysis">
        <div class="semantic-item">
          <span class="label">🎯 Predicted Vibe:</span>
          <span class="value predicted-${analysis.predictedVibe}">${analysis.predictedVibe}</span>
        </div>
        <div class="semantic-item">
          <span class="label">🔮 Manifestation Pattern:</span>
          <span class="value">${analysis.manifestationPattern}</span>
        </div>
        ${analysis.semanticMatches.length > 0 ? `
        <div class="semantic-matches">
          <span class="label">✨ Detected Archetypes:</span>
          <div class="archetype-tags">
            ${analysis.semanticMatches.map(match => 
              `<span class="archetype-tag">${match}</span>`).join('')}g">${match}</span>`
            ).join('')}
          </div>
        </div>
        ` : ''}
      </div>
    `;
  }

  performAdvancedTextAnalysis(text) {
    const words = text.trim().split(/\s+/);
    const chars = text.replace(/\s/g, '');
    const vowels = chars.match(/[aeiouAEIOU]/g) || [];
    const consonants = chars.match(/[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]/g) || [];
    const uniqueLetters = new Set(chars.toLowerCase().match(/[a-z]/g) || []).size;

    // Advanced metrics
    const vowelRatio = Math.round((vowels.length / chars.length) * 100) || 0;
    const wordVariety = new Set(words.map(w => w.toLowerCase())).size;
    const avgWordLength = words.reduce((sum, word) => sum + word.length, 0) / words.length;

    // Energy signature calculation
    let energyValue = 0;
    for (const char of text.toLowerCase()) {
      energyValue += char.charCodeAt(0);
    }
    const energySignature = (energyValue % 999).toString().padStart(3, '0');

    // Uniqueness level
    let uniquenessLevel = 'Simple';
    const complexityScore = (wordVariety * uniqueLetters * avgWordLength) / Math.max(1, words.length);

    if (complexityScore > 15) uniquenessLevel = 'Profound';
    else if (complexityScore > 10) uniquenessLevel = 'Complex';
    else if (complexityScore > 5) uniquenessLevel = 'Moderate';

    // Semantic analysis
    const archetypes = {
      'love': ['love', 'heart', 'romance', 'passion', 'affection'],
      'power': ['power', 'strength', 'force', 'might', 'energy'],
      'peace': ['peace', 'calm', 'tranquil', 'serenity', 'harmony'],
      'abundance': ['money', 'wealth', 'abundance', 'prosperity', 'rich'],
      'wisdom': ['wisdom', 'knowledge', 'understanding', 'insight', 'truth'],
      'protection': ['protect', 'shield', 'guard', 'safe', 'secure'],
      'manifestation': ['manifest', 'create', 'bring', 'attract', 'draw'],
      'consciousness': ['conscious', 'aware', 'mindful', 'present', 'awake'],
      'transformation': ['change', 'transform', 'evolve', 'grow', 'shift'],
      'healing': ['heal', 'cure', 'restore', 'renewal', 'regenerate']
    };

    const semanticMatches = [];
    const lowerText = text.toLowerCase();

    for (const [archetype, keywords] of Object.entries(archetypes)) {
      if (keywords.some(keyword => lowerText.includes(keyword))) {
        semanticMatches.push(archetype);
      }
    }

    // Predict vibe based on content
    let predictedVibe = 'mystical';
    if (lowerText.includes('star') || lowerText.includes('space') || lowerText.includes('cosmic')) predictedVibe = 'cosmic';
    if (lowerText.includes('nature') || lowerText.includes('earth') || lowerText.includes('tree')) predictedVibe = 'elemental';
    if (lowerText.includes('light') || lowerText.includes('bright') || lowerText.includes('sun')) predictedVibe = 'light';
    if (lowerText.includes('shadow') || lowerText.includes('dark') || lowerText.includes('night')) predictedVibe = 'shadow';
    if (lowerText.includes('crystal') || lowerText.includes('gem') || lowerText.includes('diamond')) predictedVibe = 'crystal';
    if (lowerText.includes('storm') || lowerText.includes('thunder') || lowerText.includes('lightning')) predictedVibe = 'storm';
    if (lowerText.includes('void') || lowerText.includes('empty') || lowerText.includes('infinite')) predictedVibe = 'void';

    // Manifestation pattern
    const patterns = ['spiral', 'radial', 'flowing', 'geometric', 'organic', 'crystalline', 'chaotic', 'harmonic'];
    const manifestationPattern = patterns[energyValue % patterns.length];

    return {
      wordCount: words.length,
      charCount: chars.length,
      uniqueLetters,
      vowelRatio,
      energySignature,
      uniquenessLevel,
      semanticMatches,
      predictedVibe,
      manifestationPattern,
      complexityScore: Math.round(complexityScore * 10) / 10
    };
  }

  debouncedAnalysis = this.debounce((text) => {
    // Advanced analysis for real-time feedback
    this.updateTextAnalysis(text);
  }, 300);

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

  showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add('show'), 100);
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        if (document.body.contains(toast)) {
          document.body.removeChild(toast);
        }
      }, 300);
    }, 4000);
  }

  initializeMobileOptimizations() {
    if (this.isMobile) {
      const setVH = () => {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
      };

      setVH();
      window.addEventListener('resize', setVH);
      window.addEventListener('orientationchange', () => setTimeout(setVH, 100));

      document.body.classList.add('mobile');
      document.addEventListener('touchstart', () => {}, { passive: true });
    }
  }

  handleViewportResize() {
    this.isMobile = window.innerWidth <= 768;

    clearTimeout(this.resizeTimeout);
    this.resizeTimeout = setTimeout(() => {
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

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }

  updateCharCounter() {
    const counter = document.querySelector('.char-counter');
    if (counter && this.domElements.phraseInput) {
      const length = this.domElements.phraseInput.value.length;
      counter.textContent = `${length}/500`;

      if (length > 450) {
        counter.style.color = 'var(--error)';
      } else if (length > 400) {
        counter.style.color = 'var(--warning)';
      } else {
        counter.style.color = 'var(--text-tertiary)';
      }
    }
  }

  initializeParticles() {
    // Simplified particles for better performance
    if (this.isMobile) return; // Skip on mobile for performance

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

    // Reduced particle count for better performance
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

  // Placeholder for the updateUI method, assuming it exists elsewhere or will be implemented.
  // If this method is intended to be part of this class, it should be defined.
  updateUI() {
    // This method needs to be implemented to update the UI elements after an error.
    // For now, it's a placeholder.
  }

  // Placeholder for the showError method, assuming it exists elsewhere or will be implemented.
  // If this method is intended to be part of this class, it should be defined.
  showError(message) {
    // This method needs to be implemented to display error messages to the user.
    // For now, it's a placeholder.
    this.showToast(message, 'error');
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
};.app.submitProKey();
  }
};

// Initialize the application
window.app = new SigilcraftApp();

// CSS for animations
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

console.log('🚀 Sigilcraft JavaScript loaded successfully!');