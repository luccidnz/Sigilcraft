// ===== SIGILCRAFT - QUANTUM SIGIL GENERATOR PRO =====

// Configuration
const FREE_ENERGIES = ["mystical", "elemental", "light"];
const ALL_ENERGIES = ["mystical", "cosmic", "elemental", "crystal", "shadow", "light"];
const COOLDOWN_TIME = 10000; // 10 seconds

// Global state
let state = {
  selectedEnergies: [FREE_ENERGIES[0]],
  lastGeneratedImage: null,
  isGenerating: false,
  cooldownActive: false,
  isPro: false,
  sigilGallery: JSON.parse(localStorage.getItem('sigil_gallery') || '[]'),
  currentSigilData: null
};

// DOM elements cache
let elements = {};

// Cache DOM elements
function cacheElements() {
  elements = {
    intentInput: document.getElementById('intentInput'),
    generateBtn: document.getElementById('generateBtn'),
    canvas: document.getElementById('sigilCanvas'),
    canvasContainer: document.getElementById('canvasContainer'),
    downloadBtn: document.getElementById('downloadBtn'),
    loading: document.getElementById('loading'),
    energyContainer: document.getElementById('energyContainer'),
    charCount: document.querySelector('.char-count'),
    galleryContainer: document.getElementById('galleryContainer'),
    shareModal: document.getElementById('shareModal'),
    proBadge: document.getElementById('proBadge'),
    proControls: document.getElementById('proControls'),
    unlockSection: document.getElementById('unlockSection'),
    proKeyInput: document.getElementById('proKeyInput'),
    proKeySubmit: document.getElementById('proKeySubmit'),
    proKeyModal: document.getElementById('proKeyModal')
  };
}

// Setup event listeners
function setupEvents() {
  if (elements.generateBtn) {
    elements.generateBtn.addEventListener('click', generateSigil);
  }

  if (elements.intentInput) {
    elements.intentInput.addEventListener('input', updateCharCounter);
    elements.intentInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !state.isGenerating && !state.cooldownActive) {
        generateSigil();
      }
    });
  }

  if (elements.downloadBtn) {
    elements.downloadBtn.addEventListener('click', downloadSigil);
  }

  if (elements.proKeySubmit) {
    elements.proKeySubmit.addEventListener('click', submitProKey);
  }

  // Close modals on outside click
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
      e.target.style.display = 'none';
    }
  });
}

// ===== PRO FEATURES =====
async function checkProStatus() {
  try {
    const localPro = localStorage.getItem('sigil_pro') === '1';
    const proKey = localStorage.getItem('sigil_pro_key');

    let serverPro = false;
    if (proKey) {
      try {
        const response = await fetch('/api/pro-status', {
          headers: { 'x-pro-key': proKey },
          signal: AbortSignal.timeout(5000)
        });

        if (response.ok) {
          const contentType = response.headers.get('content-type');
          if (contentType && contentType.includes('application/json')) {
            const data = await response.json();
            serverPro = data.isPro || false;
          } else {
            console.log('Pro status endpoint returned non-JSON response');
          }
        } else {
          console.log(`Pro status check failed: ${response.status} ${response.statusText}`);
        }
      } catch (fetchError) {
        console.log('Pro status fetch failed:', fetchError.message);
      }
    }

    state.isPro = localPro || serverPro;
    updateUI();

  } catch (error) {
    console.log('Pro status check failed, falling back to local storage');
    state.isPro = localStorage.getItem('sigil_pro') === '1';
    updateUI();
  }
}

async function submitProKey() {
  const key = elements.proKeyInput?.value?.trim();
  if (!key) return;

  try {
    const response = await fetch('/api/validate-key', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key })
    });

    const data = await response.json();

    if (data.valid) {
      localStorage.setItem('sigil_pro', '1');
      localStorage.setItem('sigil_pro_key', key);
      state.isPro = true;
      showToast('✨ Pro features unlocked!', 'success');
      updateUI();
      if (elements.proKeyModal) {
        elements.proKeyModal.style.display = 'none';
      }
    } else {
      showToast('❌ Invalid pro key', 'error');
    }
  } catch (error) {
    console.error('Pro key validation error:', error);
    showToast('❌ Validation failed', 'error');
  }
}

