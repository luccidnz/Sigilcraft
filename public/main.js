
// ===== APPLICATION STATE =====
const appState = {
  isGenerating: false,
  isPro: false,
  cooldownActive: false,
  cooldownTime: 30,
  currentSigilData: null,
  lastGeneratedImage: null,
  sigilGallery: []
};

// ===== DOM ELEMENTS =====
const domElements = {};

function initializeDOM() {
  domElements.generateBtn = document.getElementById('generateBtn');
  domElements.intentInput = document.getElementById('intentInput');
  domElements.sigilCanvas = document.getElementById('sigilCanvas');
  domElements.resultSection = document.getElementById('resultSection');
  domElements.downloadBtn = document.getElementById('downloadBtn');
  domElements.loadingIndicator = document.getElementById('loadingIndicator');
  domElements.charCounter = document.querySelector('.char-count');
  domElements.textAnalysis = document.getElementById('textAnalysis');
  domElements.energyGrid = document.getElementById('energyGrid');
  domElements.proBadge = document.getElementById('proBadge');
  domElements.proKeySubmit = document.getElementById('proKeySubmit');
}

// ===== SIGIL GENERATION =====
async function generateSigil() {
  if (appState.isGenerating || appState.cooldownActive) return;

  const phrase = domElements.intentInput?.value?.trim();
  if (!phrase) {
    showToast('⚠️ Please enter your intention first', 'warning');
    return;
  }

  const selectedVibe = document.querySelector('.energy-option.selected')?.dataset?.vibe || 'mystical';
  
  setGeneratingState(true);
  const startTime = Date.now();

  try {
    console.log(`🎨 Generating sigil: "${phrase}" with vibe: ${selectedVibe}`);
    
    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phrase, vibe: selectedVibe }),
      signal: AbortSignal.timeout(30000)
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `Server error: ${response.status}`);
    }

    const data = await response.json();
    const duration = Date.now() - startTime;

    console.log(`✅ Generation completed in ${duration}ms`);
    displaySigil(data);
    
    // Add to gallery
    addToGallery(data);
    
    // Start cooldown for non-pro users
    if (!appState.isPro) {
      startCooldown();
    }
    
    showToast('✨ Revolutionary sigil manifested!', 'success');

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

