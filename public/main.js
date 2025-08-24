
// Revolutionary Text-Responsive Sigil Generator - Frontend
// Enhanced with quantum-level text analysis and true uniqueness

// ===== CONSTANTS =====
if (typeof FREE_ENERGIES === 'undefined') {
  var FREE_ENERGIES = ['mystical', 'elemental', 'light'];
  var PRO_ENERGIES = ['cosmic', 'crystal', 'shadow'];
  var ALL_ENERGIES = [...FREE_ENERGIES, ...PRO_ENERGIES];
}

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
if (typeof appState === 'undefined') {
var appState = {
  isPro: false,
  isGenerating: false,
  cooldownActive: false,
  cooldownTime: 30,
  selectedEnergies: [FREE_ENERGIES[0]],
  currentSigilData: null,
  sigilGallery: JSON.parse(localStorage.getItem('sigil_gallery') || '[]'),
  lastGeneratedImage: null,
  generationCounter: 0 // Add counter for uniqueness
};

// ===== DOM ELEMENTS =====
if (typeof domElements === 'undefined') {
var domElements = {
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

async function initializeApp() {
  console.log('🚀 Initializing Revolutionary Sigil Generator...');
  
  initializeDOM();
  await checkProStatus();
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
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      throw new Error('Response is not JSON');
    }
    
    const data = await response.json();
    appState.isPro = data.isPro || false;
    updateProStatus();
  } catch (error) {
    console.error('Error checking pro status:', error);
    appState.isPro = false;
    updateProStatus();
  }
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
      appState.isPro = true;
      updateProStatus();
      showToast('✅ Pro features unlocked!', 'success');
      document.getElementById('proKeyModal').style.display = 'none';
    } else {
      showToast('❌ Invalid pro key', 'error');
    }
  } catch (error) {
    console.error('Key validation error:', error);
    showToast('❌ Validation failed', 'error');
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
    <p class="energy-hint">Select one or more energy types to influence your sigil</p>
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
    return;
  }

  if (appState.selectedEnergies.includes(energy)) {
    appState.selectedEnergies = appState.selectedEnergies.filter(e => e !== energy);
  } else {
    appState.selectedEnergies.push(energy);
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

  if (phrase.length > 200) {
    showToast('❌ Phrase too long (max 200 characters)', 'error');
    return;
  }

  console.log('🎨 Channeling cosmic energies...');
  console.log(`📝 Manifesting: "${phrase}" with vibes: ${appState.selectedEnergies.join('+')}`);

  appState.isGenerating = true;
  appState.generationCounter++; // Increment for uniqueness
  updateGenerateButton();
  showLoading();

  const startTime = Date.now();

  try {
    const vibe = appState.selectedEnergies.join('+');
    
    // Add uniqueness parameters
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

      await renderSigil(data.image);
      showResult();
      saveToGallery(appState.currentSigilData);
      renderGallery();

      hideLoading();
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
    appState.isGenerating = false;
    updateGenerateButton();
  }
}

// ===== UI MANAGEMENT =====
function showLoading() {
  if (domElements.loadingIndicator) {
    domElements.loadingIndicator.style.display = 'flex';
  }
}

function hideLoading() {
  if (domElements.loadingIndicator) {
    domElements.loadingIndicator.style.display = 'none';
  }
}

function showResult() {
  if (domElements.resultSection) {
    domElements.resultSection.style.display = 'block';
    domElements.resultSection.scrollIntoView({ behavior: 'smooth' });
  }
}

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
    if (domElements.generateBtn) {
      domElements.generateBtn.textContent = `Wait ${timeLeft}s for next generation`;
      domElements.generateBtn.disabled = true;
    }
    
    timeLeft--;
    
    if (timeLeft < 0) {
      clearInterval(timer);
      appState.cooldownActive = false;
      updateGenerateButton();
    }
  }, 1000);
}

// ===== SIGIL RENDERING =====
async function renderSigil(imageData) {
  if (!domElements.sigilCanvas || !imageData) return;
  
  try {
    domElements.sigilCanvas.src = imageData;
    domElements.sigilCanvas.style.display = 'block';
  } catch (error) {
    console.error('Error rendering sigil:', error);
    showToast('❌ Error displaying sigil', 'error');
  }
}

// ===== GALLERY SYSTEM =====
function saveToGallery(sigilData) {
  const galleryItem = {
    id: Date.now() + Math.random(), // Ensure unique IDs
    phrase: sigilData.phrase,
    vibe: sigilData.vibe,
    image: sigilData.image,
    timestamp: sigilData.timestamp,
    uniqueId: sigilData.uniqueId || Date.now()
  };

  appState.sigilGallery.unshift(galleryItem);

  // Limit gallery size
  if (appState.sigilGallery.length > 50) {
    appState.sigilGallery = appState.sigilGallery.slice(0, 50);
  }

  localStorage.setItem('sigil_gallery', JSON.stringify(appState.sigilGallery));
}

