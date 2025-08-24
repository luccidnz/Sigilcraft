// ===== ENHANCED SIGILCRAFT APPLICATION =====
const FREE_ENERGIES = ["mystical","elemental","light"];
const ALL_ENERGIES  = ["mystical","cosmic","elemental","crystal","shadow","light"];
let selectedEnergies = [FREE_ENERGIES[0]];
let lastGenAt = 0;
let lastGeneratedImage = null;
let isAnimating = false;
let animationFrame = null;
let sigilHistory = [];
let meditationMode = false;
let journalEntries = [];

// Enhanced DOM Element References
const el = (id) => document.getElementById(id);
const genBtn = el("genBtn");
const cooldownEl = el("cooldown");
const energyList = el("energyList");
const proBadge = el("proBadge");
const proControls = el("proControls");
const canvas = el("sigilCanvas");
const ctx = canvas?.getContext("2d");
const intentInput = el("intentInput");
const charCounter = el("charCounter");
const loadingSpinner = el("loadingSpinner");

// ===== ENHANCED PRO STATUS MANAGEMENT =====
let proStatusCache = null;
let cacheExpiry = 0;

async function serverIsPro() {
  try {
    console.log("🔍 Checking server Pro status...");
    const r = await fetch("/api/is-pro", {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache'
      }
    });

    if (!r.ok) {
      console.error("❌ Server Pro check failed:", r.status, r.statusText);
      return false;
    }

    const contentType = r.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      console.error("❌ Server returned non-JSON response:", contentType);
      return false;
    }

    const j = await r.json();
    console.log("✅ Server Pro status:", j);
    return !!j.pro;
  } catch (error) {
    console.error("❌ Error checking pro status:", error);
    return false;
  }
}

function localIsPro() {
  const localStatus = localStorage.getItem("sigil_pro") === "1";
  console.log("🔍 Local Pro status:", localStatus);
  return localStatus;
}

async function isUserPro() {
  const now = Date.now();
  if (proStatusCache !== null && now < cacheExpiry) {
    return proStatusCache;
  }

  const serverPro = await serverIsPro();
  const localPro = localIsPro();
  const isPro = serverPro || localPro;

  proStatusCache = isPro;
  cacheExpiry = now + 30000;

  console.log("Pro status check:", isPro, "(server:", serverPro, "local:", localPro, ")");
  return isPro;
}

function clearProCache() {
  proStatusCache = null;
  cacheExpiry = 0;
}

// ===== ENHANCED TOAST SYSTEM =====
let toastTimer;
function toast(msg, type = 'info', duration = 4000) {
  const toastEl = document.getElementById('toast') || createToastElement();
  toastEl.textContent = msg;
  toastEl.className = `toast ${type} show`;

  // Enhanced sound effects
  playEnhancedNotificationSound(type);

  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toastEl.classList.remove('show');
  }, duration);
}

function createToastElement() {
  const toast = document.createElement('div');
  toast.id = 'toast';
  toast.className = 'toast';
  toast.style.cssText = `
    position: fixed;
    top: 2rem;
    right: 2rem;
    z-index: 10000;
    padding: 1rem 2rem;
    border-radius: 15px;
    font-family: 'Cinzel', serif;
    font-weight: 600;
    opacity: 0;
    transform: translateX(400px);
    transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  `;
  document.body.appendChild(toast);
  return toast;
}

function playEnhancedNotificationSound(type) {
  try {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    // Enhanced mystical frequencies
    switch(type) {
      case 'success':
        oscillator.frequency.setValueAtTime(528, audioContext.currentTime); // Love frequency
        oscillator.frequency.setValueAtTime(741, audioContext.currentTime + 0.1); // Awakening
        break;
      case 'error':
        oscillator.frequency.setValueAtTime(256, audioContext.currentTime);
        oscillator.frequency.setValueAtTime(128, audioContext.currentTime + 0.1);
        break;
      case 'warning':
        oscillator.frequency.setValueAtTime(396, audioContext.currentTime); // Liberation
        break;
      default:
        oscillator.frequency.setValueAtTime(432, audioContext.currentTime); // Sacred frequency
    }

    gainNode.gain.setValueAtTime(0, audioContext.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.05, audioContext.currentTime + 0.01);
    gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.3);

    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.3);
  } catch (e) {
    console.log('Audio not available');
  }
}

