
class SigilcraftApp {
  constructor() {
    this.currentSigil = null;
    this.energies = {};
    this.selectedVibe = 'mystical';
    this.init();
  }

  async init() {
    console.log('🔮 Initializing Sigilcraft App...');
    this.setupEventListeners();
    await this.loadEnergyVibes();
    this.setupCharCounter();
    this.setupTextAnalysis();
  }

  setupEventListeners() {
    const phraseInput = document.getElementById('phraseInput');
    const generateBtn = document.getElementById('generateBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const shareBtn = document.getElementById('shareBtn');

    if (phraseInput) {
      phraseInput.addEventListener('input', () => {
        this.updateCharCounter();
        this.analyzeText();
      });
    }

    if (generateBtn) {
      generateBtn.addEventListener('click', () => this.generateSigil());
    }

    if (downloadBtn) {
      downloadBtn.addEventListener('click', () => this.downloadSigil());
    }

    if (shareBtn) {
      shareBtn.addEventListener('click', () => this.shareSigil());
    }

    // Energy selection
    document.addEventListener('click', (e) => {
      if (e.target.closest('.energy-card')) {
        const card = e.target.closest('.energy-card');
        const vibe = card.dataset.vibe;
        if (vibe) {
          this.selectEnergyVibe(vibe);
        }
      }
    });
  }

  async loadEnergyVibes() {
    try {
      const response = await fetch('/api/vibes');
      const data = await response.json();

      if (data.success) {
        this.energies = data.descriptions || {};
        this.renderEnergyGrid(data.vibes || []);
      }
    } catch (error) {
      console.error('Failed to load energy vibes:', error);
      this.renderFallbackEnergyGrid();
    }
  }

  renderEnergyGrid(vibes) {
    const grid = document.getElementById('energyGrid');
    if (!grid) return;

    const energyIcons = {
      'mystical': '🔮',
      'cosmic': '🌌',
      'elemental': '🌿',
      'crystal': '💎',
      'shadow': '🌑',
      'light': '☀️',
      'storm': '⚡',
      'void': '🌀'
    };

    grid.innerHTML = vibes.map(vibe => `
      <div class="energy-card ${vibe === this.selectedVibe ? 'selected' : ''}" data-vibe="${vibe}">
        <div class="energy-icon">${energyIcons[vibe] || '✨'}</div>
        <div class="energy-name">${vibe.charAt(0).toUpperCase() + vibe.slice(1)}</div>
        <div class="energy-description">${this.energies[vibe] || 'Mystical energy'}</div>
      </div>
    `).join('');
  }

  renderFallbackEnergyGrid() {
    const fallbackVibes = ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light', 'storm', 'void'];
    const fallbackDescriptions = {
      'mystical': 'Ancient wisdom & sacred geometry',
      'cosmic': 'Universal stellar connection',
      'elemental': 'Natural organic forces',
      'crystal': 'Prismatic geometric precision',
      'shadow': 'Hidden mysterious power',
      'light': 'Pure divine radiance',
      'storm': 'Raw electric chaos',
      'void': 'Infinite recursive potential'
    };
    this.energies = fallbackDescriptions;
    this.renderEnergyGrid(fallbackVibes);
  }

  selectEnergyVibe(vibe) {
    this.selectedVibe = vibe;
    
    // Update UI
    document.querySelectorAll('.energy-card').forEach(card => {
      card.classList.remove('selected');
    });
    
    const selectedCard = document.querySelector(`[data-vibe="${vibe}"]`);
    if (selectedCard) {
      selectedCard.classList.add('selected');
    }

    console.log(`🎯 Selected energy vibe: ${vibe}`);
  }

  setupCharCounter() {
    this.updateCharCounter();
  }

  updateCharCounter() {
    const phraseInput = document.getElementById('phraseInput');
    const charCounter = document.getElementById('charCounter');
    
    if (phraseInput && charCounter) {
      const currentLength = phraseInput.value.length;
      charCounter.textContent = `${currentLength}/500`;
      
      if (currentLength > 450) {
        charCounter.style.color = '#ff6b6b';
      } else if (currentLength > 350) {
        charCounter.style.color = '#ffd93d';
      } else {
        charCounter.style.color = '#6bcf7f';
      }
    }
  }

  setupTextAnalysis() {
    this.analyzeText();
  }

  analyzeText() {
    const phraseInput = document.getElementById('phraseInput');
    const analysisDiv = document.getElementById('textAnalysis');
    
    if (!phraseInput || !analysisDiv) return;

    const text = phraseInput.value.trim();
    if (!text) {
      analysisDiv.style.display = 'none';
      return;
    }

    analysisDiv.style.display = 'block';
    
    const words = text.split(/\s+/).filter(word => word.length > 0);
    const chars = text.length;
    const vowels = (text.match(/[aeiouAEIOU]/g) || []).length;
    const consonants = (text.match(/[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]/g) || []).length;

    analysisDiv.innerHTML = `
      <h4>✨ Text Analysis</h4>
      <div class="analysis-grid">
        <div class="analysis-item">
          <span class="analysis-label">Words:</span>
          <span class="analysis-value">${words.length}</span>
        </div>
        <div class="analysis-item">
          <span class="analysis-label">Characters:</span>
          <span class="analysis-value">${chars}</span>
        </div>
        <div class="analysis-item">
          <span class="analysis-label">Vowels:</span>
          <span class="analysis-value">${vowels}</span>
        </div>
        <div class="analysis-item">
          <span class="analysis-label">Consonants:</span>
          <span class="analysis-value">${consonants}</span>
        </div>
      </div>
    `;
  }

  async generateSigil() {
    const phraseInput = document.getElementById('phraseInput');
    const generateBtn = document.getElementById('generateBtn');
    const sigilResult = document.getElementById('sigilResult');
    const loadingDiv = document.getElementById('loading');
    
    if (!phraseInput || !generateBtn) return;

    const phrase = phraseInput.value.trim();
    if (!phrase) {
      this.showToast('Please enter a phrase or intention', 'warning');
      return;
    }

    if (phrase.length < 2) {
      this.showToast('Phrase must be at least 2 characters long', 'warning');
      return;
    }

    // Update UI for loading state
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Manifesting...';
    
    if (loadingDiv) {
      loadingDiv.style.display = 'block';
    }
    
    if (sigilResult) {
      sigilResult.style.display = 'none';
    }

    try {
      console.log(`🎨 Generating sigil for: "${phrase}" with vibe: ${this.selectedVibe}`);

      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          phrase: phrase,
          vibe: this.selectedVibe,
          advanced: false
        })
      });

      const data = await response.json();

      if (data.success) {
        this.currentSigil = data;
        this.displaySigil(data);
        this.showToast('Revolutionary sigil manifested successfully!', 'success');
      } else {
        throw new Error(data.error || 'Generation failed');
      }

    } catch (error) {
      console.error('Generation error:', error);
      this.showToast(`Generation failed: ${error.message}`, 'error');
    } finally {
      // Reset UI
      generateBtn.disabled = false;
      generateBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Sigil';
      
      if (loadingDiv) {
        loadingDiv.style.display = 'none';
      }
    }
  }

  displaySigil(data) {
    const sigilResult = document.getElementById('sigilResult');
    const sigilImage = document.getElementById('sigilImage');
    const sigilInfo = document.getElementById('sigilInfo');
    
    if (!sigilResult || !sigilImage) return;

    // Display the sigil image
    sigilImage.src = `data:image/png;base64,${data.image}`;
    sigilImage.alt = `Sigil for: ${data.phrase}`;

    // Update sigil info
    if (sigilInfo) {
      sigilInfo.innerHTML = `
        <div class="sigil-details">
          <h3>✨ Your Revolutionary Sigil</h3>
          <p><strong>Phrase:</strong> "${data.phrase}"</p>
          <p><strong>Energy Vibe:</strong> ${data.vibe.charAt(0).toUpperCase() + data.vibe.slice(1)}</p>
          <p><strong>Generated:</strong> ${new Date().toLocaleString()}</p>
        </div>
      `;
    }

    // Show the result
    sigilResult.style.display = 'block';
    
    // Scroll to result
    sigilResult.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  downloadSigil() {
    if (!this.currentSigil || !this.currentSigil.image) {
      this.showToast('No sigil to download. Please generate a sigil first.', 'warning');
      return;
    }

    try {
      const link = document.createElement('a');
      link.href = `data:image/png;base64,${this.currentSigil.image}`;
      link.download = `sigil-${this.currentSigil.phrase.replace(/[^a-zA-Z0-9]/g, '-').toLowerCase()}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      this.showToast('Sigil downloaded successfully!', 'success');
    } catch (error) {
      console.error('Download error:', error);
      this.showToast('Failed to download sigil', 'error');
    }
  }

  shareSigil() {
    if (navigator.share) {
      navigator.share({
        title: 'My Revolutionary Sigil',
        text: 'Check out this mystical sigil I created!',
        url: window.location.href
      }).catch(err => console.log('Error sharing:', err));
    } else {
      // Fallback: copy URL to clipboard
      navigator.clipboard.writeText(window.location.href).then(() => {
        this.showToast('URL copied to clipboard!', 'success');
      }).catch(() => {
        this.showToast('Unable to share', 'error');
      });
    }
  }

  showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => {
        if (document.body.contains(toast)) {
          document.body.removeChild(toast);
        }
      }, 300);
    }, 3000);
  }
}

// Initialize the application
const app = new SigilcraftApp();

// Add global error handler
window.addEventListener('error', (event) => {
  console.error('Global error:', event.error);
  if (window.app) {
    window.app.showToast('An unexpected error occurred', 'error');
  }
});

// Make app globally accessible for debugging
window.app = app;
