
// ===== SIGILCRAFT - MODERN QUANTUM SIGIL GENERATOR =====

// Configuration
const FREE_ENERGIES = ["mystical", "elemental", "light"];
const ALL_ENERGIES = ["mystical", "cosmic", "elemental", "crystal", "shadow", "light"];
const COOLDOWN_TIME = 10000; // 10 seconds

// State
let state = {
  selectedEnergies: [FREE_ENERGIES[0]],
  lastGeneratedImage: null,
  isGenerating: false,
  cooldownActive: false,
  isPro: false
};

// DOM Elements
const elements = {
  intentInput: document.getElementById('intentInput'),
  generateBtn: document.getElementById('generateBtn'),
  canvas: document.getElementById('sigilCanvas'),
  ctx: document.getElementById('sigilCanvas')?.getContext('2d')
};

// ===== CORE GENERATION =====
async function generateSigil() {
  if (state.isGenerating || state.cooldownActive) return;

  const phrase = elements.intentInput?.value?.trim();
  if (!phrase) {
    showToast('Enter your intention', 'warning');
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
    showLoading();

    console.log(`🎨 Starting sigil generation...`);
    console.log(`📝 Generating: "${phrase}" with vibes: ${vibe}`);

    const result = await makeGenerationRequest(phrase, vibe);
    
    if (result?.success && result?.image) {
      state.lastGeneratedImage = result.image;
      await renderSigil(result.image);
      showResult();
      showToast('✨ Sigil manifested!', 'success');
      
      if (!state.isPro) startCooldown();
    } else {
      throw new Error(result?.error || 'Generation failed');
    }

  } catch (error) {
    console.error('Generation error:', error);
    showToast(error.message || 'Generation failed', 'error');
  } finally {
    state.isGenerating = false;
    updateUI();
    hideLoading();
  }
}

async function makeGenerationRequest(phrase, vibe) {
  const response = await fetch('/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phrase, vibe }),
    signal: AbortSignal.timeout(30000)
  });

  if (!response.ok) {
    const errorText = await response.text().catch(() => `HTTP ${response.status}`);
    throw new Error(`Server error: ${errorText}`);
  }

  return response.json();
}

// ===== UI MANAGEMENT =====
function updateUI() {
  updateGenerateButton();
  renderEnergies();
  updateProInterface();
}

function updateGenerateButton() {
  if (!elements.generateBtn) return;
  
  if (state.isGenerating) {
    elements.generateBtn.disabled = true;
    elements.generateBtn.innerHTML = '<span>Channeling Energies...</span>';
    elements.generateBtn.classList.add('generating');
  } else if (state.cooldownActive) {
    elements.generateBtn.disabled = true;
    elements.generateBtn.innerHTML = '<span>Recharging...</span>';
    elements.generateBtn.classList.remove('generating');
  } else {
    elements.generateBtn.disabled = false;
    elements.generateBtn.innerHTML = '<span>Generate Sigil</span>';
    elements.generateBtn.classList.remove('generating');
  }
}

function startCooldown() {
  if (state.isPro) return;
  
  state.cooldownActive = true;
  let remaining = COOLDOWN_TIME;

  const interval = setInterval(() => {
    remaining -= 1000;
    
    if (elements.generateBtn) {
      elements.generateBtn.innerHTML = `<span>Recharging... ${Math.ceil(remaining/1000)}s</span>`;
    }

    if (remaining <= 0) {
      clearInterval(interval);
      state.cooldownActive = false;
      updateUI();
    }
  }, 1000);
}

async function renderSigil(imageData) {
  return new Promise((resolve) => {
    if (!elements.canvas || !elements.ctx) {
      resolve();
      return;
    }

    const img = new Image();
    img.onload = () => {
      elements.ctx.clearRect(0, 0, elements.canvas.width, elements.canvas.height);
      
      const scale = Math.min(
        elements.canvas.width / img.width, 
        elements.canvas.height / img.height
      );
      const x = (elements.canvas.width - img.width * scale) / 2;
      const y = (elements.canvas.height - img.height * scale) / 2;
      
      elements.ctx.drawImage(img, x, y, img.width * scale, img.height * scale);
      resolve();
    };
    img.src = imageData;
  });
}

function showResult() {
  const canvasContainer = document.getElementById('canvasContainer');
  const downloadBtn = document.getElementById('downloadBtn');
  
  canvasContainer?.classList.remove('hidden');
  if (downloadBtn) downloadBtn.style.display = 'block';
}

// ===== ENERGY SELECTION =====
function renderEnergies() {
  const energyContainer = document.getElementById('energyContainer');
  if (!energyContainer) return;

  const availableEnergies = state.isPro ? ALL_ENERGIES : FREE_ENERGIES;
  
  energyContainer.innerHTML = availableEnergies.map(energy => `
    <div class="energy-option ${state.selectedEnergies.includes(energy) ? 'selected' : ''}" 
         data-energy="${energy}" onclick="toggleEnergy('${energy}')">
      <span class="energy-name">${energy}</span>
      ${!FREE_ENERGIES.includes(energy) && !state.isPro ? '<span class="pro-badge">PRO</span>' : ''}
    </div>
  `).join('');
}

function toggleEnergy(energy) {
  if (!FREE_ENERGIES.includes(energy) && !state.isPro) {
    showToast('Pro feature - upgrade required', 'warning');
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
function showLoading() {
  const loading = document.getElementById('loading');
  if (loading) loading.style.display = 'block';
}

function hideLoading() {
  const loading = document.getElementById('loading');
  if (loading) loading.style.display = 'none';
}

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

function downloadSigil() {
  if (!state.lastGeneratedImage) {
    showToast('Generate a sigil first', 'warning');
    return;
  }

  const link = document.createElement('a');
  link.download = `sigil-${Date.now()}.png`;
  link.href = state.lastGeneratedImage;
  link.click();
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

  document.getElementById('downloadBtn')?.addEventListener('click', downloadSigil);

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
}

// ===== INITIALIZATION =====
async function init() {
  console.log('🚀 Initializing Sigil Generator Pro...');
  
  setupEvents();
  await checkProStatus();
  updateUI();
  
  console.log('✅ App initialization complete!');
}

// Start
document.addEventListener('DOMContentLoaded', init);

// Global access
window.generateSigil = generateSigil;
window.toggleEnergy = toggleEnergy;
window.downloadSigil = downloadSigil;