// ===== ENHANCED LOADING SYSTEM =====
function showLoading(text = "Channeling quantum energies...") {
  if (!loadingSpinner) return;

  const loadingText = loadingSpinner.querySelector('.loading-text');
  const progressBar = loadingSpinner.querySelector('.progress-bar');

  if (loadingText) loadingText.textContent = text;
  if (progressBar) {
    progressBar.style.animation = 'none';
    setTimeout(() => {
      progressBar.style.animation = 'progressFlow 4s ease-in-out infinite';
    }, 10);
  }

  loadingSpinner.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
  document.body.classList.add('loading-active');
}

function hideLoading() {
  if (!loadingSpinner) return;

  loadingSpinner.classList.add('hidden');
  document.body.style.overflow = '';
  document.body.classList.remove('loading-active');
}

// ===== ENHANCED ENERGY GRID =====
async function renderEnergies() {
  const isPro = await isUserPro();
  const allowed = isPro ? ALL_ENERGIES : FREE_ENERGIES;
  console.log("Rendering energies - Pro:", isPro, "Allowed:", allowed);

  if (!energyList) return;

  energyList.innerHTML = "";
  ALL_ENERGIES.forEach(name => {
    const div = document.createElement("div");
    const isLocked = !allowed.includes(name);
    div.className = "energy" + (isLocked ? " locked" : "");
    div.setAttribute('data-vibe', name);
    div.textContent = name;

    // Enhanced visual indicators
    if (!FREE_ENERGIES.includes(name)) {
      if (isPro) {
        div.title = "✨ Pro Energy - Unlocked";
        div.classList.add('pro-unlocked');
      } else {
        div.title = "🔒 Pro Energy - Upgrade to unlock";
        div.classList.add('pro-locked');
      }
    }

    div.onclick = async () => {
      const userIsPro = await isUserPro();
      const energyIsLocked = !userIsPro && !FREE_ENERGIES.includes(name);

      if (energyIsLocked) {
        toast(`⚡ ${name} energy requires Pro upgrade`, 'warning');
        return;
      }

      const comboMode = userIsPro && document.getElementById('comboToggle')?.checked;

      if (!comboMode) {
        selectedEnergies = [name];
      } else {
        if (selectedEnergies.includes(name)) {
          const newSelection = selectedEnergies.filter(e => e !== name);
          selectedEnergies = newSelection.length > 0 ? newSelection : [FREE_ENERGIES[0]];
        } else {
          if (selectedEnergies.length < 4) {
            selectedEnergies = [...selectedEnergies, name];
          } else {
            toast("⚠️ Maximum 4 energies can be combined", 'warning');
            return;
          }
        }
      }

      console.log("Selected energies:", selectedEnergies);
      highlightSelection();
      updateIntentStrength();
    };
    energyList.appendChild(div);
  });
  highlightSelection();
}

function highlightSelection() {
  if (!energyList) return;

  const children = [...energyList.children];
  children.forEach((div, index) => {
    const name = div.textContent.trim();
    const isSelected = selectedEnergies.includes(name);

    div.classList.remove('selected', 'combo-selected');
    const badge = div.querySelector('.combo-badge');
    if (badge) badge.remove();

    if (isSelected) {
      div.classList.add('selected');
      const selectionIndex = selectedEnergies.indexOf(name);

      if (selectedEnergies.length > 1) {
        div.classList.add('combo-selected');
        const badge = document.createElement('span');
        badge.className = 'combo-badge';
        badge.textContent = `${selectionIndex + 1}`;
        badge.style.cssText = `
          position: absolute;
          top: 12px;
          right: 12px;
          background: linear-gradient(45deg, var(--sacred-gold), var(--sacred-bronze));
          color: var(--cosmic-void);
          border-radius: 50%;
          width: 28px;
          height: 28px;
          font-size: 14px;
          font-weight: bold;
          font-family: 'Cinzel', serif;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 0 15px rgba(255, 215, 0, 0.8);
          animation: badgePulse 3s ease-in-out infinite;
        `;
        div.style.position = 'relative';
        div.appendChild(badge);
      }
    }
  });

  updateComboDisplay();
}

function updateComboDisplay() {
  const comboDisplay = document.getElementById('comboDisplay');
  if (comboDisplay) {
    comboDisplay.textContent = selectedEnergies.join(' + ');
    comboDisplay.style.color = selectedEnergies.length > 1 ? 'var(--sacred-tertiary)' : 'var(--sacred-secondary)';
  }
}

