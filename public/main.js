// ===== SIGILCRAFT - QUANTUM SIGIL GENERATOR PRO =====

// Configuration
const FREE_ENERGIES = ["mystical", "elemental", "light"];
const ALL_ENERGIES = ["mystical", "cosmic", "elemental", "crystal", "shadow", "light"];
const COOLDOWN_TIME = 10000; // 10 seconds

// State Management
let state = {
  selectedEnergies: [FREE_ENERGIES[0]],
  lastGeneratedImage: null,
  isGenerating: false,
  cooldownActive: false,
  isPro: false,
  sigilGallery: JSON.parse(localStorage.getItem('sigil_gallery') || '[]'),
  currentSigilData: null
};

// DOM Elements Cache
const elements = {
  intentInput: document.getElementById('intentInput'),
  generateBtn: document.getElementById('generateBtn'),
  canvas: document.getElementById('sigilCanvas'),
  energyContainer: document.getElementById('energyContainer'),
  canvasContainer: document.getElementById('canvasContainer'),
  downloadBtn: document.getElementById('downloadBtn'),
  loading: document.getElementById('loading'),
  charCount: document.querySelector('.char-count'),
  galleryContainer: document.getElementById('galleryContainer'),
  shareModal: document.getElementById('shareModal')
};

// ===== CORE GENERATION SYSTEM =====
async function generateSigil() {
  if (state.isGenerating || state.cooldownActive) return;

  const phrase = elements.intentInput?.value?.trim();
  if (!phrase) {
    showToast('✨ Enter your sacred intention', 'warning');
    return;
  }

  if (phrase.length < 2 || phrase.length > 200) {
    showToast('Intention must be 2-200 characters', 'warning');
    return;
  }

  const vibe = state.selectedEnergies.join('+');

  try {
    state.isGenerating = true;
    updateUI();
    showSpiritualLoading();

    console.log(`🎨 Channeling cosmic energies...`);
    console.log(`📝 Manifesting: "${phrase}" with vibes: ${vibe}`);

    const result = await makeGenerationRequest(phrase, vibe);

    if (result?.success && result?.image) {
      state.lastGeneratedImage = result.image;
      state.currentSigilData = {
        id: Date.now(),
        phrase: phrase,
        vibe: vibe,
        image: result.image,
        timestamp: new Date().toISOString(),
        energy: state.selectedEnergies
      };

      await renderSigil(result.image);
      addToGallery(state.currentSigilData);
      showResult();
      showToast('✨ Sigil manifested successfully!', 'success');

      if (!state.isPro) startCooldown();
    } else {
      throw new Error(result?.error || 'Generation failed');
    }

  } catch (error) {
    console.error('Generation error:', error);
    showToast(error.message || 'Generation temporarily unavailable', 'error');
  } finally {
    state.isGenerating = false;
    updateUI();
    hideSpiritualLoading();
  }
}

async function makeGenerationRequest(phrase, vibe) {
  const response = await fetch('/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phrase, vibe }),
    signal: AbortSignal.timeout(45000)
  });

  if (!response.ok) {
    const errorText = await response.text().catch(() => `HTTP ${response.status}`);
    throw new Error(`Server error: ${errorText}`);
  }

  return response.json();
}

// ===== ENHANCED UI MANAGEMENT =====
function updateUI() {
  updateGenerateButton();
  renderEnergies();
  updateProInterface();
  updateCharCounter();
  renderGallery();
}

function updateGenerateButton() {
  if (!elements.generateBtn) return;

  if (state.isGenerating) {
    elements.generateBtn.disabled = true;
    elements.generateBtn.innerHTML = '<div class="btn-mandala"></div><span>Channeling Energies...</span>';
    elements.generateBtn.classList.add('generating');
  } else if (state.cooldownActive) {
    elements.generateBtn.disabled = true;
    elements.generateBtn.innerHTML = '<div class="btn-mandala"></div><span>Recharging...</span>';
    elements.generateBtn.classList.remove('generating');
  } else {
    elements.generateBtn.disabled = false;
    elements.generateBtn.innerHTML = '<div class="btn-mandala"></div><span>Generate Sigil</span>';
    elements.generateBtn.classList.remove('generating');
  }
}