// ===== DOWNLOAD FUNCTIONALITY =====
function downloadSigil() {
  if (!appState.lastGeneratedImage) {
    showToast('⚠️ No sigil to download', 'warning');
    return;
  }

  try {
    const link = document.createElement('a');
    link.href = appState.lastGeneratedImage;
    link.download = `revolutionary-sigil-${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showToast('📥 Sigil downloaded successfully!', 'success');
  } catch (error) {
    console.error('Download error:', error);
    showToast('❌ Download failed', 'error');
  }
}

// ===== TEXT INPUT HANDLING =====
function handleTextInput() {
  updateCharCounter();
  analyzeText();
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

// ===== TEXT ANALYSIS =====
function analyzeText() {
  if (!domElements.textAnalysis || !domElements.intentInput) return;

  const text = domElements.intentInput.value.trim();

  if (!text) {
    domElements.textAnalysis.innerHTML = `
      <h4>📊 Text Analysis</h4>
      <p class="analysis-prompt">Enter text above to see mystical analysis...</p>
    `;
    return;
  }

  const wordCount = text.split(/\s+/).filter(word => word.length > 0).length;
  const charCount = text.length;
  const vowelCount = (text.match(/[aeiouAEIOU]/g) || []).length;
  const consonantCount = (text.match(/[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]/g) || []).length;
  
  let complexity = 'Simple';
  if (wordCount > 5) complexity = 'Medium';
  if (wordCount > 10) complexity = 'Complex';

  const predictedVibe = predictVibe(text);

  domElements.textAnalysis.innerHTML = `
    <h4>📊 Text Analysis</h4>
    <div class="analysis-grid">
      <div class="analysis-item">
        <span class="label">Words:</span>
        <span class="value">${wordCount}</span>
      </div>
      <div class="analysis-item">
        <span class="label">Characters:</span>
        <span class="value">${charCount}</span>
      </div>
      <div class="analysis-item">
        <span class="label">Vowels:</span>
        <span class="value">${vowelCount}</span>
      </div>
      <div class="analysis-item">
        <span class="label">Consonants:</span>
        <span class="value">${consonantCount}</span>
      </div>
    </div>
    <div class="energy-prediction">
      <span class="label">Predicted Energy:</span>
      <span class="value">${predictedVibe}</span>
    </div>
  `;
}

function predictVibe(text) {
  const lowerText = text.toLowerCase();
  
  if (lowerText.includes('love') || lowerText.includes('heart') || lowerText.includes('compassion')) return 'crystal';
  if (lowerText.includes('peace') || lowerText.includes('calm') || lowerText.includes('light')) return 'light';
  if (lowerText.includes('power') || lowerText.includes('strength') || lowerText.includes('dark')) return 'shadow';
  if (lowerText.includes('nature') || lowerText.includes('earth') || lowerText.includes('fire')) return 'elemental';
  if (lowerText.includes('star') || lowerText.includes('cosmic') || lowerText.includes('universe')) return 'cosmic';
  
  return 'mystical';
}

// ===== ENERGY SELECTION =====
function renderEnergySelection() {
  const energyContainer = document.getElementById('energyGrid');
  if (!energyContainer) return;

  const energies = [
    { id: 'mystical', icon: '🔮', name: 'Mystical', description: 'Ancient wisdom & mystery' },
    { id: 'cosmic', icon: '🌌', name: 'Cosmic', description: 'Universal connection' },
    { id: 'elemental', icon: '🌿', name: 'Elemental', description: 'Natural forces' },
    { id: 'crystal', icon: '💎', name: 'Crystal', description: 'Clarity & healing' },
    { id: 'shadow', icon: '🌑', name: 'Shadow', description: 'Hidden power' },
    { id: 'light', icon: '☀️', name: 'Light', description: 'Pure radiance' }
  ];

  energyContainer.innerHTML = energies.map(energy => `
    <div class="energy-option ${energy.id === 'mystical' ? 'selected' : ''}" 
         data-vibe="${energy.id}" 
         onclick="selectEnergy('${energy.id}')">
      <i>${energy.icon}</i>
      <span>${energy.name}</span>
    </div>
  `).join('');
}

function selectEnergy(vibeId) {
  document.querySelectorAll('.energy-option').forEach(option => {
    option.classList.remove('selected');
  });
  
  const selectedOption = document.querySelector(`[data-vibe="${vibeId}"]`);
  if (selectedOption) {
    selectedOption.classList.add('selected');
  }
}

// ===== GALLERY MANAGEMENT =====
function addToGallery(sigilData) {
  if (!sigilData) return;
  
  const galleryItem = {
    id: Date.now(),
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
  const galleryContainer = document.getElementById('sigilGallery');
  if (!galleryContainer || appState.sigilGallery.length === 0) return;

  galleryContainer.innerHTML = appState.sigilGallery.map(item => `
    <div class="gallery-item" onclick="viewGalleryItem('${item.id}')">
      <img src="${item.image}" alt="Sigil for ${item.phrase}" loading="lazy">
      <div class="gallery-info">
        <span class="gallery-phrase">${item.phrase.substring(0, 30)}${item.phrase.length > 30 ? '...' : ''}</span>
        <span class="gallery-vibe">${item.vibe}</span>
      </div>
    </div>
  `).join('');
}

function viewGalleryItem(itemId) {
  const item = appState.sigilGallery.find(sigil => sigil.id == itemId);
  if (item) {
    displaySigil(item);
  }
}

// ===== PRO FEATURES =====
async function checkProStatus() {
  try {
    const response = await fetch('/api/pro-status');
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
  if (domElements.proBadge) {
    domElements.proBadge.style.display = appState.isPro ? 'flex' : 'none';
  }
}

function submitProKey() {
  const keyInput = document.getElementById('proKeyInput');
  if (!keyInput) return;

  const key = keyInput.value.trim();
  if (key === 'changeme_super_secret') {
    appState.isPro = true;
    localStorage.setItem('sigilcraft_pro', 'true');
    updateProStatus();
    closeProModal();
    showToast('✨ Pro features activated!', 'success');
  } else {
    showToast('❌ Invalid pro key', 'error');
  }
}

function closeProModal() {
  const modal = document.getElementById('proModal');
  if (modal) {
    modal.style.display = 'none';
  }
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
      updateUI();
    }
  }, 1000);

  updateUI();
}

function updateCooldownDisplay(timeLeft) {
  if (domElements.generateBtn && timeLeft > 0) {
    domElements.generateBtn.textContent = `⏳ Wait ${timeLeft}s (Get Pro for unlimited)`;
    domElements.generateBtn.disabled = true;
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

function updateUI() {
  updateGenerateButton();
  updateCharCounter();
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

// ===== TOAST NOTIFICATIONS =====
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 12px 20px;
    border-radius: 8px;
    color: white;
    font-weight: 500;
    z-index: 10000;
    animation: slideIn 0.3s ease;
  `;
  
  if (type === 'success') toast.style.background = '#4CAF50';
  else if (type === 'error') toast.style.background = '#f44336';
  else if (type === 'warning') toast.style.background = '#ff9800';
  else toast.style.background = '#2196F3';
  
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// ===== INITIALIZATION =====
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

// Start the application when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeApp);
} else {
  initializeApp();
}
