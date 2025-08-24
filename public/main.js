// Revolutionary Text-Responsive Sigil Generator - Frontend
// Enhanced with quantum-level text analysis and true uniqueness

// ===== CONSTANTS =====
const FREE_ENERGIES = ['mystical', 'elemental', 'light'];
const PRO_ENERGIES = ['cosmic', 'crystal', 'shadow'];
const ALL_ENERGIES = [...FREE_ENERGIES, ...PRO_ENERGIES];

// Energy descriptions for better UX
const ENERGY_DESCRIPTIONS = {
  'mystical': 'Ancient wisdom and spiritual connection',
  'cosmic': 'Universal forces and stellar energies',
  'elemental': 'Earth, fire, water, and air harmonies',
  'crystal': 'Prismatic light and geometric perfection',
  'shadow': 'Hidden depths and transformative power',
  'light': 'Divine radiance and illuminating truth'
};

// ===== STATE MANAGEMENT =====
const appState = {
  isPro: false,
  isGenerating: false,
  cooldownActive: false,
  cooldownTime: 30,
  selectedEnergies: [FREE_ENERGIES[0]],
  currentSigilData: null,
  sigilGallery: JSON.parse(localStorage.getItem('sigil_gallery') || '[]'),
  lastGeneratedImage: null,
  generationCounter: 0
};

// ===== DOM ELEMENTS =====
const domElements = {
  intentInput: null,
  generateBtn: null,
  downloadBtn: null,
  sigilCanvas: null,
  textAnalysis: null,
  energyContainer: null,
  galleryContainer: null,
  proKeyInput: null,
  proKeySubmit: null,
  shareModal: null,
  loadingIndicator: null,
  resultSection: null,
  charCounter: null,
  unlockSection: null,
  cooldownTimer: null
};

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', initializeApp);

function initializeApp() {
  console.log('🚀 Initializing Revolutionary Sigil Generator...');

  // Check for saved pro status
  if (localStorage.getItem('sigilcraft_pro') === 'true') {
    appState.isPro = true;
  }

  // Load saved gallery
  const savedGallery = localStorage.getItem('sigil_gallery');
  if (savedGallery) {
    try {
      appState.sigilGallery = JSON.parse(savedGallery);
    } catch (e) {
      console.warn('Failed to load gallery:', e);
      appState.sigilGallery = [];
    }
  }

  initializeDOM();
  checkProStatus();
  renderEnergySelection();
  renderGallery();
  setupEvents();
  updateUI();

  console.log('✅ Revolutionary app initialization complete!');
}

function initializeDOM() {
  domElements.intentInput = document.getElementById('intentInput');
  domElements.generateBtn = document.getElementById('generateBtn');
  domElements.downloadBtn = document.getElementById('downloadBtn');
  domElements.sigilCanvas = document.getElementById('sigilCanvas');
  domElements.textAnalysis = document.getElementById('textAnalysis');
  domElements.energyContainer = document.getElementById('energyContainer');
  domElements.galleryContainer = document.getElementById('galleryContainer');
  domElements.proKeyInput = document.getElementById('proKeyInput');
  domElements.proKeySubmit = document.getElementById('proKeySubmit');
  domElements.shareModal = document.getElementById('shareModal');
  domElements.loadingIndicator = document.getElementById('loading');
  domElements.resultSection = document.getElementById('resultSection');
  domElements.charCounter = document.getElementById('charCounter');
  domElements.unlockSection = document.getElementById('unlockSection');
  domElements.cooldownTimer = document.getElementById('cooldownTimer');
}

// ===== PRO STATUS MANAGEMENT =====
async function checkProStatus() {
  try {
    const storedKey = localStorage.getItem('pro_key');

    const response = await fetch('/api/pro-status', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(storedKey ? { 'X-Pro-Key': storedKey } : {})
      },
    });

    if (response.ok) {
      const data = await response.json();
      appState.isPro = data.isPro || false;
    }
  } catch (error) {
    console.log('Pro status check failed, using default');
    appState.isPro = localStorage.getItem('sigilcraft_pro') === 'true';
  }

  updateProStatus();
}

function updateProStatus() {
  if (domElements.unlockSection) {
    domElements.unlockSection.style.display = appState.isPro ? 'none' : 'block';
  }

  updateGenerateButton();
  renderEnergySelection();
}