function updateCharCounter() {
  if (elements.charCount && elements.intentInput) {
    const count = elements.intentInput.value.length;
    elements.charCount.textContent = `${count}/200`;
    elements.charCount.style.color = count > 180 ? '#ff6b9d' : count > 150 ? '#ffd700' : '#cbd5e1';
  }
}

function startCooldown() {
  if (state.isPro) return;

  state.cooldownActive = true;
  let remaining = COOLDOWN_TIME;

  const interval = setInterval(() => {
    remaining -= 1000;

    if (elements.generateBtn) {
      elements.generateBtn.innerHTML = `<div class="btn-mandala"></div><span>Recharging... ${Math.ceil(remaining/1000)}s</span>`;
    }

    if (remaining <= 0) {
      clearInterval(interval);
      state.cooldownActive = false;
      updateUI();
    }
  }, 1000);
}

// ===== SPIRITUAL LOADING SYSTEM =====
function showSpiritualLoading() {
  if (!elements.loading) return;

  elements.loading.innerHTML = `
    <div class="spiritual-loading">
      <div class="cosmic-mandala">
        <div class="outer-ring"></div>
        <div class="middle-ring"></div>
        <div class="inner-ring"></div>
        <div class="sacred-eye">👁</div>
      </div>
      <div class="energy-waves">
        <div class="wave wave-1"></div>
        <div class="wave wave-2"></div>
        <div class="wave wave-3"></div>
      </div>
      <p class="spiritual-text">Channeling cosmic energies...</p>
      <div class="blessing-particles">
        ${'✨'.repeat(12).split('').map((star, i) => `<span class="particle" style="--delay: ${i * 0.3}s">${star}</span>`).join('')}
      </div>
    </div>
  `;

  elements.loading.style.display = 'flex';
}

function hideSpiritualLoading() {
  if (elements.loading) {
    elements.loading.style.display = 'none';
  }
}

// ===== ENHANCED ENERGY SELECTION =====
function renderEnergies() {
  if (!elements.energyContainer) return;

  const availableEnergies = state.isPro ? ALL_ENERGIES : FREE_ENERGIES;

  elements.energyContainer.innerHTML = availableEnergies.map(energy => `
    <div class="energy-option ${state.selectedEnergies.includes(energy) ? 'selected' : ''}" 
         data-energy="${energy}" 
         data-vibe="${energy}"
         onclick="toggleEnergy('${energy}')">
      <div class="energy-icon">${getEnergyIcon(energy)}</div>
      <span class="energy-name">${energy.charAt(0).toUpperCase() + energy.slice(1)}</span>
      ${!FREE_ENERGIES.includes(energy) && !state.isPro ? '<span class="pro-badge">PRO</span>' : ''}
    </div>
  `).join('');
}

function getEnergyIcon(energy) {
  const icons = {
    mystical: '🔮',
    cosmic: '🌌',
    elemental: '🌊',
    crystal: '💎',
    shadow: '🌑',
    light: '☀️'
  };
  return icons[energy] || '✨';
}

function toggleEnergy(energy) {
  if (!FREE_ENERGIES.includes(energy) && !state.isPro) {
    showToast('✨ Pro feature - unlock to access all energies', 'warning');
    return;
  }

  if (state.selectedEnergies.includes(energy)) {
    if (state.selectedEnergies.length > 1) {
      state.selectedEnergies = state.selectedEnergies.filter(e => e !== energy);
    }
  } else {
    if (!state.isPro && state.selectedEnergies.length >= 1) {
      state.selectedEnergies = [energy];
    } else if (state.selectedEnergies.length < 4) {
      state.selectedEnergies.push(energy);
    }
  }

  renderEnergies();
}