// ===== ENERGY SELECTION =====
function renderEnergySelection() {
  if (!elements.energyContainer) return;

  const availableEnergies = state.isPro ? ALL_ENERGIES : FREE_ENERGIES;

  elements.energyContainer.innerHTML = `
    <h3>Choose Your Vibe</h3>
    <div class="energy-grid">
      ${availableEnergies.map(energy => `
        <div class="energy-option ${state.selectedEnergies.includes(energy) ? 'selected' : ''}" 
             onclick="toggleEnergy('${energy}')">
          <i class="fas ${getEnergyIcon(energy)}"></i>
          <span>${energy.charAt(0).toUpperCase() + energy.slice(1)}</span>
          ${!FREE_ENERGIES.includes(energy) ? '<span class="pro-badge">PRO</span>' : ''}
        </div>
      `).join('')}
    </div>
  `;
}

function getEnergyIcon(energy) {
  const icons = {
    mystical: 'fa-moon',
    cosmic: 'fa-star',
    elemental: 'fa-fire',
    crystal: 'fa-gem',
    shadow: 'fa-eye',
    light: 'fa-sun'
  };
  return icons[energy] || 'fa-circle';
}

function toggleEnergy(energy) {
  if (!FREE_ENERGIES.includes(energy) && !state.isPro) {
    showToast('🔒 Pro feature - unlock to access all energies!', 'info');
    return;
  }

  if (state.selectedEnergies.includes(energy)) {
    state.selectedEnergies = state.selectedEnergies.filter(e => e !== energy);
  } else {
    state.selectedEnergies.push(energy);
  }

  if (state.selectedEnergies.length === 0) {
    state.selectedEnergies = [FREE_ENERGIES[0]];
  }

  renderEnergySelection();
}

// ===== SIGIL GENERATION =====
async function generateSigil() {
  if (state.isGenerating || state.cooldownActive) return;

  const phrase = elements.intentInput?.value?.trim();
  if (!phrase) {
    showToast('✨ Enter your intention first!', 'info');
    return;
  }

  if (phrase.length > 200) {
    showToast('❌ Phrase too long (max 200 characters)', 'error');
    return;
  }

  console.log('🎨 Channeling cosmic energies...');
  console.log(`📝 Manifesting: "${phrase}" with vibes: ${state.selectedEnergies.join('+')}`);

  state.isGenerating = true;
  updateGenerateButton();
  showLoading();

  try {
    const vibe = state.selectedEnergies.join('+');

    console.log(`🌟 Sending request: phrase="${phrase}", vibe="${vibe}"`);

    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phrase, vibe }),
      signal: AbortSignal.timeout(30000)
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Generation failed: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    console.log('✅ Generation response received');

    if (data.success && data.image) {
      state.lastGeneratedImage = data.image;
      state.currentSigilData = { phrase, vibe, image: data.image, timestamp: new Date().toISOString() };

      await renderSigil(data.image);
      showResult();
      saveToGallery(state.currentSigilData);
      renderGallery();

      hideLoading();
      showToast('✨ Sigil manifested successfully!', 'success');

      if (!state.isPro) {
        startCooldown();
      }
    } else {
      throw new Error(data.error || data.details || 'Generation failed - unknown error');
    }
  } catch (error) {
    const duration = Date.now() - startTime;
    console.error('Generation error:', error);
    hideLoading();

    let errorMessage = 'Generation failed';
    if (error.name === 'AbortError') {
      errorMessage = 'Generation timed out - please try again';
    } else if (error.message && error.message.trim()) {
      errorMessage = error.message;
    } else if (typeof error === 'string' && error.trim()) {
      errorMessage = error;
    } else {
      errorMessage = 'Unknown generation error occurred';
    }

    showToast(`❌ ${errorMessage}`, 'error');
  } finally {
    state.isGenerating = false;
    updateGenerateButton();
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

    img.onerror = () => {
      console.error('Failed to load sigil image data.');
      resolve();
    };

    img.src = imageData;
  });
}

// ===== GALLERY SYSTEM =====
function saveToGallery(sigilData) {
  const galleryItem = {
    id: Date.now(),
    phrase: sigilData.phrase,
    vibe: sigilData.vibe,
    image: sigilData.image,
    timestamp: sigilData.timestamp
  };

  state.sigilGallery.unshift(galleryItem);

  // Limit gallery size
  if (state.sigilGallery.length > 50) {
    state.sigilGallery = state.sigilGallery.slice(0, 50);
  }

  localStorage.setItem('sigil_gallery', JSON.stringify(state.sigilGallery));
}