async function submitProKey() {
  const key = domElements.proKeyInput?.value?.trim();
  if (!key) {
    showToast('❌ Please enter a pro key', 'error');
    return;
  }

  try {
    const response = await fetch('/api/validate-key', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key })
    });

    const data = await response.json();

    if (data.valid) {
      localStorage.setItem('pro_key', key);
      localStorage.setItem('sigilcraft_pro', 'true');
      appState.isPro = true;
      updateProStatus();
      showToast('✅ Pro features unlocked!', 'success');
      hideProModal();
    } else {
      showToast('❌ Invalid pro key', 'error');
    }
  } catch (error) {
    // Fallback for demo purposes
    if (key === 'sigilcraft_pro_2024' || key === 'changeme_super_secret') {
      localStorage.setItem('sigilcraft_pro', 'true');
      appState.isPro = true;
      updateProStatus();
      showToast('✅ Pro features unlocked!', 'success');
      hideProModal();
    } else {
      showToast('❌ Invalid pro key', 'error');
    }
  }
}

// ===== ENERGY SELECTION SYSTEM =====
function renderEnergySelection() {
  if (!domElements.energyContainer) return;

  const energyHTML = ALL_ENERGIES.map(energy => {
    const isSelected = appState.selectedEnergies.includes(energy);
    const isLocked = !FREE_ENERGIES.includes(energy) && !appState.isPro;

    return `
      <div class="energy-option ${isSelected ? 'selected' : ''} ${isLocked ? 'locked' : ''}"
           onclick="toggleEnergy('${energy}')" 
           title="${ENERGY_DESCRIPTIONS[energy]}">
        <div class="energy-icon">${getEnergyIcon(energy)}</div>
        <div class="energy-name">${energy}</div>
        ${isLocked ? '<div class="lock-icon">🔒</div>' : ''}
      </div>
    `;
  }).join('');

  domElements.energyContainer.innerHTML = `
    <h4>🌟 Energy Vibes</h4>
    <div class="energy-grid">${energyHTML}</div>
    <p class="energy-hint">Select energy types to influence your revolutionary sigil</p>
  `;
}

function getEnergyIcon(energy) {
  const icons = {
    'mystical': '🔮',
    'cosmic': '🌌', 
    'elemental': '🌿',
    'crystal': '💎',
    'shadow': '🌑',
    'light': '✨'
  };
  return icons[energy] || '⚡';
}

function toggleEnergy(energy) {
  if (!FREE_ENERGIES.includes(energy) && !appState.isPro) {
    showToast('🔒 Pro feature - unlock to access all energies!', 'info');
    showProModal();
    return;
  }

  if (appState.selectedEnergies.includes(energy)) {
    appState.selectedEnergies = appState.selectedEnergies.filter(e => e !== energy);
  } else {
    if (appState.isPro) {
      appState.selectedEnergies.push(energy);
    } else {
      appState.selectedEnergies = [energy];
    }
  }

  if (appState.selectedEnergies.length === 0) {
    appState.selectedEnergies = [FREE_ENERGIES[0]];
  }

  renderEnergySelection();
}

// ===== SIGIL GENERATION =====
async function generateSigil() {
  if (appState.isGenerating || appState.cooldownActive) return;

  const phrase = domElements.intentInput?.value?.trim();
  if (!phrase) {
    showToast('✨ Enter your intention first!', 'info');
    return;
  }

  if (phrase.length < 3) {
    showToast('🌟 Your intention needs at least 3 characters', 'warning');
    return;
  }

  if (phrase.length > 200) {
    showToast('❌ Phrase too long (max 200 characters)', 'error');
    return;
  }

  console.log('🎨 Channeling cosmic energies...');
  console.log(`📝 Manifesting: "${phrase}" with vibes: ${appState.selectedEnergies.join('+')}`);

  setGeneratingState(true);
  appState.generationCounter++;

  const startTime = Date.now();

  try {
    const vibe = appState.selectedEnergies.join('+');

    const uniqueParams = {
      phrase,
      vibe,
      timestamp: Date.now(),
      counter: appState.generationCounter,
      randomSeed: Math.random()
    };

    console.log(`🌟 Sending request: phrase="${phrase}", vibe="${vibe}"`);

    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(uniqueParams),
      signal: AbortSignal.timeout(30000)
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Generation failed: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    console.log('✅ Generation response received');

    if (data.success && data.image) {
      appState.lastGeneratedImage = data.image;
      appState.currentSigilData = { 
        phrase, 
        vibe, 
        image: data.image, 
        timestamp: new Date().toISOString(),
        uniqueId: Date.now() + Math.random()
      };

      displaySigil(data);
      saveSigilToGallery(appState.currentSigilData);
      showToast('✨ Revolutionary sigil manifested successfully!', 'success');

      if (!appState.isPro) {
        startCooldown();
      }
    } else {
      throw new Error(data.error || data.details || 'Generation failed - unknown error');
    }
  } catch (error) {
    const duration = Date.now() - startTime;
    console.error('Generation error:', error);

    let errorMessage = 'Generation failed';
    if (error.name === 'AbortError') {
      errorMessage = 'Generation timed out - please try again';
    } else if (error.message && error.message.trim()) {
      errorMessage = error.message;
    }

    showToast(`❌ ${errorMessage}`, 'error');
  } finally {
    setGeneratingState(false);
  }
}