// ===== ENHANCED INTENT STRENGTH SYSTEM =====
function updateIntentStrength() {
  if (!intentInput) return;

  const phrase = intentInput.value.trim();
  const strengthContainer = document.querySelector('.intent-strength');

  if (!strengthContainer) return;

  // Calculate intent strength based on multiple factors
  let strength = 0;
  const wordCount = phrase.split(/\s+/).filter(w => w.length > 0).length;
  const uniqueWords = new Set(phrase.toLowerCase().split(/\s+/)).size;
  const emotionalWords = countEmotionalWords(phrase);
  const energyCount = selectedEnergies.length;

  // Strength calculation
  strength += Math.min(wordCount * 0.5, 3); // Max 3 from word count
  strength += Math.min(uniqueWords * 0.3, 2); // Max 2 from unique words
  strength += emotionalWords * 0.8; // Emotional words boost
  strength += (energyCount - 1) * 0.5; // Multi-energy bonus

  const maxStrength = 5;
  const normalizedStrength = Math.min(strength / maxStrength, 1);
  const strengthLevel = Math.ceil(normalizedStrength * 5);

  // Update strength bars
  const strengthBars = strengthContainer.querySelector('.strength-bars');
  if (strengthBars) {
    strengthBars.innerHTML = '';
    for (let i = 0; i < 5; i++) {
      const bar = document.createElement('div');
      bar.className = `bar ${i < strengthLevel ? 'active' : ''}`;
      strengthBars.appendChild(bar);
    }
  }

  // Update strength label
  const strengthLabel = strengthContainer.querySelector('.strength-label');
  if (strengthLabel) {
    const labels = ['Whisper', 'Gentle', 'Focused', 'Powerful', 'Divine'];
    strengthLabel.textContent = labels[strengthLevel - 1] || 'Whisper';
  }
}

function countEmotionalWords(text) {
  const emotionalWords = [
    'love', 'peace', 'power', 'strength', 'healing', 'money', 'success', 'joy',
    'happiness', 'protection', 'wisdom', 'clarity', 'abundance', 'prosperity',
    'freedom', 'wealth', 'health', 'beauty', 'truth', 'light', 'divine', 'sacred',
    'blessed', 'gratitude', 'manifestation', 'transformation', 'awakening', 'enlightenment'
  ];

  const words = text.toLowerCase().split(/\s+/);
  return words.filter(word => emotionalWords.includes(word)).length;
}

// ===== ENHANCED PRO UNLOCK SYSTEM =====
async function unlockProFeatures() {
  const keyInput = document.getElementById("proKeyInput2") || document.getElementById("proKeyInput");
  if (!keyInput) {
    toast("Key input not found", 'error');
    return;
  }

  const key = keyInput.value.trim();
  if (!key) {
    toast("Enter a Pro key", 'warning');
    return;
  }

  console.log("🔑 Starting Pro unlock...");

  try {
    const r = await fetch("/api/verify-pro", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cache-Control": "no-cache"
      },
      body: JSON.stringify({ key })
    });

    console.log("🔑 Unlock response status:", r.status);

    if (!r.ok) {
      console.error("❌ Pro unlock failed:", r.status, r.statusText);
      toast("❌ Server error during unlock", 'error');
      return;
    }

    const contentType = r.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      console.error("❌ Pro unlock returned non-JSON:", contentType);
      toast("❌ Server error - invalid response format", 'error');
      return;
    }

    const j = await r.json();
    console.log("🔑 Unlock response:", j);

    if (j.ok) {
      localStorage.setItem("sigil_pro","1");
      clearProCache();
      keyInput.value = '';

      // Enhanced success feedback
      toast("✨ Pro features unlocked! All energies available!", 'success', 6000);

      // Close modal if it exists
      const modal = document.getElementById('keyModal');
      if (modal && modal.close) {
        modal.close();
      }

      // Trigger celebration animation
      triggerUnlockCelebration();

      setTimeout(async () => {
        await renderEnergies();
        await updateProInterface();
      }, 500);
    } else {
      toast("❌ Invalid Pro key", 'error');
    }
  } catch (error) {
    console.error("❌ Error unlocking:", error);
    toast("❌ Network error during unlock. Please try again.", 'error');
  }
}

function triggerUnlockCelebration() {
  // Create celebration particles
  for (let i = 0; i < 20; i++) {
    setTimeout(() => {
      createCelebrationParticle();
    }, i * 100);
  }
}

function createCelebrationParticle() {
  const particle = document.createElement('div');
  particle.style.cssText = `
    position: fixed;
    width: 10px;
    height: 10px;
    background: linear-gradient(45deg, var(--sacred-gold), var(--sacred-primary));
    border-radius: 50%;
    pointer-events: none;
    z-index: 10000;
    animation: celebrationFloat 3s ease-out forwards;
  `;

  particle.style.left = Math.random() * 100 + 'vw';
  particle.style.top = '100vh';

  document.body.appendChild(particle);

  setTimeout(() => {
    particle.remove();
  }, 3000);
}

