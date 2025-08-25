
// Sigilcraft Enhanced Frontend
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
    
    if (phraseInput) {
      phraseInput.addEventListener('input', () => {
        this.updateCharCounter();
        this.analyzeText();
      });
    }

    if (generateBtn) {
      generateBtn.addEventListener('click', () => this.generateSigil());
    }
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
      'void': '🕳️'
    };

    grid.innerHTML = vibes.map(vibe => `
      <div class="energy-option ${vibe === this.selectedVibe ? 'selected' : ''}" 
           data-vibe="${vibe}">
        <div class="energy-icon">${energyIcons[vibe] || '✨'}</div>
        <div class="energy-content">
          <div class="energy-name">${vibe.charAt(0).toUpperCase() + vibe.slice(1)}</div>
          <div class="energy-desc">${this.energies[vibe] || 'Mystical energy'}</div>
        </div>
      </div>
    `).join('');

    // Add click listeners
    grid.querySelectorAll('.energy-option').forEach(option => {
      option.addEventListener('click', () => {
        this.selectEnergyVibe(option.dataset.vibe);
      });
    });
  }

  renderFallbackEnergyGrid() {
    const fallbackVibes = ['mystical', 'cosmic', 'elemental', 'crystal'];
    this.renderEnergyGrid(fallbackVibes);
  }

  selectEnergyVibe(vibe) {
    this.selectedVibe = vibe;
    
    // Update UI
    document.querySelectorAll('.energy-option').forEach(option => {
      option.classList.toggle('selected', option.dataset.vibe === vibe);
    });
  }

  setupCharCounter() {
    this.updateCharCounter();
  }

  updateCharCounter() {
    const input = document.getElementById('phraseInput');
    const counter = document.getElementById('charCounter');
    
    if (input && counter) {
      const length = input.value.length;
      counter.textContent = `${length}/500`;
      
      if (length > 450) {
        counter.style.color = 'var(--error)';
      } else if (length > 350) {
        counter.style.color = 'var(--warning)';
      } else {
        counter.style.color = 'var(--text-tertiary)';
      }
    }
  }

  setupTextAnalysis() {
    this.analyzeText();
  }

  analyzeText() {
    const input = document.getElementById('phraseInput');
    const analysisDiv = document.getElementById('textAnalysis');
    
    if (!input || !analysisDiv) return;
    
    const text = input.value.trim();
    
    if (text.length === 0) {
      analysisDiv.innerHTML = `
        <h4>✨ Text Analysis</h4>
        <div class="analysis-prompt">Enter text above to see detailed analysis</div>
      `;
      return;
    }

    const analysis = this.performTextAnalysis(text);
    
    analysisDiv.innerHTML = `
      <h4>✨ Text Analysis</h4>
      <div class="analysis-grid">
        <div class="analysis-item">
          <span class="label">Length:</span>
          <span class="value">${analysis.length}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Words:</span>
          <span class="value">${analysis.wordCount}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Complexity:</span>
          <span class="value complexity-${analysis.complexity}">${analysis.complexity}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Energy:</span>
          <span class="value">${analysis.energy}</span>
        </div>
      </div>
    `;
  }

  performTextAnalysis(text) {
    const wordCount = text.split(/\s+/).length;
    const length = text.length;
    
    let complexity = 'Simple';
    if (length > 100) complexity = 'Profound';
    else if (length > 50) complexity = 'Complex';
    else if (length > 20) complexity = 'Moderate';
    
    const energy = Math.floor((text.length + wordCount) / 10) + 1;
    
    return { length, wordCount, complexity, energy };
  }

  async generateSigil() {
    const phraseInput = document.getElementById('phraseInput');
    const generateBtn = document.getElementById('generateBtn');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const resultsSection = document.getElementById('resultsSection');
    
    if (!phraseInput) return;
    
    const phrase = phraseInput.value.trim();
    
    if (phrase.length < 2) {
      this.showToast('Please enter at least 2 characters', 'error');
      return;
    }

    try {
      // Show loading
      if (loadingOverlay) loadingOverlay.style.display = 'flex';
      if (generateBtn) {
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Manifesting...';
      }

      const advanced = document.getElementById('advancedMode')?.checked || false;

      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          phrase,
          vibe: this.selectedVibe,
          advanced
        })
      });

      const data = await response.json();

      if (data.success) {
        this.displaySigil(data);
        if (resultsSection) resultsSection.style.display = 'block';
        this.showToast('Revolutionary sigil manifested!', 'success');
      } else {
        throw new Error(data.error || 'Generation failed');
      }

    } catch (error) {
      console.error('Generation error:', error);
      this.showToast('Failed to generate sigil: ' + error.message, 'error');
    } finally {
      // Hide loading
      if (loadingOverlay) loadingOverlay.style.display = 'none';
      if (generateBtn) {
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-magic"></i> <span>Generate Revolutionary Sigil</span>';
      }
    }
  }

  displaySigil(data) {
    const container = document.getElementById('sigilContainer');
    if (!container) return;

    const imageUrl = `data:image/png;base64,${data.image}`;
    
    container.innerHTML = `
      <div class="sigil-display">
        <img src="${imageUrl}" alt="Generated Sigil" class="sigil-image">
        <div class="sigil-info">
          <p class="sigil-phrase">"${data.phrase}"</p>
          <p class="sigil-vibe">Energy: ${data.vibe}</p>
        </div>
        <div class="sigilActions">
          <button class="btn btn-secondary" onclick="app.downloadSigil('${imageUrl}', '${data.phrase}')">
            <i class="fas fa-download"></i> Download
          </button>
          <button class="btn btn-secondary" onclick="app.shareSigil('${imageUrl}')">
            <i class="fas fa-share"></i> Share
          </button>
        </div>
      </div>
    `;

    this.currentSigil = data;
  }

  downloadSigil(imageUrl, phrase) {
    const link = document.createElement('a');
    link.href = imageUrl;
    link.download = `sigil-${phrase.replace(/[^a-zA-Z0-9]/g, '-').toLowerCase()}.png`;
    link.click();
  }

  shareSigil(imageUrl) {
    if (navigator.share) {
      navigator.share({
        title: 'My Revolutionary Sigil',
        text: 'Check out my manifested sigil from Sigilcraft!',
        url: window.location.href
      });
    } else {
      navigator.clipboard.writeText(window.location.href);
      this.showToast('Link copied to clipboard!', 'info');
    }
  }

  showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => document.body.removeChild(toast), 300);
    }, 3000);
  }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.app = new SigilcraftApp();
});
