
// ===== SIGILCRAFT - REVOLUTIONARY TEXT-RESPONSIVE SIGIL GENERATOR =====

// Configuration
const FREE_ENERGIES = ["mystical", "elemental", "light"];
const ALL_ENERGIES = ["mystical", "cosmic", "elemental", "crystal", "shadow", "light"];
const COOLDOWN_TIME = 10000; // 10 seconds

// Global state
let appState = {
  selectedEnergies: [FREE_ENERGIES[0]],
  lastGeneratedImage: null,
  isGenerating: false,
  cooldownActive: false,
  isPro: false,
  sigilGallery: JSON.parse(localStorage.getItem('sigil_gallery') || '[]'),
  currentSigilData: null
};

// DOM elements cache
let domElements = {};

// Cache DOM elements
function cacheElements() {
  domElements = {
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
    proKeyModal: document.getElementById('proKeyModal'),
    textAnalysis: document.getElementById('textAnalysis')
  };
}

// Setup event listeners
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

// Handle text input with analysis
function handleTextInput() {
  updateCharCounter();
  analyzeText();
}

// ===== TEXT ANALYSIS DISPLAY =====
function analyzeText() {
  const text = domElements.intentInput?.value?.trim() || '';
  
  if (!text || !domElements.textAnalysis) return;
  
  // Perform basic analysis
  const analysis = {
    length: text.length,
    wordCount: text.split(/\s+/).filter(word => word.length > 0).length,
    uniqueChars: new Set(text.toLowerCase().replace(/\s/g, '')).size,
    vowelRatio: (text.match(/[aeiou]/gi) || []).length / Math.max(text.length, 1),
    complexity: calculateComplexity(text)
  };
  
  // Update analysis display
  domElements.textAnalysis.innerHTML = `
    <h4>📊 Text Analysis</h4>
    <div class="analysis-grid">
      <div class="analysis-item">
        <span class="label">Words:</span>
        <span class="value">${analysis.wordCount}</span>
      </div>
      <div class="analysis-item">
        <span class="label">Unique chars:</span>
        <span class="value">${analysis.uniqueChars}</span>
      </div>
      <div class="analysis-item">
        <span class="label">Vowel ratio:</span>
        <span class="value">${(analysis.vowelRatio * 100).toFixed(1)}%</span>
      </div>
      <div class="analysis-item">
        <span class="label">Complexity:</span>
        <span class="value complexity-${getComplexityLevel(analysis.complexity)}">${getComplexityLevel(analysis.complexity)}</span>
      </div>
    </div>
    <div class="energy-prediction">
      <span class="label">Predicted energy:</span>
      <span class="value">${predictEnergy(text)}</span>
    </div>
  `;
}

function calculateComplexity(text) {
  let complexity = 0;
  complexity += new Set(text.toLowerCase().replace(/\s/g, '')).size * 0.1;
  complexity += text.split(/\s+/).length * 0.15;
  complexity += (text.match(/[aeiou]/gi) || []).length / text.length * 0.2;
  return Math.min(Math.max(complexity, 0.3), 1.0);
}

function getComplexityLevel(complexity) {
  if (complexity < 0.4) return 'Simple';
  if (complexity < 0.7) return 'Medium';
  return 'Complex';
}

function predictEnergy(text) {
  const energyWords = {
    fire: ['fire', 'flame', 'burn', 'passion', 'energy', 'power'],
    water: ['water', 'flow', 'calm', 'peace', 'healing', 'emotion'],
    earth: ['earth', 'ground', 'stable', 'home', 'money', 'growth'],
    air: ['air', 'wind', 'thought', 'mind', 'freedom', 'ideas'],
    light: ['light', 'bright', 'sun', 'clarity', 'divine', 'pure'],
    shadow: ['dark', 'shadow', 'mystery', 'hidden', 'transform'],
    love: ['love', 'heart', 'romance', 'care', 'soul'],
    wisdom: ['wisdom', 'knowledge', 'learn', 'truth', 'insight']
  };
  
  const lowerText = text.toLowerCase();
  let maxScore = 0;
  let dominantEnergy = 'mystical';
  
  for (const [energy, keywords] of Object.entries(energyWords)) {
    let score = 0;
    keywords.forEach(keyword => {
      if (lowerText.includes(keyword)) score++;
    });
    
    if (score > maxScore) {
      maxScore = score;
      dominantEnergy = energy;
    }
  }
  
  return dominantEnergy;
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

    appState.isPro = localPro || serverPro;
    updateUI();

  } catch (error) {
    console.log('Pro status check failed, falling back to local storage');
    appState.isPro = localStorage.getItem('sigil_pro') === '1';
    updateUI();
  }
}