// ===== SIGIL GALLERY SYSTEM =====
function addToGallery(sigilData) {
  state.sigilGallery.unshift(sigilData);
  if (state.sigilGallery.length > 50) {
    state.sigilGallery = state.sigilGallery.slice(0, 50);
  }
  localStorage.setItem('sigil_gallery', JSON.stringify(state.sigilGallery));
  renderGallery();
}

function renderGallery() {
  const galleryContainer = document.getElementById('galleryContainer');
  if (!galleryContainer || state.sigilGallery.length === 0) return;

  galleryContainer.innerHTML = `
    <div class="gallery-header">
      <h3><i class="fas fa-images"></i> Your Sacred Gallery</h3>
      <button onclick="clearGallery()" class="clear-gallery-btn">
        <i class="fas fa-trash-alt"></i> Clear All
      </button>
    </div>
    <div class="gallery-grid">
      ${state.sigilGallery.map(sigil => `
        <div class="gallery-item" onclick="loadSigil('${sigil.id}')">
          <img src="${sigil.image}" alt="Sigil: ${sigil.phrase}">
          <div class="gallery-overlay">
            <div class="gallery-info">
              <p class="gallery-phrase">"${sigil.phrase.substring(0, 30)}${sigil.phrase.length > 30 ? '...' : ''}"</p>
              <p class="gallery-energy">${sigil.energy.join(' + ')}</p>
              <p class="gallery-date">${new Date(sigil.timestamp).toLocaleDateString()}</p>
            </div>
            <div class="gallery-actions">
              <button onclick="event.stopPropagation(); downloadSigilFromGallery('${sigil.id}')" class="gallery-btn">
                <i class="fas fa-download"></i>
              </button>
              <button onclick="event.stopPropagation(); shareSigil('${sigil.id}')" class="gallery-btn">
                <i class="fas fa-share-alt"></i>
              </button>
            </div>
          </div>
        </div>
      `).join('')}
    </div>
  `;

  galleryContainer.style.display = 'block';
}

function loadSigil(sigilId) {
  const sigil = state.sigilGallery.find(s => s.id == sigilId);
  if (sigil) {
    state.lastGeneratedImage = sigil.image;
    state.currentSigilData = sigil;
    renderSigil(sigil.image);
    showResult();
    elements.intentInput.value = sigil.phrase;
    state.selectedEnergies = sigil.energy;
    updateUI();
  }
}

function clearGallery() {
  if (confirm('Are you sure you want to clear your entire sigil gallery?')) {
    state.sigilGallery = [];
    localStorage.removeItem('sigil_gallery');
    renderGallery();
    showToast('Gallery cleared', 'info');
  }
}

// ===== ENHANCED DOWNLOAD SYSTEM =====
function downloadSigil() {
  if (!state.lastGeneratedImage) {
    showToast('Generate a sigil first', 'warning');
    return;
  }

  const phrase = state.currentSigilData?.phrase || 'sigil';
  const timestamp = new Date().toISOString().split('T')[0];
  const filename = `sigilcraft-${phrase.replace(/\s+/g, '-').toLowerCase()}-${timestamp}.png`;

  const link = document.createElement('a');
  link.download = filename;
  link.href = state.lastGeneratedImage;
  link.click();

  showToast('✨ Sigil downloaded to your device', 'success');
}

function downloadSigilFromGallery(sigilId) {
  const sigil = state.sigilGallery.find(s => s.id == sigilId);
  if (sigil) {
    const phrase = sigil.phrase.replace(/\s+/g, '-').toLowerCase();
    const timestamp = new Date(sigil.timestamp).toISOString().split('T')[0];
    const filename = `sigilcraft-${phrase}-${timestamp}.png`;

    const link = document.createElement('a');
    link.download = filename;
    link.href = sigil.image;
    link.click();

    showToast('✨ Sigil downloaded', 'success');
  }
}