// Add celebration animation
const celebrationStyle = document.createElement('style');
celebrationStyle.textContent = `
  @keyframes celebrationFloat {
    0% { transform: translateY(0) rotate(0deg); opacity: 1; }
    100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
  }
`;
document.head.appendChild(celebrationStyle);

// ===== ENHANCED SIGIL GENERATION =====
async function generateSigil() {
  if (!intentInput) {
    toast("❌ Intent input not found", 'error');
    return;
  }

  const phrase = intentInput.value.trim();
  if (!phrase) {
    toast("⚠️ Please enter your sacred intent first", 'warning');
    intentInput.focus();
    return;
  }

  if (phrase.length < 2) {
    toast("⚠️ Intent must be at least 2 characters", 'warning');
    return;
  }

  if (phrase.length > 200) {
    toast("⚠️ Intent too long (maximum 200 characters)", 'warning');
    return;
  }

  console.log("🎨 Starting enhanced sigil generation...");
  console.log(`📝 Generating: "${phrase}" with energies: ${selectedEnergies.join(' + ')}`);

  const isPro = await isUserPro();
  const vibe = selectedEnergies.join('+');

  // Enhanced cooldown check for free users
  if (!isPro) {
    const now = Date.now();
    const timeSinceLastGen = now - lastGenAt;
    const cooldownPeriod = 10000;

    if (timeSinceLastGen < cooldownPeriod) {
      const remaining = Math.ceil((cooldownPeriod - timeSinceLastGen) / 1000);
      toast(`⏳ Sacred energies recharging... ${remaining} more seconds`, 'warning');
      return;
    }
  }

  try {
    // Enhanced generation feedback
    if (genBtn) {
      genBtn.disabled = true;
      genBtn.innerHTML = `
        <div class="btn-sacred-mandala">
          <i class="fas fa-eye">👁️</i>
        </div>
        <span class="generate-text">Channeling Energies...</span>
      `;
    }

    // Enhanced loading messages
    const loadingMessages = [
      "Aligning quantum frequencies...",
      "Weaving sacred geometry...",
      "Channeling cosmic energies...",
      "Manifesting divine intention...",
      "Crystallizing mystical patterns..."
    ];

    let messageIndex = 0;
    showLoading(loadingMessages[0]);

    const messageInterval = setInterval(() => {
      messageIndex = (messageIndex + 1) % loadingMessages.length;
      const loadingText = document.querySelector('.loading-text');
      if (loadingText) {
        loadingText.textContent = loadingMessages[messageIndex];
      }
    }, 1500);

    // Generate the sigil with enhanced error handling
    const result = await generateSigilRequest(phrase, vibe);
    clearInterval(messageInterval);

    if (result && result.success) {
      // Add to history
      addToSigilHistory({
        phrase,
        vibe,
        image: result.image,
        timestamp: Date.now(),
        id: Date.now().toString()
      });

      toast("✨ Sacred sigil manifested successfully!", 'success');

      if (!isPro) {
        startCooldownIfNeeded();
      }

      // Update intent strength display
      updateIntentStrength();
    }

  } catch (error) {
    console.error("❌ Generation failed:", error);
    toast(`❌ ${error.message || 'Generation failed. Please try again.'}`, 'error');
  } finally {
    // Reset generate button
    if (genBtn) {
      genBtn.disabled = false;
      genBtn.innerHTML = `
        <div class="btn-sacred-mandala">
          <i class="fas fa-eye">👁️</i>
        </div>
        <span class="generate-text">Manifest Sacred Sigil</span>
      `;
    }

    hideLoading();
  }
}

// Enhanced sigil request with better error handling
async function generateSigilRequest(phrase, vibe, retryCount = 0) {
  const maxRetries = 2;
  const retryDelay = 1000 * Math.min(retryCount + 1, 3);

  try {
    console.log(`🎨 Sending enhanced sigil request (attempt ${retryCount + 1}):`, { phrase, vibe });

    const controller = new AbortController();
    const timeoutDuration = vibe.includes('+') ? 25000 : 20000;
    const timeoutId = setTimeout(() => controller.abort(), timeoutDuration);

    const response = await fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cache-Control": "no-cache"
      },
      body: JSON.stringify({
        phrase: phrase.trim(),
        vibe,
        enhanced: true,
        timestamp: Date.now()
      }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response) {
      throw new Error("No response received from server");
    }

    if (!response.ok) {
      const errorText = await response.text().catch(() => `HTTP ${response.status}`);
      throw new Error(`Server error: ${errorText}`);
    }

    const data = await response.json();

    if (!data.success) {
      const errorMsg = data.error || "Generation failed";
      if (errorMsg.includes("timeout") && retryCount < maxRetries) {
        console.log(`⏱️ Timeout, retrying... (${retryCount + 1}/${maxRetries})`);
        await new Promise(resolve => setTimeout(resolve, retryDelay));
        return generateSigilRequest(phrase, vibe, retryCount + 1);
      }
      throw new Error(errorMsg);
    }

    if (!data.image) {
      throw new Error("No image data received");
    }

    lastGeneratedImage = data.image;
    await renderSigil(data.image);
    showResult(data.image);

    console.log("✅ Enhanced sigil generation completed successfully");
    return data;

  } catch (error) {
    if (error.name === 'AbortError' && retryCount < maxRetries) {
      console.log(`⏱️ Request timed out, retrying... (${retryCount + 1}/${maxRetries})`);
      await new Promise(resolve => setTimeout(resolve, retryDelay));
      return generateSigilRequest(phrase, vibe, retryCount + 1);
    }
    throw error;
  }
}