function renderGallery() {
  if (!elements.galleryContainer) return;

  if (state.sigilGallery.length === 0) {
    elements.galleryContainer.innerHTML = '<p class="no-gallery">No sigils created yet. Generate your first sigil!</p>';
    return;
  }

  elements.galleryContainer.innerHTML = `
    <h3>Your Sacred Gallery</h3>
    <div class="gallery-grid">
      ${state.sigilGallery.map(sigil => `
        <div class="gallery-item">
          <img src="${sigil.image}" alt="Sigil for ${sigil.phrase}" onclick="viewSigil(${sigil.id})">
          <div class="gallery-info">
            <p class="gallery-phrase">"${sigil.phrase}"</p>
            <p class="gallery-vibe">${sigil.vibe}</p>
            <div class="gallery-actions">
              <button onclick="downloadSigilFromGallery(${sigil.id})" class="gallery-btn">
                <i class="fas fa-download"></i>
              </button>
              <button onclick="shareSigil(${sigil.id})" class="gallery-btn">
                <i class="fas fa-share-alt"></i>
              </button>
              <button onclick="deleteSigil(${sigil.id})" class="gallery-btn delete">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

function viewSigil(sigilId) {
  const sigil = state.sigilGallery.find(s => s.id == sigilId);
  if (!sigil) return;

  state.currentSigilData = sigil;
  renderSigil(sigil.image);
  showResult();
}

function deleteSigil(sigilId) {
  if (confirm('Delete this sigil from your gallery?')) {
    state.sigilGallery = state.sigilGallery.filter(s => s.id != sigilId);
    localStorage.setItem('sigil_gallery', JSON.stringify(state.sigilGallery));
    renderGallery();
    showToast('🗑️ Sigil removed from gallery', 'info');
  }
}

// ===== DOWNLOAD SYSTEM =====
function downloadSigil() {
  if (!state.currentSigilData) {
    showToast('❌ No sigil to download', 'error');
    return;
  }

  const phrase = state.currentSigilData.phrase.replace(/\s+/g, '-').toLowerCase();
  const timestamp = new Date().toISOString().split('T')[0];
  const filename = `sigilcraft-${phrase}-${timestamp}.png`;

  const link = document.createElement('a');
  link.download = filename;
  link.href = state.currentSigilData.image;
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
  if (elements.shareModal) {
    elements.shareModal.style.display = 'flex';
  }
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

// ===== UI UPDATES =====
function updateGenerateButton() {
  if (!elements.generateBtn) return;

  if (state.isGenerating) {
    elements.generateBtn.textContent = 'Channeling Energies...';
    elements.generateBtn.disabled = true;
  } else if (state.cooldownActive) {
    elements.generateBtn.disabled = true;
  } else {
    elements.generateBtn.textContent = '✨ Generate Sigil';
    elements.generateBtn.disabled = false;
  }
}

function updateCharCounter() {
  if (!elements.charCount || !elements.intentInput) return;

  const count = elements.intentInput.value.length;
  elements.charCount.textContent = `${count}/200`;

  if (count > 200) {
    elements.charCount.style.color = '#ff4444';
  } else if (count > 150) {
    elements.charCount.style.color = '#ffaa00';
  } else {
    elements.charCount.style.color = '#888';
  }
}

function updateProInterface() {
  if (elements.proBadge) {
    elements.proBadge.style.display = state.isPro ? 'block' : 'none';
  }

  if (elements.unlockSection) {
    elements.unlockSection.style.display = state.isPro ? 'none' : 'block';
  }
}

function startCooldown() {
  state.cooldownActive = true;
  let timeLeft = COOLDOWN_TIME / 1000;

  const countdown = setInterval(() => {
    if (elements.generateBtn) {
      elements.generateBtn.textContent = `Wait ${timeLeft}s`;
    }

    timeLeft--;

    if (timeLeft <= 0) {
      clearInterval(countdown);
      state.cooldownActive = false;
      updateGenerateButton();
    }
  }, 1000);
}

function showResult() {
  if (elements.canvasContainer) {
    elements.canvasContainer.classList.remove('hidden');
  }
  if (elements.downloadBtn) {
    elements.downloadBtn.style.display = 'block';
  }
}

function showLoading() {
  if (elements.loading) {
    elements.loading.style.display = 'flex';
  }
}

function hideLoading() {
  if (elements.loading) {
    elements.loading.style.display = 'none';
  }
}

// ===== TOAST NOTIFICATIONS =====
function showToast(message, type = 'info') {
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

// ===== MAIN UPDATE FUNCTION =====
function updateUI() {
  updateGenerateButton();
  renderEnergySelection();
  updateProInterface();
  updateCharCounter();
  renderGallery();
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', async () => {
  console.log('🚀 Initializing Sigil Generator Pro...');

  try {
    cacheElements();
    setupEvents();
    await checkProStatus();
    updateUI();

    console.log('✅ App initialization complete!');
  } catch (error) {
    console.error('❌ Initialization failed:', error);
    showToast('❌ App initialization failed', 'error');
  }
});