// ===== SOCIAL SHARING SYSTEM =====
function shareSigil(sigilId) {
  const sigil = state.sigilGallery.find(s => s.id == sigilId);
  if (!sigil) return;

  state.currentSigilData = sigil;
  showShareModal();
}

function showShareModal() {
  if (!state.currentSigilData) return;

  const modal = document.createElement('div');
  modal.className = 'share-modal-overlay';
  modal.innerHTML = `
    <div class="share-modal">
      <div class="share-header">
        <h3><i class="fas fa-share-alt"></i> Share Your Sacred Sigil</h3>
        <button onclick="this.closest('.share-modal-overlay').remove()" class="close-btn">×</button>
      </div>
      <div class="share-content">
        <div class="share-preview">
          <img src="${state.currentSigilData.image}" alt="Sigil">
          <p>"${state.currentSigilData.phrase}"</p>
        </div>
        <div class="share-options">
          <button onclick="shareToTwitter()" class="share-btn twitter">
            <i class="fab fa-twitter"></i> Share to Twitter
          </button>
          <button onclick="shareToFacebook()" class="share-btn facebook">
            <i class="fab fa-facebook"></i> Share to Facebook
          </button>
          <button onclick="shareToInstagram()" class="share-btn instagram">
            <i class="fab fa-instagram"></i> Instagram Story
          </button>
          <button onclick="copyShareLink()" class="share-btn copy">
            <i class="fas fa-link"></i> Copy Link
          </button>
          <button onclick="shareViaNative()" class="share-btn native">
            <i class="fas fa-share"></i> More Options
          </button>
        </div>
      </div>
    </div>
  `;

  document.body.appendChild(modal);
}

function shareToTwitter() {
  const text = `I just created this mystical sigil for "${state.currentSigilData.phrase}" using Sigilcraft! ✨🔮`;
  const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(window.location.href)}`;
  window.open(url, '_blank');
}

function shareToFacebook() {
  const url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.href)}`;
  window.open(url, '_blank');
}

function shareToInstagram() {
  showToast('💫 Download the sigil and share to your Instagram story!', 'info');
  downloadSigil();
}

function copyShareLink() {
  navigator.clipboard.writeText(window.location.href).then(() => {
    showToast('✨ Link copied to clipboard!', 'success');
  });
}

function shareViaNative() {
  if (navigator.share) {
    navigator.share({
      title: 'My Sacred Sigil',
      text: `Check out this mystical sigil I created for "${state.currentSigilData.phrase}"`,
      url: window.location.href
    });
  } else {
    copyShareLink();
  }
}

// ===== CANVAS & RENDERING =====
async function renderSigil(imageData) {
  return new Promise((resolve) => {
    if (!elements.canvas) {
      resolve();
      return;
    }

    const ctx = elements.canvas.getContext('2d');
    const img = new Image();
    img.onload = () => {
      ctx.clearRect(0, 0, elements.canvas.width, elements.canvas.height);

      const scale = Math.min(
        elements.canvas.width / img.width, 
        elements.canvas.height / img.height
      );
      const x = (elements.canvas.width - img.width * scale) / 2;
      const y = (elements.canvas.height - img.height * scale) / 2;

      ctx.drawImage(img, x, y, img.width * scale, img.height * scale);
      resolve();
    };
    img.src = imageData;
  });
}

function showResult() {
  if (elements.canvasContainer) {
    elements.canvasContainer.classList.remove('hidden');
  }
  if (elements.downloadBtn) {
    elements.downloadBtn.style.display = 'block';
  }
}

// ===== PRO FEATURES =====
async function checkProStatus() {
  try {
    const localPro = localStorage.getItem('sigil_pro') === '1';
    const proKey = localStorage.getItem('sigil_pro_key');

    let serverPro = false;
    if (proKey) {
      const response = await fetch('/api/pro-status', {
        headers: { 'x-pro-key': proKey }
      });

      if (response.ok) {
        const data = await response.json();
        serverPro = data.isPro || false;
      }
    }

    state.isPro = localPro || serverPro;
    updateUI();

  } catch (error) {
    console.error('Error checking pro status:', error);
    state.isPro = localStorage.getItem('sigil_pro') === '1';
    updateUI();
  }
}