// ===== SIGIL HISTORY MANAGEMENT =====
function addToSigilHistory(sigil) {
  sigilHistory.unshift(sigil);
  if (sigilHistory.length > 50) {
    sigilHistory = sigilHistory.slice(0, 50);
  }
  localStorage.setItem('sigil_history', JSON.stringify(sigilHistory));
}

function loadSigilHistory() {
  try {
    const saved = localStorage.getItem('sigil_history');
    sigilHistory = saved ? JSON.parse(saved) : [];
  } catch (e) {
    console.error('Error loading sigil history:', e);
    sigilHistory = [];
  }
}

// ===== ENHANCED CANVAS RENDERING =====
async function renderSigil(imageSrc, isSvg = false) {
  return new Promise((resolve, reject) => {
    try {
      if (!canvas || !ctx) {
        reject(new Error("Canvas not available"));
        return;
      }

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      if (!imageSrc || typeof imageSrc !== 'string') {
        reject(new Error("Invalid image source"));
        return;
      }

      if (!imageSrc.startsWith('data:image/')) {
        reject(new Error("Invalid image data format"));
        return;
      }

      const img = new Image();

      img.onload = async () => {
        try {
          if (img.width === 0 || img.height === 0) {
            reject(new Error("Invalid image dimensions"));
            return;
          }

          // Enhanced rendering with better quality
          ctx.imageSmoothingEnabled = true;
          ctx.imageSmoothingQuality = 'high';
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          // Add subtle background gradient
          const gradient = ctx.createRadialGradient(
            canvas.width/2, canvas.height/2, 0,
            canvas.width/2, canvas.height/2, canvas.width/2
          );
          gradient.addColorStop(0, 'rgba(139, 92, 246, 0.05)');
          gradient.addColorStop(1, 'rgba(0, 0, 0, 0.95)');
          ctx.fillStyle = gradient;
          ctx.fillRect(0, 0, canvas.width, canvas.height);

          // Draw the sigil
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

          // Add enhancement overlay
          await addEnhancementOverlay();

          console.log("Enhanced sigil rendered to canvas successfully");
          resolve();
        } catch (renderError) {
          reject(new Error(`Failed to render image: ${renderError.message}`));
        }
      };

      img.onerror = () => {
        reject(new Error("Failed to load generated image"));
      };

      const imageTimeout = setTimeout(() => {
        reject(new Error("Image loading timed out"));
      }, 10000);

      img.onload = (originalOnload => async function(...args) {
        clearTimeout(imageTimeout);
        return originalOnload.apply(this, args);
      })(img.onload);

      img.src = imageSrc;

    } catch (error) {
      reject(error);
    }
  });
}

async function addEnhancementOverlay() {
  if (!ctx || !canvas) return;

  const isPro = await isUserPro();

  // Add sacred geometry overlay for pro users
  if (isPro) {
    ctx.globalAlpha = 0.1;
    ctx.strokeStyle = '#9b59b6';
    ctx.lineWidth = 2;

    // Draw sacred geometry pattern
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(canvas.width, canvas.height) / 4;

    // Draw flower of life pattern
    for (let i = 0; i < 6; i++) {
      const angle = (i * Math.PI * 2) / 6;
      const x = centerX + Math.cos(angle) * radius / 2;
      const y = centerY + Math.sin(angle) * radius / 2;

      ctx.beginPath();
      ctx.arc(x, y, radius / 3, 0, Math.PI * 2);
      ctx.stroke();
    }

    ctx.globalAlpha = 1;
  } else {
    // Add watermark for free users
    ctx.globalAlpha = 0.4;
    ctx.fillStyle = "#ffffff";
    ctx.font = `${Math.max(16, Math.floor(canvas.width * 0.03))}px Cinzel, serif`;
    const text = "🔮 Sigilcraft";
    const metrics = ctx.measureText(text);
    ctx.fillText(text, canvas.width - metrics.width - 20, canvas.height - 20);
    ctx.globalAlpha = 1;
  }
}