function displaySigil(data) {
  if (!domElements.sigilCanvas) return;

  appState.currentSigilData = data;
  appState.lastGeneratedImage = data.image;

  domElements.sigilCanvas.innerHTML = `
    <img src="${data.image}" 
         alt="Revolutionary Sigil for ${data.phrase}" 
         class="sigil-image"
         style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.3);">
  `;

  if (domElements.resultSection) {
    domElements.resultSection.style.display = 'block';
    domElements.resultSection.scrollIntoView({ behavior: 'smooth' });
  }

  if (domElements.downloadBtn) {
    domElements.downloadBtn.style.display = 'inline-block';
  }
}

function setGeneratingState(isGenerating) {
  appState.isGenerating = isGenerating;

  if (domElements.generateBtn) {
    domElements.generateBtn.disabled = isGenerating;
    domElements.generateBtn.textContent = isGenerating ? '🌀 Manifesting...' : '✨ Generate Revolutionary Sigil';
  }

  if (domElements.loadingIndicator) {
    domElements.loadingIndicator.style.display = isGenerating ? 'block' : 'none';
  }
}

// ===== UI MANAGEMENT =====
function updateGenerateButton() {
  if (!domElements.generateBtn) return;

  if (appState.isGenerating) {
    domElements.generateBtn.textContent = 'Channeling Revolutionary Energies...';
    domElements.generateBtn.disabled = true;
  } else if (appState.cooldownActive) {
    domElements.generateBtn.disabled = true;
  } else {
    domElements.generateBtn.textContent = '🚀 Generate Revolutionary Sigil';
    domElements.generateBtn.disabled = false;
  }
}

function updateCharCounter() {
  if (!domElements.charCounter || !domElements.intentInput) return;

  const count = domElements.intentInput.value.length;
  domElements.charCounter.textContent = `${count}/200 characters`;

  if (count > 150) {
    domElements.charCounter.style.color = '#ff6b6b';
  } else {
    domElements.charCounter.style.color = 'var(--text-secondary)';
  }
}

function updateUI() {
  updateGenerateButton();
  updateCharCounter();
}

// ===== COOLDOWN SYSTEM =====
function startCooldown() {
  if (appState.isPro) return;

  appState.cooldownActive = true;
  let timeLeft = appState.cooldownTime;

  const timer = setInterval(() => {
    timeLeft--;
    updateCooldownDisplay(timeLeft);

    if (timeLeft <= 0) {
      clearInterval(timer);
      appState.cooldownActive = false;
      updateCooldownDisplay(0);
    }
  }, 1000);

  updateCooldownDisplay(timeLeft);
}

function updateCooldownDisplay(timeLeft) {
  if (domElements.cooldownTimer) {
    if (timeLeft > 0) {
      domElements.cooldownTimer.textContent = `Next generation in ${timeLeft}s`;
      domElements.cooldownTimer.style.display = 'block';
    } else {
      domElements.cooldownTimer.style.display = 'none';
    }
  }

  if (domElements.generateBtn) {
    domElements.generateBtn.disabled = appState.cooldownActive || appState.isGenerating;
    if (appState.cooldownActive && !appState.isGenerating) {
      domElements.generateBtn.textContent = `⏱️ Wait ${timeLeft}s`;
    } else if (!appState.isGenerating) {
      domElements.generateBtn.textContent = '🚀 Generate Revolutionary Sigil';
    }
  }
}

// ===== GALLERY SYSTEM =====
function saveSigilToGallery(sigilData) {
  const galleryItem = {
    id: Date.now(),
    uniqueId: appState.generationCounter,
    phrase: sigilData.phrase,
    vibe: sigilData.vibe,
    image: sigilData.image,
    timestamp: new Date().toISOString()
  };

  appState.sigilGallery.unshift(galleryItem);

  // Keep only last 20 sigils
  if (appState.sigilGallery.length > 20) {
    appState.sigilGallery = appState.sigilGallery.slice(0, 20);
  }

  localStorage.setItem('sigil_gallery', JSON.stringify(appState.sigilGallery));
  renderGallery();
}