function renderGallery() {
  if (!domElements.galleryContainer) return;

  if (appState.sigilGallery.length === 0) {
    domElements.galleryContainer.innerHTML = '<p class="no-gallery">No sigils created yet. Generate your first revolutionary sigil!</p>';
    return;
  }

  domElements.galleryContainer.innerHTML = `
    <h3>Your Sacred Gallery</h3>
    <div class="gallery-grid">
      ${appState.sigilGallery.map(sigil => `
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
  const sigil = appState.sigilGallery.find(s => s.id == sigilId);
  if (!sigil) return;

  appState.currentSigilData = sigil;
  renderSigil(sigil.image);
  showResult();
}

function deleteSigil(sigilId) {
  if (confirm('Delete this sigil from your gallery?')) {
    appState.sigilGallery = appState.sigilGallery.filter(s => s.id != sigilId);
    localStorage.setItem('sigil_gallery', JSON.stringify(appState.sigilGallery));
    renderGallery();
    showToast('🗑️ Sigil removed from gallery', 'info');
  }
}

// ===== DOWNLOAD SYSTEM =====
function downloadSigil() {
  if (!appState.currentSigilData) {
    showToast('❌ No sigil to download', 'error');
    return;
  }

  const phrase = appState.currentSigilData.phrase.replace(/\s+/g, '-').toLowerCase();
  const timestamp = new Date().toISOString().split('T')[0];
  const uniqueId = Date.now();
  const filename = `sigilcraft-revolutionary-${phrase}-${timestamp}-${uniqueId}.png`;

  const link = document.createElement('a');
  link.download = filename;
  link.href = appState.currentSigilData.image;
  link.click();

  showToast('✨ Revolutionary sigil downloaded to your device', 'success');
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
  showShareModal();
}

function showShareModal() {
  if (domElements.shareModal) {
    domElements.shareModal.style.display = 'flex';
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
      title: 'My Revolutionary Sigil',
      text: `Check out this revolutionary text-responsive sigil I created for "${appState.currentSigilData.phrase}"`,
      url: window.location.href
    });
  } else {
    copyShareLink();
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
        <span class="analysis-value">${analysis.dominantEnergy}</span>
      </div>
    </div>
  `;
}

function performTextAnalysis(text) {
  const length = text.length;
  const words = text.split(/\s+/).length;
  const uniqueChars = new Set(text.toLowerCase().replace(/\s/g, '')).size;
  const vowels = (text.match(/[aeiou]/gi) || []).length;
  const vowelRatio = Math.round((vowels / Math.max(length, 1)) * 100);
  
  // Simple complexity calculation
  let complexity = 'Simple';
  if (uniqueChars > 15 || words > 5) complexity = 'Complex';
  else if (uniqueChars > 10 || words > 3) complexity = 'Moderate';
  
  // Dominant energy detection (simplified)
  const energyKeywords = {
    mystical: ['magic', 'spirit', 'soul', 'divine', 'sacred'],
    cosmic: ['space', 'star', 'universe', 'cosmic', 'galaxy'],
    elemental: ['earth', 'fire', 'water', 'air', 'nature'],
    crystal: ['crystal', 'gem', 'diamond', 'clear', 'pure'],
    shadow: ['dark', 'shadow', 'hidden', 'mystery', 'deep'],
    light: ['light', 'bright', 'sun', 'radiant', 'shine']
  };
  
  let dominantEnergy = 'Neutral';
  let maxMatches = 0;
  
  for (const [energy, keywords] of Object.entries(energyKeywords)) {
    const matches = keywords.filter(keyword => 
      text.toLowerCase().includes(keyword)
    ).length;
    
    if (matches > maxMatches) {
      maxMatches = matches;
      dominantEnergy = energy.charAt(0).toUpperCase() + energy.slice(1);
    }
  }
  
  return {
    length,
    words,
    uniqueChars,
    vowelRatio,
    complexity,
    dominantEnergy
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

// ===== UTILITY FUNCTIONS =====
function formatTimestamp(timestamp) {
  return new Date(timestamp).toLocaleString();
}

function validateInput(text) {
  if (!text || text.trim().length === 0) {
    return { valid: false, error: 'Please enter some text' };
  }
  
  if (text.length > 200) {
    return { valid: false, error: 'Text too long (max 200 characters)' };
  }
  
  return { valid: true };
}

// Expose functions globally for onclick handlers
window.toggleEnergy = toggleEnergy;
window.viewSigil = viewSigil;
window.deleteSigil = deleteSigil;
window.downloadSigilFromGallery = downloadSigilFromGallery;
window.shareSigil = shareSigil;
window.copyShareLink = copyShareLink;
window.shareViaNative = shareViaNative;
