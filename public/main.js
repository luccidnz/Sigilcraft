` tags.

<replit_final_file>
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
    const phraseInput = document.getElementById('phraseInput');
    const counterContainer = document.querySelector('.char-counter-container');

    if (!phraseInput) return;

    // Create counter if it doesn't exist
    if (!counterContainer) {
      const container = document.createElement('div');
      container.className = 'char-counter-container';
      container.innerHTML = '<span id="charCounter" class="char-counter">0/500</span>';
      phraseInput.parentNode.appendChild(container);
    }

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

    // Perform text analysis
    const words = text.split(/\s+/).filter(word => word.length > 0);
    const characters = text.length;
    const vowels = (text.match(/[aeiouAEIOU]/g) || []).length;
    const consonants = (text.match(/[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]/g) || []).length;

    let complexity = 'Simple';
    if (characters > 50) complexity = 'Moderate';
    if (characters > 100) complexity = 'Complex';
    if (characters > 200) complexity = 'Profound';

    analysisDiv.innerHTML = `
      <h4>✨ Text Analysis</h4>
      <div class="analysis-grid">
        <div class="analysis-item">
          <span class="label">Words:</span>
          <span class="value">${words.length}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Characters:</span>
          <span class="value">${characters}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Vowels:</span>
          <span class="value">${vowels}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Consonants:</span>
          <span class="value">${consonants}</span>
        </div>
        <div class="analysis-item">
          <span class="label">Complexity:</span>
          <span class="value complexity-${complexity}">${complexity}</span>
        </div>
      </div>
    `;
  }

  async generateSigil() {
    const phraseInput = document.getElementById('phraseInput');
    const generateBtn = document.getElementById('generateBtn');

    if (!phraseInput || !phraseInput.value.trim()) {
      this.showToast('Please enter a phrase to generate a sigil', 'warning');
      return;
    }

    const phrase = phraseInput.value.trim();
    const advanced = document.getElementById('advancedMode')?.checked || false;

    try {
      generateBtn.disabled = true;
      generateBtn.textContent = 'Manifesting...';

      this.showLoadingOverlay();

      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          phrase: phrase,
          vibe: this.selectedVibe,
          advanced: advanced
        })
      });

      const data = await response.json();

      if (data.success) {
        this.displaySigil(data);
        this.showToast('Revolutionary sigil manifested!', 'success');
      } else {
        throw new Error(data.error || 'Generation failed');
      }

    } catch (error) {
      console.error('Generation error:', error);
      this.showToast(error.message || 'Failed to generate sigil', 'error');
    } finally {
      this.hideLoadingOverlay();
      generateBtn.disabled = false;
      generateBtn.textContent = 'Generate Sigil';
    }
  }

  displaySigil(data) {
    const displayDiv = document.getElementById('sigilDisplay');
    if (!displayDiv) return;

    this.currentSigil = data;

    displayDiv.innerHTML = `
      <div class="sigil-image-container">
        <img src="data:image/png;base64,${data.image}" alt="Generated Sigil" class="sigil-image">
      </div>
      <div class="sigil-info">
        <h3>"${data.phrase}"</h3>
        <p class="sigil-vibe">${data.vibe.charAt(0).toUpperCase() + data.vibe.slice(1)} Energy</p>
        <div class="sigilActions">
          <button class="btn btn-secondary" onclick="app.downloadSigil()">📥 Download</button>
          <button class="btn btn-secondary" onclick="app.shareSigil()">📤 Share</button>
        </div>
      </div>
    `;

    displayDiv.scrollIntoView({ behavior: 'smooth' });
  }

  showLoadingOverlay() {
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
      <div class="loading-content">
        <div class="spinner"></div>
        <p>Manifesting your revolutionary sigil...</p>
      </div>
    `;
    document.body.appendChild(overlay);
  }

  hideLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
      document.body.removeChild(overlay);
    }
  }

  downloadSigil() {
    if (!this.currentSigil) {
      this.showToast('No sigil to download', 'warning');
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

// Make app globally accessible for HTML onclick handlers
window.app = app;