/**
 * SIGILCRAFT: ULTRA-REVOLUTIONARY SIGIL GENERATOR
 * Enhanced Frontend Application with Revolutionary Features
 */

class SigilcraftApp {
  constructor() {
    this.currentSigil = null;
    this.isGenerating = false;
    this.cooldownTimer = null;
    this.init();
  }

  init() {
    this.setupEventListeners();
    this.loadVibes();
    this.updateUI();
    console.log('🎨 Sigilcraft Ultra initialized successfully!');
  }

  setupEventListeners() {
    // Generate button
    const generateBtn = document.getElementById('generateBtn');
    if (generateBtn) {
      generateBtn.addEventListener('click', () => this.generateSigil());
    }

    // Download button
    const downloadBtn = document.getElementById('downloadBtn');
    if (downloadBtn) {
      downloadBtn.addEventListener('click', () => this.downloadSigil());
    }

    // Share button
    const shareBtn = document.getElementById('shareBtn');
    if (shareBtn) {
      shareBtn.addEventListener('click', () => this.shareSigil());
    }

    // Form submission
    const sigilForm = document.getElementById('sigilForm');
    if (sigilForm) {
      sigilForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.generateSigil();
      });
    }

    // Phrase input
    const phraseInput = document.getElementById('phrase');
    if (phraseInput) {
      phraseInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.generateSigil();
        }
      });
    }
  }

  async loadVibes() {
    try {
      const response = await fetch('/api/vibes');
      const data = await response.json();

      if (data.success) {
        this.populateVibeSelector(data.vibes, data.descriptions);
      }
    } catch (error) {
      console.warn('Failed to load vibes from server, using defaults');
      this.populateVibeSelector(
        ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light', 'storm', 'void'],
        {
          'mystical': 'Ancient wisdom & sacred geometry',
          'cosmic': 'Universal stellar connection',
          'elemental': 'Natural organic forces',
          'crystal': 'Prismatic geometric precision',
          'shadow': 'Hidden mysterious power',
          'light': 'Pure divine radiance',
          'storm': 'Raw electric chaos',
          'void': 'Infinite recursive potential'
        }
      );
    }
  }

  populateVibeSelector(vibes, descriptions) {
    const vibeSelect = document.getElementById('vibe');
    if (!vibeSelect) return;

    vibeSelect.innerHTML = '';

    vibes.forEach(vibe => {
      const option = document.createElement('option');
      option.value = vibe;
      option.textContent = `${vibe.charAt(0).toUpperCase() + vibe.slice(1)} - ${descriptions[vibe] || 'Mystical energy'}`;
      vibeSelect.appendChild(option);
    });
  }

  async generateSigil() {
    if (this.isGenerating) {
      this.showToast('Generation in progress...', 'info');
      return;
    }

    const phrase = document.getElementById('phrase')?.value?.trim();
    if (!phrase) {
      this.showToast('Please enter a phrase for your sigil', 'error');
      return;
    }

    if (phrase.length < 2) {
      this.showToast('Phrase must be at least 2 characters long', 'error');
      return;
    }

    const vibe = document.getElementById('vibe')?.value || 'mystical';
    const advanced = document.getElementById('advanced')?.checked || false;

    this.isGenerating = true;
    this.updateUI();

    try {
      const response = await fetch('/api/sigil', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ phrase, vibe, advanced })
      });

      const data = await response.json();

      if (data.success) {
        this.currentSigil = data;
        this.displaySigil(data);
        this.showToast(`Revolutionary sigil manifested in ${data.metadata?.duration?.toFixed(2) || 0}s!`, 'success');
      } else {
        throw new Error(data.error || 'Generation failed');
      }
    } catch (error) {
      console.error('Generation error:', error);
      this.showToast(`Generation failed: ${error.message}`, 'error');
    } finally {
      this.isGenerating = false;
      this.updateUI();
    }
  }

  displaySigil(sigilData) {
    const resultDiv = document.getElementById('result');
    const sigilImage = document.getElementById('sigilImage');

    if (resultDiv && sigilImage) {
      sigilImage.src = `data:image/png;base64,${sigilData.image}`;
      sigilImage.alt = `Sigil for: ${sigilData.phrase}`;
      resultDiv.style.display = 'block';

      // Update metadata
      const metadataDiv = document.getElementById('sigilMetadata');
      if (metadataDiv) {
        metadataDiv.innerHTML = `
          <p><strong>Phrase:</strong> "${sigilData.phrase}"</p>
          <p><strong>Vibe:</strong> ${sigilData.vibe}</p>
          <p><strong>Advanced:</strong> ${sigilData.advanced ? 'Yes' : 'No'}</p>
          <p><strong>Generated:</strong> ${new Date(sigilData.metadata?.timestamp || Date.now()).toLocaleString()}</p>
        `;
      }
    }
  }

  updateUI() {
    const generateBtn = document.getElementById('generateBtn');
    if (generateBtn) {
      generateBtn.disabled = this.isGenerating;
      generateBtn.textContent = this.isGenerating ? 'Manifesting Sigil...' : 'Generate Sigil';
    }

    const downloadBtn = document.getElementById('downloadBtn');
    const shareBtn = document.getElementById('shareBtn');

    if (downloadBtn) downloadBtn.disabled = !this.currentSigil;
    if (shareBtn) shareBtn.disabled = !this.currentSigil;
  }

  downloadSigil() {
    if (!this.currentSigil) {
      this.showToast('No sigil to download', 'error');
      return;
    }

    try {
      const link = document.createElement('a');
      link.href = `data:image/png;base64,${this.currentSigil.image}`;
      link.download = `sigil-${this.currentSigil.phrase.replace(/[^a-zA-Z0-9]/g, '_')}-${Date.now()}.png`;

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

    // Add toast styles
    Object.assign(toast.style, {
      position: 'fixed',
      top: '20px',
      right: '20px',
      padding: '12px 20px',
      borderRadius: '5px',
      color: 'white',
      fontWeight: 'bold',
      zIndex: '10000',
      opacity: '1',
      transition: 'opacity 0.3s ease'
    });

    // Set background color based on type
    const colors = {
      success: '#28a745',
      error: '#dc3545',
      info: '#17a2b8',
      warning: '#ffc107'
    };
    toast.style.backgroundColor = colors[type] || colors.info;

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

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.app = new SigilcraftApp();
});

// Add global error handler
window.addEventListener('error', (event) => {
  console.error('Global error:', event.error);
  if (window.app) {
    window.app.showToast('An unexpected error occurred', 'error');
  }
});

// Make app globally accessible
window.SigilcraftApp = SigilcraftApp;