// ===== MODERN FEATURE: MEDITATION MODE =====
function toggleMeditationMode() {
  meditationMode = !meditationMode;

  if (meditationMode) {
    document.body.classList.add('meditation-mode');
    toast("🧘‍♀️ Meditation mode activated", 'success');

    // Dim the interface
    const overlay = document.createElement('div');
    overlay.id = 'meditation-overlay';
    overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.7);
      z-index: 50;
      pointer-events: none;
      transition: opacity 1s ease;
    `;
    document.body.appendChild(overlay);

    // Start ambient meditation sounds
    startMeditationAmbient();
  } else {
    document.body.classList.remove('meditation-mode');
    const overlay = document.getElementById('meditation-overlay');
    if (overlay) overlay.remove();
    stopMeditationAmbient();
    toast("Meditation mode deactivated", 'info');
  }
}

let meditationAudio = null;

function startMeditationAmbient() {
  try {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    // 528 Hz - Love frequency
    oscillator.frequency.setValueAtTime(528, audioContext.currentTime);
    oscillator.type = 'sine';

    gainNode.gain.setValueAtTime(0, audioContext.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.02, audioContext.currentTime + 2);

    oscillator.start(audioContext.currentTime);

    meditationAudio = { oscillator, gainNode, audioContext };
  } catch (e) {
    console.log('Meditation audio not available');
  }
}

function stopMeditationAmbient() {
  if (meditationAudio) {
    try {
      meditationAudio.gainNode.gain.linearRampToValueAtTime(0, meditationAudio.audioContext.currentTime + 1);
      setTimeout(() => {
        meditationAudio.oscillator.stop();
        meditationAudio = null;
      }, 1000);
    } catch (e) {
      console.log('Error stopping meditation audio');
    }
  }
}

// ===== MODERN FEATURE: SIGIL JOURNAL =====
function saveSigilToJournal() {
  if (!lastGeneratedImage || !intentInput) {
    toast('⚠️ No sigil to save', 'warning');
    return;
  }

  const phrase = intentInput.value.trim();
  const vibe = selectedEnergies.join('+');

  const entry = {
    id: Date.now().toString(),
    phrase,
    vibe,
    image: lastGeneratedImage,
    timestamp: Date.now(),
    notes: '',
    manifestationStatus: 'active'
  };

  journalEntries.unshift(entry);
  localStorage.setItem('sigil_journal', JSON.stringify(journalEntries.slice(0, 100)));

  toast('📖 Sigil saved to sacred journal', 'success');
}

function loadSigilJournal() {
  try {
    const saved = localStorage.getItem('sigil_journal');
    journalEntries = saved ? JSON.parse(saved) : [];
  } catch (e) {
    console.error('Error loading sigil journal:', e);
    journalEntries = [];
  }
}

// ===== MODERN FEATURE: ENHANCED SHARING =====
async function shareToSocialMedia(platform) {
  if (!lastGeneratedImage) {
    toast('⚠️ Generate a sigil first to share', 'warning');
    return;
  }

  const phrase = intentInput?.value?.trim() || 'Sacred Sigil';
  const vibe = selectedEnergies.join(' + ');

  const shareTexts = {
    twitter: `🔮 I just manifested a ${vibe} sigil for "${phrase}" using Sigilcraft! ✨ #sigilcraft #manifestation #sacredgeometry`,
    facebook: `✨ Just created a beautiful ${vibe} sigil for my intention: "${phrase}" using Sigilcraft! 🔮`,
    instagram: `🔮✨ Manifesting with sacred geometry and quantum energy! Created this ${vibe} sigil for "${phrase}" #sigilcraft #manifestation #sacredart`,
    pinterest: `Sacred ${vibe} Sigil for "${phrase}" - Created with Sigilcraft ✨🔮`
  };

  const urls = {
    twitter: `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareTexts.twitter)}&url=${encodeURIComponent(window.location.origin)}`,
    facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.origin)}&quote=${encodeURIComponent(shareTexts.facebook)}`,
    instagram: `https://www.instagram.com/`,
    pinterest: `https://pinterest.com/pin/create/button/?url=${encodeURIComponent(window.location.origin)}&description=${encodeURIComponent(shareTexts.pinterest)}`
  };

  if (urls[platform]) {
    window.open(urls[platform], '_blank', 'width=600,height=400');
    toast(`Sharing to ${platform}...`, 'success');
  }
}

