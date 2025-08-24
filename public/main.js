
// ===== MODERN SIGILCRAFT APPLICATION =====
const FREE_ENERGIES = ["mystical", "elemental", "light"];
const ALL_ENERGIES = ["mystical", "cosmic", "elemental", "crystal", "shadow", "light"];

// Application State
let selectedEnergies = [FREE_ENERGIES[0]];
let lastGeneratedImage = null;
let isGenerating = false;
let cooldownActive = false;
let isPro = false;

// DOM Elements
const intentInput = document.getElementById('intentInput');
const generateBtn = document.getElementById('generateBtn');
const canvas = document.getElementById('sigilCanvas');
const ctx = canvas?.getContext('2d');

// ===== CORE GENERATION FUNCTION =====
async function generateSigil() {
  if (isGenerating || cooldownActive) return;

  const phrase = intentInput?.value?.trim();
  if (!phrase) {
    showToast('Please enter your intention', 'warning');
    return;
  }

  if (phrase.length < 2) {
    showToast('Intention too short (minimum 2 characters)', 'warning');
    return;
  }

  if (phrase.length > 200) {
    showToast('Intention too long (maximum 200 characters)', 'warning');
    return;
  }

  const vibe = selectedEnergies.join('+');
  
  try {
    isGenerating = true;
    updateGenerateButton(true);
    showLoading();

    console.log(`🎨 Generating sigil for: "${phrase}" with vibe: ${vibe}`);

    const result = await generateSigilRequest(phrase, vibe);
    
    if (result?.success && result?.image) {
      lastGeneratedImage = result.image;
      await renderSigil(result.image);
      showResult();
      showToast('✨ Sigil manifested successfully!', 'success');
      
      if (!isPro) {
        startCooldown();
      }
    } else {
      throw new Error(result?.error || 'Generation failed');
    }

  } catch (error) {
    console.error('Generation error:', error);
    showToast(error.message || 'Generation failed. Please try again.', 'error');
  } finally {
    isGenerating = false;
    updateGenerateButton(false);
    hideLoading();
  }
}

async function generateSigilRequest(phrase, vibe, retryCount = 0) {
  const maxRetries = 2;
  const timeout = 45000;

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phrase, vibe }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text().catch(() => `HTTP ${response.status}`);
      throw new Error(`Server error: ${errorText}`);
    }

    const data = await response.json();
    
    if (!data.success) {
      const errorMsg = data.error || "Generation failed";
      if (errorMsg.includes("timeout") && retryCount < maxRetries) {
        console.log(`⏱️ Timeout, retrying... (${retryCount + 1}/${maxRetries})`);
        await new Promise(resolve => setTimeout(resolve, 2000));
        return generateSigilRequest(phrase, vibe, retryCount + 1);
      }
      throw new Error(errorMsg);
    }

    return data;

  } catch (error) {
    if (error.name === 'AbortError' && retryCount < maxRetries) {
      console.log(`⏱️ Request timed out, retrying... (${retryCount + 1}/${maxRetries})`);
      await new Promise(resolve => setTimeout(resolve, 2000));
      return generateSigilRequest(phrase, vibe, retryCount + 1);
    }
    throw error;
  }
}

// ===== UI MANAGEMENT =====
function updateGenerateButton(generating) {
  if (!generateBtn) return;
  
  if (generating) {
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<span>Channeling Energies...</span>';
    generateBtn.classList.add('generating');
  } else {
    generateBtn.disabled = cooldownActive;
    generateBtn.innerHTML = cooldownActive ? 
      '<span>Recharging...</span>' : 
      '<span>Generate Sigil</span>';
    generateBtn.classList.toggle('generating', false);
  }
}

function startCooldown() {
  if (isPro) return;
  
  cooldownActive = true;
  const cooldownTime = 10000; // 10 seconds
  let remaining = cooldownTime;

  updateGenerateButton(false);

  const interval = setInterval(() => {
    remaining -= 1000;
    
    if (generateBtn) {
      generateBtn.innerHTML = `<span>Recharging... ${Math.ceil(remaining/1000)}s</span>`;
    }

    if (remaining <= 0) {
      clearInterval(interval);
      cooldownActive = false;
      updateGenerateButton(false);
    }
  }, 1000);
}

async function renderSigil(imageData) {
  return new Promise((resolve) => {
    if (!canvas || !ctx) {
      resolve();
      return;
    }

    const img = new Image();
    img.onload = () => {
      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Draw image centered
      const scale = Math.min(canvas.width / img.width, canvas.height / img.height);
      const x = (canvas.width - img.width * scale) / 2;
      const y = (canvas.height - img.height * scale) / 2;
      
      ctx.drawImage(img, x, y, img.width * scale, img.height * scale);
      resolve();
    };
    img.src = imageData;
  });
}

function showResult() {
  const canvasContainer = document.getElementById('canvasContainer');
  const downloadBtn = document.getElementById('downloadBtn');
  
  if (canvasContainer) {
    canvasContainer.classList.remove('hidden');
  }
  
  if (downloadBtn) {
    downloadBtn.style.display = 'block';
  }
}

// ===== ENERGY/VIBE SELECTION =====
function renderEnergies() {
  const energyContainer = document.getElementById('energyContainer');
  if (!energyContainer) return;

  const availableEnergies = isPro ? ALL_ENERGIES : FREE_ENERGIES;
  
  energyContainer.innerHTML = availableEnergies.map(energy => `
    <div class="energy-option ${selectedEnergies.includes(energy) ? 'selected' : ''}" 
         data-energy="${energy}" onclick="toggleEnergy('${energy}')">
      <span class="energy-name">${energy}</span>
      ${!FREE_ENERGIES.includes(energy) && !isPro ? '<span class="pro-badge">PRO</span>' : ''}
    </div>
  `).join('');
}