function renderGallery() {
  if (!domElements.galleryContainer) return;

  if (appState.sigilGallery.length === 0) {
    domElements.galleryContainer.innerHTML = `
      <h4>🎨 Your Sigil Gallery</h4>
      <p class="gallery-empty">Your revolutionary sigils will appear here</p>
    `;
    return;
  }

  const galleryHTML = appState.sigilGallery.map(sigil => `
    <div class="gallery-item" data-sigil-id="${sigil.id}">
      <img src="${sigil.image}" alt="Sigil for ${sigil.phrase}" class="gallery-thumbnail" onclick="viewSigil(${sigil.id})">
      <div class="gallery-info">
        <div class="gallery-phrase">"${sigil.phrase}"</div>
        <div class="gallery-meta">${sigil.vibe} • ${new Date(sigil.timestamp).toLocaleDateString()}</div>
      </div>
      <div class="gallery-actions">
        <button onclick="downloadSigilFromGallery(${sigil.id})" class="gallery-btn" title="Download">📥</button>
        <button onclick="shareSigil(${sigil.id})" class="gallery-btn" title="Share">📤</button>
        <button onclick="deleteSigil(${sigil.id})" class="gallery-btn delete" title="Delete">🗑️</button>
      </div>
    </div>
  `).join('');

  domElements.galleryContainer.innerHTML = `
    <h4>🎨 Your Sigil Gallery (${appState.sigilGallery.length})</h4>
    <div class="gallery-grid">${galleryHTML}</div>
  `;
}

function viewSigil(sigilId) {
  const sigil = appState.sigilGallery.find(s => s.id == sigilId);
  if (!sigil) return;

  appState.currentSigilData = sigil;
  displaySigil(sigil);
}

function deleteSigil(sigilId) {
  if (confirm('Delete this revolutionary sigil from your gallery?')) {
    appState.sigilGallery = appState.sigilGallery.filter(s => s.id != sigilId);
    localStorage.setItem('sigil_gallery', JSON.stringify(appState.sigilGallery));
    renderGallery();
    showToast('🗑️ Sigil removed from gallery', 'info');
  }
}

// ===== DOWNLOAD SYSTEM =====
function downloadSigil() {
  if (!appState.lastGeneratedImage) {
    showToast('🌟 Generate a sigil first!', 'warning');
    return;
  }

  const phrase = appState.currentSigilData?.phrase || 'sigil';
  const timestamp = new Date().toISOString().split('T')[0];
  const uniqueId = Date.now();
  const filename = `sigilcraft-revolutionary-${phrase.replace(/\s+/g, '-').toLowerCase()}-${timestamp}-${uniqueId}.png`;

  const link = document.createElement('a');
  link.download = filename;
  link.href = appState.lastGeneratedImage;
  link.click();

  showToast('✨ Revolutionary sigil downloaded!', 'success');
}

function downloadSigilFromGallery(sigilId) {
  const sigil = appState.sigilGallery.find(s => s.id == sigilId);
  if (sigil) {
    const phrase = sigil.phrase.replace(/\s+/g, '-').toLowerCase();
    const timestamp = new Date(sigil.timestamp).toISOString().split('T')[0];
    const uniqueId = sigil.uniqueId || Date.now();
    const filename = `sigilcraft-revolutionary-${phrase}-${timestamp}-${uniqueId}.png`;

    const link = document.createElement('a');
    link.download = filename;
    link.href = sigil.image;
    link.click();

    showToast('✨ Sigil downloaded', 'success');
  }
}

// ===== SOCIAL SHARING SYSTEM =====
function shareSigil(sigilId) {
  const sigil = appState.sigilGallery.find(s => s.id == sigilId);
  if (!sigil) return;

  appState.currentSigilData = sigil;

  if (navigator.share) {
    navigator.share({
      title: 'My Revolutionary Sigil',
      text: `Check out this revolutionary text-responsive sigil I created for "${sigil.phrase}"`,
      url: window.location.href
    });
  } else {
    navigator.clipboard.writeText(window.location.href).then(() => {
      showToast('✨ Link copied to clipboard!', 'success');
    });
  }
}

// ===== PRO MODAL SYSTEM =====
function showProModal() {
  const modal = document.getElementById('proModal');
  if (modal) {
    modal.style.display = 'flex';
  }
}

function hideProModal() {
  const modal = document.getElementById('proModal');
  if (modal) {
    modal.style.display = 'none';
  }
}