// ===== ENHANCED DOWNLOAD SYSTEM =====
async function downloadSigil(format = 'png') {
  if (!lastGeneratedImage || !canvas) {
    toast('⚠️ Generate a sigil first to download', 'warning');
    return;
  }

  try {
    const isPro = await isUserPro();
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
    const phrase = intentInput?.value?.trim() || 'sigil';
    const vibe = selectedEnergies.join('_');
    const filename = `${phrase.replace(/[^a-zA-Z0-9]/g, '_')}_${vibe}_${timestamp}`;

    if (format === 'svg' && isPro) {
      // Generate SVG version for Pro users
      const svgData = generateSVGVersion();
      const blob = new Blob([svgData], { type: 'image/svg+xml' });
      downloadFile(blob, `${filename}.svg`);
      toast('✨ SVG sigil downloaded!', 'success');
    } else {
      // PNG download
      canvas.toBlob((blob) => {
        if (!blob) {
          toast('❌ Download failed - please regenerate', 'error');
          return;
        }
        downloadFile(blob, `${filename}.png`);
        toast('✨ Sacred sigil downloaded!', 'success');
      }, 'image/png', 1.0);
    }
  } catch (error) {
    console.error('Download error:', error);
    toast(`❌ Download failed: ${error.message}`, 'error');
  }
}

function downloadFile(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.style.display = 'none';

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function generateSVGVersion() {
  // Enhanced SVG generation based on current sigil
  const phrase = intentInput?.value?.trim() || 'sigil';
  const vibe = selectedEnergies[0] || 'mystical';

  return `<svg width="512" height="512" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="bg" cx="50%" cy="50%">
        <stop offset="0%" stop-color="rgba(139,92,246,0.1)"/>
        <stop offset="100%" stop-color="rgba(0,0,0,0.95)"/>
      </radialGradient>
    </defs>
    <rect width="512" height="512" fill="url(#bg)"/>
    <!-- Enhanced SVG sigil content would go here -->
    <text x="256" y="30" text-anchor="middle" fill="#9b59b6" font-family="Cinzel" font-size="16">${phrase}</text>
  </svg>`;
}

// ===== ENHANCED INITIALIZATION =====
async function initializeApp() {
  console.log('🚀 Initializing Enhanced Sigilcraft...');

  try {
    // Load saved data
    loadSigilHistory();
    loadSigilJournal();

    // Setup event listeners
    setupEventListeners();

    // Initialize Pro status and UI
    await updateProInterface();
    await renderEnergies();

    // Setup character counter
    if (intentInput && charCounter) {
      intentInput.addEventListener('input', () => {
        const length = intentInput.value.length;
        charCounter.textContent = `${length}/200`;
        charCounter.style.color = length > 180 ? '#ff6b9d' : '#64748b';
        updateIntentStrength();
      });
    }

    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      // Ctrl/Cmd + Enter to generate
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        generateSigil();
      }
      // Escape to close modals
      if (e.key === 'Escape') {
        closeAllModals();
      }
    });

    // Initialize moon phase display
    updateMoonPhase();

    // Check for URL parameters
    const params = new URLSearchParams(window.location.search);
    if (params.get("purchase") === "success") {
      toast("🎉 Payment successful! Check your email for your Pro key.", 'success', 6000);
    } else if (params.get("purchase") === "cancel") {
      toast("Purchase cancelled.", 'warning');
    }

    // Enhanced welcome message
    setTimeout(() => {
      toast("✨ Enhanced Sigilcraft loaded! Sacred energies aligned.", 'success', 4000);
    }, 1000);

    console.log('✅ Enhanced app initialization complete!');

  } catch (error) {
    console.error('Initialization error:', error);
    toast('⚠️ App initialization error. Please refresh the page.', 'error');
  }
}

// ===== UTILITY FUNCTIONS =====
function setupEventListeners() {
  // Generation button
  if (genBtn) {
    genBtn.addEventListener('click', generateSigil);
  }

  // Download button
  const downloadBtn = document.getElementById('downloadBtn');
  if (downloadBtn) {
    downloadBtn.addEventListener('click', () => downloadSigil('png'));
  }

  // Pro unlock buttons
  const unlockBtn = document.getElementById('unlockBtn');
  if (unlockBtn) {
    unlockBtn.addEventListener('click', unlockProFeatures);
  }

  const enterKeyBtn = document.getElementById('enterKeyBtn');
  if (enterKeyBtn) {
    enterKeyBtn.addEventListener('click', () => {
      const modal = document.getElementById('keyModal');
      if (modal && modal.showModal) {
        modal.showModal();
      }
    });
  }
}