function toggleEnergy(energy) {
  if (!FREE_ENERGIES.includes(energy) && !isPro) {
    showToast('This energy requires Pro upgrade', 'warning');
    return;
  }

  if (selectedEnergies.includes(energy)) {
    if (selectedEnergies.length > 1) {
      selectedEnergies = selectedEnergies.filter(e => e !== energy);
    }
  } else {
    if (!isPro && selectedEnergies.length >= 1) {
      selectedEnergies = [energy];
    } else if (selectedEnergies.length < 4) {
      selectedEnergies.push(energy);
    }
  }
  
  renderEnergies();
}

// ===== PRO FEATURES =====
async function checkProStatus() {
  try {
    const localPro = localStorage.getItem('sigil_pro') === '1';
    let serverPro = false;

    try {
      const proKey = localStorage.getItem('sigil_pro_key');
      const response = await fetch('/api/pro-status', {
        headers: proKey ? { 'x-pro-key': proKey } : {}
      });
      
      if (response.ok) {
        const data = await response.json();
        serverPro = data.isPro || false;
      }
    } catch (error) {
      console.error('Error checking server pro status:', error);
    }

    isPro = localPro || serverPro;
    updateProInterface();
    renderEnergies();

  } catch (error) {
    console.error('Error checking pro status:', error);
    isPro = localStorage.getItem('sigil_pro') === '1';
    updateProInterface();
    renderEnergies();
  }
}

function updateProInterface() {
  const proBadge = document.getElementById('proBadge');
  const proControls = document.getElementById('proControls');
  const unlockSection = document.getElementById('unlockSection');

  if (proBadge) {
    proBadge.style.display = isPro ? 'flex' : 'none';
  }
  
  if (proControls) {
    proControls.style.display = isPro ? 'block' : 'none';
  }
  
  if (unlockSection) {
    unlockSection.style.display = isPro ? 'none' : 'block';
  }
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
      isPro = true;
      updateProInterface();
      renderEnergies();
      showToast('✨ Pro features unlocked!', 'success');
      return true;
    } else {
      showToast('Invalid pro key', 'error');
      return false;
    }
  } catch (error) {
    console.error('Pro key validation error:', error);
    showToast('Validation failed. Please try again.', 'error');
    return false;
  }
}

// ===== UTILITY FUNCTIONS =====
function showLoading() {
  const loadingDiv = document.getElementById('loading');
  if (loadingDiv) {
    loadingDiv.style.display = 'block';
  }
}

function hideLoading() {
  const loadingDiv = document.getElementById('loading');
  if (loadingDiv) {
    loadingDiv.style.display = 'none';
  }
}

function showToast(message, type = 'info') {
  // Create toast element
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  
  // Add to page
  document.body.appendChild(toast);
  
  // Show toast
  setTimeout(() => toast.classList.add('show'), 100);
  
  // Remove after 3 seconds
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => document.body.removeChild(toast), 300);
  }, 3000);
}

function downloadSigil() {
  if (!lastGeneratedImage) {
    showToast('Generate a sigil first', 'warning');
    return;
  }

  const link = document.createElement('a');
  link.download = `sigil-${Date.now()}.png`;
  link.href = lastGeneratedImage;
  link.click();
}

// ===== EVENT LISTENERS =====
function setupEventListeners() {
  // Generate button
  if (generateBtn) {
    generateBtn.addEventListener('click', generateSigil);
  }

  // Enter key in input
  if (intentInput) {
    intentInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        generateSigil();
      }
    });
  }

  // Download button
  const downloadBtn = document.getElementById('downloadBtn');
  if (downloadBtn) {
    downloadBtn.addEventListener('click', downloadSigil);
  }

  // Pro key modal
  const proKeyBtn = document.getElementById('proKeyBtn');
  const proKeyModal = document.getElementById('proKeyModal');
  const proKeySubmit = document.getElementById('proKeySubmit');
  const proKeyInput = document.getElementById('proKeyInput');

  if (proKeyBtn && proKeyModal) {
    proKeyBtn.addEventListener('click', () => {
      proKeyModal.showModal();
    });
  }

  if (proKeySubmit && proKeyInput) {
    proKeySubmit.addEventListener('click', async () => {
      const key = proKeyInput.value.trim();
      if (key) {
        const valid = await validateProKey(key);
        if (valid) {
          proKeyModal.close();
          proKeyInput.value = '';
        }
      }
    });
  }
}

// ===== INITIALIZATION =====
async function initializeApp() {
  console.log('🚀 Initializing Sigil Generator Pro...');

  try {
    // Setup event listeners
    setupEventListeners();

    // Check pro status
    await checkProStatus();

    // Render initial UI
    renderEnergies();

    console.log('✅ App initialization complete!');

  } catch (error) {
    console.error('Initialization error:', error);
    showToast('⚠️ App initialization error. Please refresh the page.', 'error');
  }
}

// Start the application
document.addEventListener('DOMContentLoaded', initializeApp);

// Global function access
window.generateSigil = generateSigil;
window.toggleEnergy = toggleEnergy;
window.downloadSigil = downloadSigil;