async function submitProKey() {
  const key = domElements.proKeyInput?.value?.trim();
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
      appState.isPro = true;
      showToast('✨ Pro features unlocked!', 'success');
      updateUI();
      if (domElements.proKeyModal) {
        domElements.proKeyModal.style.display = 'none';
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
  if (!domElements.energyContainer) return;

  const availableEnergies = appState.isPro ? ALL_ENERGIES : FREE_ENERGIES;

  domElements.energyContainer.innerHTML = `
    <h3>Choose Your Vibe</h3>
    <div class="energy-grid">
      ${availableEnergies.map(energy => `
        <div class="energy-option ${appState.selectedEnergies.includes(energy) ? 'selected' : ''}" 
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

  console.log('🚀 Channeling revolutionary energies...');
  console.log(`📝 Manifesting: "${phrase}" with vibes: ${appState.selectedEnergies.join('+')}`);

  appState.isGenerating = true;
  updateGenerateButton();
  showLoading();

  const startTime = Date.now();

  try {
    const vibe = appState.selectedEnergies.join('+');

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
      appState.lastGeneratedImage = data.image;
      appState.currentSigilData = { phrase, vibe, image: data.image, timestamp: new Date().toISOString() };

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

// ===== CANVAS & RENDERING =====
async function renderSigil(imageData) {
  return new Promise((resolve) => {
    if (!domElements.canvas) {
      resolve();
      return;
    }

    const ctx = domElements.canvas.getContext('2d');
    const img = new Image();

    img.onload = () => {
      ctx.clearRect(0, 0, domElements.canvas.width, domElements.canvas.height);

      const scale = Math.min(
        domElements.canvas.width / img.width, 
        domElements.canvas.height / img.height
      );
      const x = (domElements.canvas.width - img.width * scale) / 2;
      const y = (domElements.canvas.height - img.height * scale) / 2;

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
  const filename = `sigilcraft-revolutionary-${phrase}-${timestamp}.png`;

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
    const filename = `sigilcraft-revolutionary-${phrase}-${timestamp}.png`;

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

// ===== UI UPDATES =====
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
  if (!domElements.charCount || !domElements.intentInput) return;

  const count = domElements.intentInput.value.length;
  domElements.charCount.textContent = `${count}/200`;

  if (count > 200) {
    domElements.charCount.style.color = '#ff4444';
  } else if (count > 150) {
    domElements.charCount.style.color = '#ffaa00';
  } else {
    domElements.charCount.style.color = '#888';
  }
}

function updateProInterface() {
  if (domElements.proBadge) {
    domElements.proBadge.style.display = appState.isPro ? 'block' : 'none';
  }

  if (domElements.unlockSection) {
    domElements.unlockSection.style.display = appState.isPro ? 'none' : 'block';
  }
}

function startCooldown() {
  appState.cooldownActive = true;
  let timeLeft = COOLDOWN_TIME / 1000;

  const countdown = setInterval(() => {
    if (domElements.generateBtn) {
      domElements.generateBtn.textContent = `Wait ${timeLeft}s`;
    }

    timeLeft--;

    if (timeLeft <= 0) {
      clearInterval(countdown);
      appState.cooldownActive = false;
      updateGenerateButton();
    }
  }, 1000);
}

function showResult() {
  if (domElements.canvasContainer) {
    domElements.canvasContainer.classList.remove('hidden');
  }
  if (domElements.downloadBtn) {
    domElements.downloadBtn.style.display = 'block';
  }
}

function showLoading() {
  if (domElements.loading) {
    domElements.loading.style.display = 'flex';
  }
}

function hideLoading() {
  if (domElements.loading) {
    domElements.loading.style.display = 'none';
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
  analyzeText();
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', async () => {
  console.log('🚀 Initializing Revolutionary Sigil Generator...');

  try {
    cacheElements();
    setupEvents();
    await checkProStatus();
    updateUI();

    console.log('✅ Revolutionary app initialization complete!');
  } catch (error) {
    console.error('❌ Initialization failed:', error);
    showToast('❌ App initialization failed', 'error');
  }
});

// Make functions globally available
window.toggleEnergy = toggleEnergy;
window.viewSigil = viewSigil;
window.deleteSigil = deleteSigil;
window.downloadSigilFromGallery = downloadSigilFromGallery;
window.shareSigil = shareSigil;
window.copyShareLink = copyShareLink;
window.shareViaNative = shareViaNative;