// ===== EVENT HANDLERS =====
function setupEvents() {
  if (domElements.generateBtn) {
    domElements.generateBtn.addEventListener('click', generateSigil);
  }

  if (domElements.intentInput) {
    domElements.intentInput.addEventListener('input', handleTextInput);
    domElements.intentInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !appState.isGenerating && !appState.cooldownActive) {
        generateSigil();
      }
    });
  }

  if (domElements.downloadBtn) {
    domElements.downloadBtn.addEventListener('click', downloadSigil);
  }

  if (domElements.proKeySubmit) {
    domElements.proKeySubmit.addEventListener('click', submitProKey);
  }

  // Close modals on outside click
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
      e.target.style.display = 'none';
    }
  });
}

function handleTextInput() {
  updateCharCounter();
  analyzeText();
}

// ===== TEXT ANALYSIS DISPLAY =====
function analyzeText() {
  if (!domElements.textAnalysis || !domElements.intentInput) return;

  const text = domElements.intentInput.value.trim();

  if (!text) {
    domElements.textAnalysis.innerHTML = `
      <h4>📊 Text Analysis</h4>
      <p class="analysis-prompt">Enter text above to see how it will influence your sigil</p>
    `;
    return;
  }

  const analysis = performTextAnalysis(text);

  domElements.textAnalysis.innerHTML = `
    <h4>📊 Revolutionary Text Analysis</h4>
    <div class="analysis-grid">
      <div class="analysis-item">
        <span class="analysis-label">Length:</span>
        <span class="analysis-value">${analysis.length} chars</span>
      </div>
      <div class="analysis-item">
        <span class="analysis-label">Words:</span>
        <span class="analysis-value">${analysis.words}</span>
      </div>
      <div class="analysis-item">
        <span class="analysis-label">Unique Characters:</span>
        <span class="analysis-value">${analysis.uniqueChars}</span>
      </div>
      <div class="analysis-item">
        <span class="analysis-label">Vowel Ratio:</span>
        <span class="analysis-value">${analysis.vowelRatio}%</span>
      </div>
      <div class="analysis-item">
        <span class="analysis-label">Complexity:</span>
        <span class="analysis-value">${analysis.complexity}</span>
      </div>
      <div class="analysis-item">
        <span class="analysis-label">Energy:</span>
        <span class="analysis-value">${analysis.energy}</span>
      </div>
    </div>
    <p class="analysis-hint">This analysis influences your sigil's revolutionary design</p>
  `;
}

function performTextAnalysis(text) {
  const words = text.split(/\s+/).filter(word => word.length > 0).length;
  const uniqueChars = new Set(text.toLowerCase().replace(/\s/g, '')).size;
  const vowels = (text.match(/[aeiouAEIOU]/g) || []).length;
  const vowelRatio = text.length > 0 ? Math.round((vowels / text.length) * 100) : 0;

  let complexity = 'Simple';
  if (uniqueChars > 8) complexity = 'Complex';
  else if (uniqueChars > 5) complexity = 'Moderate';

  let energy = 'Balanced';
  if (vowelRatio > 40) energy = 'High';
  else if (vowelRatio < 20) energy = 'Grounded';

  return {
    length: text.length,
    words,
    uniqueChars,
    vowelRatio,
    complexity,
    energy
  };
}

// ===== TOAST NOTIFICATIONS =====
function showToast(message, type = 'info') {
  console.log(`Toast: ${message} (${type})`);

  // Remove existing toasts
  const existingToasts = document.querySelectorAll('.toast');
  existingToasts.forEach(toast => toast.remove());

  // Create new toast
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;

  // Style the toast
  Object.assign(toast.style, {
    position: 'fixed',
    top: '20px',
    right: '20px',
    padding: '15px 20px',
    borderRadius: '8px',
    color: 'white',
    fontWeight: '600',
    zIndex: '10000',
    minWidth: '250px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
    transform: 'translateX(300px)',
    transition: 'transform 0.3s ease'
  });

  // Set background color based on type
  const colors = {
    success: '#4CAF50',
    error: '#f44336',
    warning: '#ff9800',
    info: '#2196F3'
  };
  toast.style.backgroundColor = colors[type] || colors.info;

  // Add to DOM and animate in
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.transform = 'translateX(0)';
  }, 100);

  // Auto remove after delay
  setTimeout(() => {
    toast.style.transform = 'translateX(300px)';
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }, 4000);
}

// Expose functions globally for onclick handlers
window.toggleEnergy = toggleEnergy;
window.viewSigil = viewSigil;
window.deleteSigil = deleteSigil;
window.downloadSigilFromGallery = downloadSigilFromGallery;
window.shareSigil = shareSigil;
window.submitProKey = submitProKey;
window.showProModal = showProModal;
window.hideProModal = hideProModal;