async function updateProInterface() {
  const isPro = await isUserPro();

  // Update pro badge visibility
  if (proBadge) {
    if (isPro) {
      proBadge.classList.remove("hidden");
      proBadge.style.display = 'flex';
    } else {
      proBadge.classList.add("hidden");
      proBadge.style.display = 'none';
    }
  }

  // Update pro controls visibility
  if (proControls) {
    if (isPro) {
      proControls.classList.remove("hidden");
    } else {
      proControls.classList.add("hidden");
    }
  }

  // Update canvas size
  if (canvas) {
    if (isPro) {
      canvas.width = 2048;
      canvas.height = 2048;
    } else {
      canvas.width = 1200;
      canvas.height = 1200;
    }
  }

  // Update pro buttons
  await updateProButtons();
}

async function updateProButtons() {
  const isPro = await isUserPro();
  const proButtons = document.getElementById("proButtons");
  const proUnlock = document.getElementById("proUnlock");

  if (isPro) {
    if (proButtons) proButtons.style.display = 'none';
    if (proUnlock) proUnlock.style.display = 'none';
  } else {
    if (proButtons) proButtons.style.display = 'flex';
    if (proUnlock) proUnlock.style.display = 'block';
  }
}

function startCooldownIfNeeded() {
  const now = Date.now();
  lastGenAt = now;
  const wait = 10000;

  if (genBtn) genBtn.disabled = true;
  if (cooldownEl) cooldownEl.classList.remove("hidden");

  let left = wait;
  const iv = setInterval(() => {
    left -= 1000;
    if (cooldownEl) {
      cooldownEl.textContent = `Sacred energies recharging... ${Math.ceil(left/1000)}s`;
    }
    if (left <= 0) {
      clearInterval(iv);
      if (genBtn) genBtn.disabled = false;
      if (cooldownEl) cooldownEl.classList.add("hidden");
    }
  }, 1000);
}

function showResult(imageData) {
  const canvas = document.getElementById('sigilCanvas');
  const canvasPlaceholder = document.getElementById('canvasPlaceholder');
  const downloadBtn = document.getElementById('downloadBtn');

  if (canvasPlaceholder) {
    canvasPlaceholder.classList.add('hidden');
  }

  if (canvas) {
    canvas.style.display = 'block';
  }

  if (downloadBtn) {
    downloadBtn.style.display = 'inline-flex';
  }
}

function updateMoonPhase() {
  const moonPhaseEl = document.getElementById('moonPhase');
  if (!moonPhaseEl) return;

  // Calculate current moon phase
  const now = new Date();
  const newMoon = new Date('2024-01-01'); // Reference new moon
  const daysSinceNew = (now - newMoon) / (1000 * 60 * 60 * 24);
  const phase = (daysSinceNew % 29.53) / 29.53; // Lunar cycle is ~29.53 days

  const phases = [
    { name: 'New Moon', icon: '🌑', power: 'new beginnings' },
    { name: 'Waxing Crescent', icon: '🌒', power: 'growth intention' },
    { name: 'First Quarter', icon: '🌓', power: 'decision making' },
    { name: 'Waxing Gibbous', icon: '🌔', power: 'refinement' },
    { name: 'Full Moon', icon: '🌕', power: 'manifestation' },
    { name: 'Waning Gibbous', icon: '🌖', power: 'gratitude' },
    { name: 'Last Quarter', icon: '🌗', power: 'release' },
    { name: 'Waning Crescent', icon: '🌘', power: 'reflection' }
  ];

  const phaseIndex = Math.floor(phase * 8);
  const currentPhase = phases[phaseIndex];

  moonPhaseEl.innerHTML = `
    <span class="moon-icon">${currentPhase.icon}</span>
    <span class="moon-text">${currentPhase.name}</span>
    <span class="moon-power">• ${currentPhase.power}</span>
  `;
}

function closeAllModals() {
  const modals = document.querySelectorAll('dialog[open], .modal.show');
  modals.forEach(modal => {
    if (modal.close) {
      modal.close();
    } else {
      modal.classList.remove('show');
    }
  });
}

// Make functions globally available
window.generateSigil = generateSigil;
window.unlockProFeatures = unlockProFeatures;
window.toggleMeditationMode = toggleMeditationMode;
window.saveSigilToJournal = saveSigilToJournal;
window.shareToSocialMedia = shareToSocialMedia;
window.downloadSigil = downloadSigil;

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeApp);
} else {
  initializeApp();
}