function updateProInterface() {
  const proBadge = document.getElementById('proBadge');
  const proControls = document.getElementById('proControls');
  const unlockSection = document.getElementById('unlockSection');

  if (proBadge) proBadge.style.display = state.isPro ? 'flex' : 'none';
  if (proControls) proControls.style.display = state.isPro ? 'block' : 'none';
  if (unlockSection) unlockSection.style.display = state.isPro ? 'none' : 'block';
}

async function validateProKey(key) {
  try {
    const response = await fetch('/api/validate-key', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key })
    });

    const data = await response.json();

    if (data.success && data.valid) {
      localStorage.setItem('sigil_pro', '1');
      localStorage.setItem('sigil_pro_key', key);
      state.isPro = true;
      updateUI();
      showToast('✨ Pro features unlocked!', 'success');
      return true;
    } else {
      showToast('Invalid pro key', 'error');
      return false;
    }
  } catch (error) {
    console.error('Pro validation error:', error);
    showToast('Validation failed', 'error');
    return false;
  }
}

// ===== UTILITIES =====
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <div class="toast-content">
      <i class="toast-icon ${getToastIcon(type)}"></i>
      <span>${message}</span>
    </div>
  `;

  document.body.appendChild(toast);
  setTimeout(() => toast.classList.add('show'), 100);

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => document.body.removeChild(toast), 300);
  }, 4000);
}

function getToastIcon(type) {
  const icons = {
    success: 'fas fa-check-circle',
    error: 'fas fa-exclamation-circle',
    warning: 'fas fa-exclamation-triangle',
    info: 'fas fa-info-circle'
  };
  return icons[type] || 'fas fa-info-circle';
}

// ===== EVENT SETUP =====
function setupEvents() {
  elements.generateBtn?.addEventListener('click', generateSigil);

  elements.intentInput?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      generateSigil();
    }
  });

  elements.intentInput?.addEventListener('input', updateCharCounter);

  elements.downloadBtn?.addEventListener('click', downloadSigil);

  const proKeyBtn = document.getElementById('proKeyBtn');
  const proKeyModal = document.getElementById('proKeyModal');
  const proKeySubmit = document.getElementById('proKeySubmit');
  const proKeyInput = document.getElementById('proKeyInput');

  proKeyBtn?.addEventListener('click', () => proKeyModal?.showModal());

  proKeySubmit?.addEventListener('click', async () => {
    const key = proKeyInput?.value?.trim();
    if (key && await validateProKey(key)) {
      proKeyModal?.close();
      if (proKeyInput) proKeyInput.value = '';
    }
  });

  // Close modal on backdrop click
  proKeyModal?.addEventListener('click', (e) => {
    if (e.target === proKeyModal) {
      proKeyModal.close();
    }
  });
}

// ===== INITIALIZATION =====
async function init() {
  console.log('🚀 Initializing Sigil Generator Pro...');

  setupEvents();
  await checkProStatus();
  updateUI();

  console.log('✅ App initialization complete!');
}

// Start the application
document.addEventListener('DOMContentLoaded', init);

// Global access for inline event handlers
window.generateSigil = generateSigil;
window.toggleEnergy = toggleEnergy;
window.downloadSigil = downloadSigil;
window.loadSigil = loadSigil;
window.clearGallery = clearGallery;
window.downloadSigilFromGallery = downloadSigilFromGallery;
window.shareSigil = shareSigil;
window.shareToTwitter = shareToTwitter;
window.shareToFacebook = shareToFacebook;
window.shareToInstagram = shareToInstagram;
window.copyShareLink = copyShareLink;
window.shareViaNative = shareViaNative;