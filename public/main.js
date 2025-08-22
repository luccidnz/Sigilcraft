// ---- simple state ----
const FREE_ENERGIES = ["mystical","elemental","light"];
const ALL_ENERGIES  = ["mystical","cosmic","elemental","crystal","shadow","light"];
let selectedEnergies = [FREE_ENERGIES[0]];
let lastGenAt = 0;
let lastGeneratedImage = null;

const el = (id) => document.getElementById(id);
const genBtn = el("genBtn");
const cooldownEl = el("cooldown");
const energyList = el("energyList");
const proBadge = el("proBadge");
const proControls = el("proControls");
const comboToggle = el("comboToggle");
const seedInput = el("seedInput");
const batchToggle = el("batchToggle");
const exportType = el("exportType");
const keyModal = el("keyModal");
const proKeyInput = el("proKeyInput");
const unlockBtn = el("unlockBtn");
const enterKeyBtn = el("enterKeyBtn");
const downloadBtn = el("downloadBtn");
const toastEl = el("toast");
const canvas = el("sigilCanvas");
const ctx = canvas.getContext("2d");
const previewSvg = el("previewSvg");

// --- pro detection with caching ---
let proStatusCache = null;
let cacheExpiry = 0;

async function serverIsPro() {
  try {
    const r = await fetch("/api/is-pro");
    const j = await r.json();
    return !!j.pro;
  } catch { return false; }
}

function localIsPro() {
  return localStorage.getItem("sigil_pro") === "1";
}

async function isUserPro() {
  const now = Date.now();

  // Use cache if valid (30 second cache)
  if (proStatusCache !== null && now < cacheExpiry) {
    return proStatusCache;
  }

  // Check both server and local
  const serverPro = await serverIsPro();
  const localPro = localIsPro();
  const isPro = serverPro || localPro;

  // Cache the result
  proStatusCache = isPro;
  cacheExpiry = now + 30000; // 30 seconds

  console.log("Pro status check:", isPro, "(server:", serverPro, "local:", localPro, ")");
  return isPro;
}

// Clear cache when Pro status changes
function clearProCache() {
  proStatusCache = null;
  cacheExpiry = 0;
}

// --- enhanced toast system ---
let toastTimer;
function toast(msg, type = 'info', duration = 3000) {
  toastEl.textContent = msg;
  toastEl.classList.add('toast', 'show'); // Ensure 'toast' class is always present

  // Remove existing type classes
  toastEl.classList.remove('error', 'success', 'warning', 'info');

  // Add type-specific styling
  if (type !== 'info') {
    toastEl.classList.add(type);
  }

  // Add sound effect for different types
  playNotificationSound(type);

  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toastEl.classList.remove('show');
    // Remove the 'toast' class only after the transition is complete
    setTimeout(() => {
      toastEl.className = 'toast';
    }, 300);
  }, duration);
}

// Sound effects for better UX
function playNotificationSound(type) {
  // Create audio context for web audio
  try {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    // Different frequencies for different notification types
    switch(type) {
      case 'success':
        oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
        oscillator.frequency.setValueAtTime(1000, audioContext.currentTime + 0.1);
        break;
      case 'error':
        oscillator.frequency.setValueAtTime(300, audioContext.currentTime);
        oscillator.frequency.setValueAtTime(200, audioContext.currentTime + 0.1);
        break;
      case 'warning':
        oscillator.frequency.setValueAtTime(600, audioContext.currentTime);
        break;
      default:
        oscillator.frequency.setValueAtTime(500, audioContext.currentTime);
    }

    gainNode.gain.setValueAtTime(0, audioContext.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.1, audioContext.currentTime + 0.01);
    gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.2);

    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.2);
  } catch (e) {
    // Fallback - silent operation if audio context fails
  }
}

// Loading spinner utilities
const loadingSpinner = el("loadingSpinner");

function showLoading(text = "Generating quantum sigil...") {
  const loadingText = loadingSpinner.querySelector('.loading-text');
  if (loadingText) loadingText.textContent = text;
  loadingSpinner.classList.remove('hidden');
  document.body.style.overflow = 'hidden'; // Prevent scrolling
}

function hideLoading() {
  loadingSpinner.classList.add('hidden');
  document.body.style.overflow = ''; // Restore scrolling
}

// --- energy grid ---
async function renderEnergies() {
  const isPro = await isUserPro();
  const allowed = isPro ? ALL_ENERGIES : FREE_ENERGIES;
  console.log("Rendering energies - Pro:", isPro, "Allowed:", allowed);

  energyList.innerHTML = "";
  ALL_ENERGIES.forEach(name => {
    const div = document.createElement("div");
    const isLocked = !allowed.includes(name);
    div.className = "energy" + (isLocked ? " locked" : "");
    div.textContent = name;

    // Add visual indicator for pro energies
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
      // Check if energy is locked for current user
      const userIsPro = await isUserPro();
      const energyIsLocked = !userIsPro && !FREE_ENERGIES.includes(name);

      if (energyIsLocked) {
        toast("⚡ " + name + " energy requires Pro upgrade", 'warning');
        return;
      }

      // Always clear and rebuild selection to ensure consistency
      if (!comboToggle.checked) {
        // Single selection mode - replace current selection
        selectedEnergies = [name];
      } else {
        // Combo mode - toggle selection
        if (selectedEnergies.includes(name)) {
          // Remove from selection
          const newSelection = selectedEnergies.filter(e => e !== name);
          // Ensure at least one energy is always selected
          selectedEnergies = newSelection.length > 0 ? newSelection : [FREE_ENERGIES[0]];
        } else {
          // Add to selection if not already present
          selectedEnergies = [...selectedEnergies, name];
        }
      }

      console.log("Selected energies:", selectedEnergies);
      highlightSelection();
    };
    energyList.appendChild(div);
  });
  highlightSelection();
}
function highlightSelection() {
  const children = [...energyList.children];
  children.forEach(div => {
    const on = selectedEnergies.includes(div.textContent.trim());
    div.style.borderColor = on ? "#7ee787" : "#30364a";
  });
}

// --- gating view ---
async function renderGate() {
  const isPro = await isUserPro();
  console.log("Rendering gate with Pro status:", isPro);

  // Pro badge visibility - show when pro, hide when not
  if (isPro) {
    proBadge.classList.remove("hidden");
  } else {
    proBadge.classList.add("hidden");
  }

  // Pro controls visibility
  if (isPro) {
    proControls.classList.remove("hidden");
  } else {
    proControls.classList.add("hidden");
  }

  exportType.value = "png";
  if (isPro) {
    canvas.width = 2048; canvas.height = 2048;
    console.log("Pro mode: canvas set to 2048x2048");
  } else {
    canvas.width = 1200; canvas.height = 1200;
    comboToggle.checked = false;
    batchToggle.checked = false;
    console.log("Free mode: canvas set to 1200x1200");
  }
  await renderEnergies();
  await updateProButtons();
}

// --- pro button management ---
async function updateProButtons() {
  const isPro = await isUserPro();
  const proButtons = document.getElementById("proButtons");

  console.log("Updating Pro buttons - Pro status:", isPro);

  if (isPro) {
    // Hide pro purchase buttons when user is pro
    if (proButtons) {
      proButtons.style.display = 'none';
      console.log("Pro buttons hidden");
    }
  } else {
    // Show pro purchase buttons when user is not pro
    if (proButtons) {
      proButtons.style.display = 'flex';
      console.log("Pro buttons shown");
    }
  }
}

// --- key modal ---
enterKeyBtn.onclick = () => keyModal.showModal();
unlockBtn.onclick = async () => {
  const key = proKeyInput.value.trim();
  if (!key) return toast("Enter a key", 'warning');

  try {
    const r = await fetch("/api/verify-pro", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ key })
    });
    const j = await r.json();
    if (j.ok) {
      localStorage.setItem("sigil_pro","1");
      clearProCache(); // Clear the cache so next check gets fresh data
      keyModal.close();
      proKeyInput.value = ''; // Clear the input
      toast("✨ Pro unlocked successfully! All energies are now available!", 'success', 5000);

      // Force complete UI refresh
      setTimeout(async () => {
        await renderGate();
        await updateProButtons();
        await renderEnergies(); // Ensure energies are re-rendered with Pro status
      }, 100);
    } else {
      toast("❌ Invalid Pro key", 'error');
    }
  } catch (error) {
    console.error("Pro key verification error:", error);
    toast("❌ Error verifying key. Please try again.", 'error');
  }
};

// --- cooldown (free only) ---
function startCooldownIfNeeded() {
  isUserPro().then(isPro => {
    if (isPro) return;
    const now = Date.now();
    lastGenAt = now;
    const wait = 10000;
    genBtn.disabled = true;
    cooldownEl.classList.remove("hidden");
    let left = wait;
    const iv = setInterval(() => {
      left -= 1000;
      cooldownEl.textContent = `Ready in ${Math.ceil(left/1000)}s`;
      if (left <= 0) {
        clearInterval(iv);
        genBtn.disabled = false;
        cooldownEl.classList.add("hidden");
      }
    }, 1000);
  });
}

// --- drawing helpers ---
function clearCanvas() {
  ctx.fillStyle = "#0a0b0f"; ctx.fillRect(0,0,canvas.width,canvas.height);
}
async function drawWatermarkIfFree() {
  const isPro = await isUserPro();
  if (isPro) return;
  ctx.globalAlpha = 0.6;
  ctx.fillStyle = "#ffffff";
  ctx.font = `${Math.max(14, Math.floor(canvas.width * 0.04))}px monospace`;
  const text = "Sigilcraft";
  const m = ctx.measureText(text);
  ctx.fillText(text, canvas.width - m.width - 16, canvas.height - 16);
  ctx.globalAlpha = 1;
}

// Generate sigil using backend with retry logic
async function renderSigil(imageSrc, isSvg = false) {
  return new Promise((resolve, reject) => {
    try {
      clearCanvas();

      if (isSvg) {
        console.warn("SVG rendering path not fully implemented in this example.");
        // For now, we'll log a warning and proceed as if it's a data URL.
      }

      // Validate image source
      if (!imageSrc || typeof imageSrc !== 'string') {
        throw new Error("Invalid image source");
      }

      // Check if it's a valid data URL
      if (!imageSrc.startsWith('data:image/')) {
        throw new Error("Invalid image data format");
      }

      const img = new Image();
      
      img.onload = async () => {
        try {
          // Validate image dimensions
          if (img.width === 0 || img.height === 0) {
            throw new Error("Invalid image dimensions");
          }

          // Use high quality scaling
          ctx.imageSmoothingEnabled = true;
          ctx.imageSmoothingQuality = 'high';
          
          // Clear canvas before drawing
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          
          // Draw the image
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
          
          // Add watermark if needed
          await drawWatermarkIfFree();
          
          console.log("Image rendered to canvas successfully");
          resolve();
        } catch (renderError) {
          console.error("Error during image rendering:", renderError);
          reject(new Error(`Failed to render image: ${renderError.message}`));
        }
      };

      img.onerror = (errorEvent) => {
        console.error("Failed to load generated image:", errorEvent);
        reject(new Error("Failed to load generated image - invalid image data"));
      };

      // Set a timeout for image loading
      const imageTimeout = setTimeout(() => {
        reject(new Error("Image loading timed out"));
      }, 10000);

      img.onload = (originalOnload => async function(...args) {
        clearTimeout(imageTimeout);
        return originalOnload.apply(this, args);
      })(img.onload);

      img.onerror = (originalOnerror => function(...args) {
        clearTimeout(imageTimeout);
        return originalOnerror.apply(this, args);
      })(img.onerror);

      // Start loading the image
      img.src = imageSrc;

    } catch (error) {
      console.error("renderSigil error:", error);
      reject(error);
    }
  });
}


// Generate sigil using backend with retry logic
async function generateSigilRequest(phrase = "default", vibe = "mystical", retryCount = 0) {
  const maxRetries = 2; // Reduced retries for faster response
  const retryDelay = 500 * Math.min(retryCount + 1, 3); // Faster retry delay

  clearCanvas();

  try {
    console.log(`Sending sigil generation request (attempt ${retryCount + 1}):`, { phrase, vibe });

    // Reduced timeout for faster response
    const controller = new AbortController();
    const isComplexRequest = vibe.includes('+') || phrase.length > 50;
    const timeoutDuration = isComplexRequest ? 25000 : 15000; // Much shorter timeouts
    const timeoutId = setTimeout(() => controller.abort(), timeoutDuration);

    const response = await fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cache-Control": "no-cache"
      },
      body: JSON.stringify({ phrase: phrase.trim(), vibe }),
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    // Enhanced response validation with better error handling
    if (!response) {
      throw new Error("No response received from server");
    }

    if (!response.ok) {
      const errorText = await response.text().catch(() => `HTTP ${response.status}`);
      throw new Error(`Server error: ${errorText}`);
    }

    const contentType = response.headers.get("content-type");
    if (!contentType || !contentType.includes("application/json")) {
      const text = await response.text();
      console.error("Non-JSON response:", text.substring(0, 500));
      throw new Error("Server returned invalid response format");
    }

    const data = await response.json();
    
    // Better validation of response data
    if (!data) {
      throw new Error("Empty response from server");
    }

    if (!data.success) {
      const errorMsg = data.error || "Generation failed";
      console.error("Generation failed:", errorMsg);
      
      // Show user-friendly error message
      if (errorMsg.includes("timeout") || errorMsg.includes("timed out")) {
        toast("⏱️ Generation taking longer than expected. Retrying with optimized settings...", 'warning', 3000);
        throw new Error("timeout");
      } else if (errorMsg.includes("rate limit")) {
        toast("⏳ Rate limit reached. Please wait a moment...", 'warning', 3000);
        throw new Error("rate_limit");
      } else {
        toast(`❌ ${errorMsg}`, 'error', 4000);
        throw new Error(errorMsg);
      }
    }

    if (!data.image) {
      throw new Error("No image data received");
    }

    // Successfully generated - render the sigil
    await renderSigil(data.image, phrase, vibe);
    return data;

  } catch (error) {
    console.error("Generation request error:", error);
    
    // Handle specific error types
    if (error.name === 'AbortError' || error.message === 'timeout') {
      if (retryCount < maxRetries) {
        console.log(`Request timed out, retrying... (${retryCount + 1}/${maxRetries})`);
        await new Promise(resolve => setTimeout(resolve, retryDelay));
        return generateSigilRequest(phrase, vibe, retryCount + 1);
      } else {
        toast("⏱️ Generation is taking too long. Please try a shorter phrase or simpler vibe.", 'error', 5000);
        throw new Error("Generation timed out after multiple attempts");
      }
    }
    
    if (error.message === 'rate_limit') {
      throw error; // Don't retry rate limit errors
    }
    
    // Only retry on network errors or server errors
    if (retryCount < maxRetries && (
      error.message.includes('fetch') || 
      error.message.includes('network') ||
      error.message.includes('Server error')
    )) {
      console.log(`Retrying due to network/server error... (${retryCount + 1}/${maxRetries})`);
      await new Promise(resolve => setTimeout(resolve, retryDelay));
      return generateSigilRequest(phrase, vibe, retryCount + 1);
    }
    
    throw error;
  }rver");
    }

    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}`;
      try {
        const errorText = await response.text();
        const errorData = errorText ? JSON.parse(errorText) : {};
        errorMessage = errorData.error || `Server error: ${response.status}`;
      } catch (parseError) {
        console.warn("Could not parse error response:", parseError);
      }

      if (response.status === 429) {
        throw new Error("Rate limit exceeded. Please wait before trying again.");
      } else if (response.status === 503) {
        throw new Error("Service temporarily unavailable. Please try again.");
      } else if (response.status === 408) {
        throw new Error("Request timeout. Please try again.");
      } else {
        throw new Error(errorMessage);
      }
    }

    // Enhanced response parsing with validation
    let data;
    try {
      const responseText = await response.text();
      if (!responseText) {
        throw new Error("Empty response from server");
      }
      data = JSON.parse(responseText);
    } catch (parseError) {
      console.error("Response parsing error:", parseError);
      throw new Error("Invalid response format from server");
    }

    console.log("Received response:", data.success ? "Success" : "Failed", data.error || "");

    // Enhanced validation of response data
    if (!data || typeof data !== 'object') {
      throw new Error("Invalid response data structure");
    }

    if (data.success && data.image) {
      // Validate image data
      if (typeof data.image !== 'string' || data.image.length < 100) {
        throw new Error("Invalid image data received");
      }

      lastGeneratedImage = data.image;
      console.log("Stored image for download, length:", data.image.length);
      
      try {
        await renderSigil(data.image, false);
        downloadBtn.style.display = 'block';
        return { success: true };
      } catch (renderError) {
        console.error("Image rendering error:", renderError);
        throw new Error("Failed to display generated image");
      }
    } else {
      const errorMsg = data.error || "Generation failed - no image data received";
      console.warn("Generation failed:", errorMsg);
      return {
        success: false,
        error: errorMsg
      };
    }
  } catch (error) {
    console.error("Sigil generation error:", error);

    // Enhanced error categorization and messaging
    let errorMessage = '⚠️ Generation failed. Please try again.';
    let retryable = true;

    const errorStr = error.message || error.toString() || 'Unknown error';

    if (error.name === 'AbortError' || errorStr.includes('timeout') || errorStr.includes('aborted')) {
      errorMessage = '⏱️ Generation timed out. Try a simpler phrase or try again.';
      retryable = true;
    } else if (errorStr.includes('408') || errorStr.includes('Request timeout')) {
      errorMessage = '⏱️ Request timed out. Please try again with a simpler phrase.';
      retryable = true;
    } else if (errorStr.includes('503') || errorStr.includes('Service')) {
      errorMessage = '🔄 Service starting up. Please wait a moment and try again.';
      retryable = true;
    } else if (errorStr.includes('rate limit') || errorStr.includes('429')) {
      errorMessage = '⏳ Too many requests. Please wait before trying again.';
      retryable = false;
    } else if (errorStr.includes('Invalid characters')) {
      errorMessage = '🚫 Invalid characters in your intent. Please remove them.';
      retryable = false;
    } else if (errorStr.includes('too long') || errorStr.includes('too short')) {
      errorMessage = `📝 ${errorStr}`;
      retryable = false;
    } else if (errorStr.includes('not available')) {
      errorMessage = `⚡ ${errorStr}`;
      retryable = true;
    } else if (errorStr.includes('Failed to fetch') || errorStr.includes('Network')) {
      errorMessage = '🌐 Network error. Please check your connection and try again.';
      retryable = true;
    } else if (errorStr.includes('Empty response') || errorStr.includes('Invalid response')) {
      errorMessage = '📡 Invalid server response. Please try again.';
      retryable = true;
    } else if (errorStr.includes('display') || errorStr.includes('render')) {
      errorMessage = '🖼️ Failed to display image. Please try regenerating.';
      retryable = true;
    }

    toast(errorMessage, 'error', 5000);

    return {
      success: false,
      error: errorMessage,
      retryable: retryable
    };
  }
}

// seeded RNG
function mulberry32(a){return function(){var t=a+=0x6D2B79F5;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return ((t^t>>>14)>>>0)/4294967296}}

// SVG export: mirrors the placeholder look
function buildSvg(seed = 0, size = 2048) {
  const r = mulberry32(seed || 1);
  const n = 120;
  const pts = [];
  for (let i=0;i<n;i++) pts.push(`${Math.floor(size*r())},${Math.floor(size*r())}`);
  const poly = pts.join(" ");
  return `
<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" style="background:#0a0b0f">
  <polyline points="${poly}" fill="none" stroke="#9ad0ff" stroke-width="${Math.max(2, Math.floor(size*0.004))}" />
</svg>`.trim();
}

// --- generation + download ---
// Input validation utilities
const validatePhrase = (phrase) => {
  if (!phrase || typeof phrase !== 'string') {
    return { valid: false, error: "Please enter your intent or desire" };
  }

  const trimmed = phrase.trim();
  if (trimmed.length === 0) {
    return { valid: false, error: "Please enter your intent or desire" };
  }

  if (trimmed.length > 200) {
    return { valid: false, error: "Intent is too long (maximum 200 characters)" };
  }

  if (trimmed.length < 2) {
    return { valid: false, error: "Intent is too short (minimum 2 characters)" };
  }

  // Check for potentially harmful content
  const harmfulPatterns = [
    /<script/i, /javascript:/i, /vbscript:/i, /data:/i,
    /onload=/i, /onerror=/i, /onclick=/i
  ];

  for (const pattern of harmfulPatterns) {
    if (pattern.test(trimmed)) {
      return { valid: false, error: "Invalid characters detected" };
    }
  }

  return { valid: true, phrase: trimmed };
};

const validateEnergies = (energies, isPro) => {
  if (!Array.isArray(energies) || energies.length === 0) {
    return { valid: false, error: "Select at least one energy type" };
  }

  const allowedEnergies = isPro ? ALL_ENERGIES : FREE_ENERGIES;
  const invalidEnergies = energies.filter(e => !allowedEnergies.includes(e));

  if (invalidEnergies.length > 0) {
    return {
      valid: false,
      error: `${invalidEnergies.join(", ")} ${invalidEnergies.length === 1 ? 'is' : 'are'} not available`
    };
  }

  if (!isPro && energies.length > 1) {
    return { valid: false, error: "Multiple energies require Pro upgrade" };
  }

  return { valid: true };
};

genBtn.onclick = async () => {
  try {
    // Validate energies
    const isPro = await isUserPro();
    const energyValidation = validateEnergies(selectedEnergies, isPro);
    if (!energyValidation.valid) {
      toast(energyValidation.error, 'warning');
      return;
    }

    // Get and validate phrase
    const intentInput = document.getElementById("intentInput");
    if (!intentInput) {
      toast("Intent input field not found", 'error');
      return;
    }

    const phraseValidation = validatePhrase(intentInput.value);
    if (!phraseValidation.valid) {
      toast(phraseValidation.error, 'warning');
      return;
    }

    const phrase = phraseValidation.phrase;

    // Handle multiple vibes by combining them or using combo mode
    const vibe = selectedEnergies.length > 1 ? selectedEnergies.join("+") : selectedEnergies[0];
    const size = isPro ? 2048 : 1200;

    canvas.width = size; canvas.height = size;
    genBtn.disabled = true;
    genBtn.textContent = "Generating...";

    showLoading(isPro && batchToggle.checked ? "Creating sigil batch..." : "Channeling quantum energy...");

    if (isPro && batchToggle.checked) {
      // Batch generation
      if (typeof JSZip === 'undefined') {
        toast("JSZip library not loaded", 'error');
        return;
      }

      const zip = new JSZip();
      let successCount = 0;
      const batchSize = 5;

      for (let i = 0; i < batchSize; i++){
        try {
          showLoading(`Creating sigil ${i + 1} of ${batchSize}...`);
          const batchPhrase = `${phrase} variant ${i + 1}`;
          
          // Try generation with retry logic
          let result = null;
          let attempts = 0;
          const maxAttempts = 2;

          while (attempts < maxAttempts && (!result || !result.success)) {
            try {
              result = await generateSigilRequest(batchPhrase, vibe);
              if (result && result.success) break;
            } catch (batchError) {
              console.warn(`Batch attempt ${attempts + 1} failed:`, batchError);
            }
            attempts++;
            if (attempts < maxAttempts) {
              await new Promise(resolve => setTimeout(resolve, 1000));
            }
          }

          if (result && result.success && lastGeneratedImage) {
            const base64Data = lastGeneratedImage.includes(',') ? lastGeneratedImage.split(",")[1] : lastGeneratedImage;
            zip.file(`sigil_${i+1}.png`, base64Data, {base64: true});
            successCount++;
          } else {
            console.warn(`Failed to generate sigil ${i + 1} after ${attempts} attempts`);
          }
        } catch (error) {
          console.error(`Error generating sigil ${i + 1}:`, error);
        }
      }

      if (successCount > 0) {
        try {
          const blob = await zip.generateAsync({type:"blob"});
          downloadFile(blob, "sigils.zip");
          toast(`✨ ${successCount}/${batchSize} sigils ready for download!`, 'success', 4000);
        } catch (zipError) {
          console.error("Zip creation error:", zipError);
          toast("❌ Failed to create download package", 'error');
        }
      } else {
        toast("❌ Failed to generate any batch sigils", 'error');
      }
    } else {
      // Single generation with retry logic
      let result = null;
      let attempts = 0;
      const maxAttempts = 3;

      while (attempts < maxAttempts && (!result || !result.success)) {
        try {
          if (attempts > 0) {
            const delay = 1000 * attempts;
            console.log(`Retrying generation (attempt ${attempts}/${maxAttempts})... Delay: ${delay}ms`);
            showLoading(`Retrying generation (${attempts + 1}/${maxAttempts})...`);
            await new Promise(resolve => setTimeout(resolve, delay));
          }

          result = await generateSigilRequest(phrase, vibe);

          if (result && result.success) {
            toast("✨ Quantum sigil generated successfully!", 'success', 3000);
            break;
          } else if (result && !result.retryable) {
            // Don't retry if error is not retryable
            break;
          }
        } catch (genError) {
          console.error(`Generation attempt ${attempts + 1} failed:`, genError);
          result = { success: false, error: genError.message || 'Generation failed', retryable: true };
        }
        attempts++;
      }

      if (!result || !result.success) {
        const errorMsg = result?.error || 'Unknown generation error';
        console.error("All generation attempts failed:", errorMsg);
        // Error message already shown by generateSigilRequest
      }
    }
  } catch (error) {
    console.error("Generation process error:", error);
    toast(`❌ Generation failed: ${error.message || 'Unknown error'}`, 'error', 5000);
  } finally {
    hideLoading();
    genBtn.disabled = false;
    genBtn.textContent = "Initialize Quantum Sigil";
    startCooldownIfNeeded();
  }
};

downloadBtn.onclick = async () => {
  console.log("Download button clicked");

  try {
    const userIsPro = await isUserPro();
    const seed = Number(seedInput.value) || 0;

    // Check if we have a current sigil to download
    if (!lastGeneratedImage) {
      console.log("No image available for download");
      toast("⚠️ Generate a sigil first to download", 'warning');
      return;
    }

    console.log("Image available for download, size:", lastGeneratedImage.length);

    if (userIsPro && exportType.value === "svg") {
      // SVG Download
      console.log("Downloading as SVG");
      const svg = buildSvg(seed, 2048);
      const blob = new Blob([svg], {type:"image/svg+xml"});
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
      const filename = `quantum_sigil_${timestamp}.svg`;
      downloadFile(blob, filename);
      toast("✨ SVG sigil downloaded!", 'success');
    } else {
      // PNG Download - use canvas directly for most reliable download
      console.log("Downloading as PNG via canvas");

      if (!canvas || canvas.width === 0 || canvas.height === 0) {
        throw new Error("Canvas not available for download");
      }

      // Convert canvas to blob
      canvas.toBlob((blob) => {
        if (!blob || blob.size === 0) {
          console.error("Canvas produced empty blob");
          toast("❌ Download failed - please regenerate the sigil", 'error');
          return;
        }

        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
        const filename = `quantum_sigil_${timestamp}.png`;

        console.log("Created canvas blob for download:", {
          filename,
          size: blob.size,
          type: blob.type
        });

        downloadFile(blob, filename);
        toast("✨ Quantum Sigil downloaded successfully!", 'success');
      }, 'image/png', 1.0);
    }

  } catch (error) {
    console.error("Download error:", error);
    toast(`❌ Download failed: ${error.message}`, 'error');
  }
};

// Simple, reliable download function
function downloadFile(blob, filename) {
  console.log("Starting download:", filename, "size:", blob.size);

  try {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');

    link.href = url;
    link.download = filename;
    link.style.display = 'none';

    // Add to DOM, click, and clean up immediately
    document.body.appendChild(link);
    link.click();

    // Clean up immediately
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    console.log("Download completed successfully");
  } catch (error) {
    console.error("Download file error:", error);
    throw error;
  }
}

// Legacy download function for batch downloads
function triggerDownload(blob, filename) {
  downloadFile(blob, filename);
}

// === NEW POPULAR FEATURES ===

// Sigil Animation Feature
let animationFrame = null;
let isAnimating = false;

function toggleSigilAnimation() {
  const animateBtn = document.getElementById('animateBtn');
  
  if (!animateBtn) {
    console.error('Animate button not found');
    return;
  }

  if (isAnimating) {
    stopAnimation();
    animateBtn.textContent = '✨ Animate Sigil';
  } else {
    startAnimation();
    animateBtn.textContent = '⏸️ Stop Animation';
  }
}

// Make function globally available
window.toggleSigilAnimation = toggleSigilAnimation;

function startAnimation() {
  if (!canvas || !lastGeneratedImage) {
    toast('⚠️ Generate a sigil first to animate', 'warning');
    return;
  }

  isAnimating = true;
  let frame = 0;
  
  // Store the original image
  const originalImg = new Image();
  originalImg.onload = () => {
    const animate = () => {
      if (!isAnimating) return;

      const ctx = canvas.getContext('2d');
      
      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Save context
      ctx.save();

      // Create pulsing and rotation effects
      const scale = 1 + Math.sin(frame * 0.08) * 0.03;
      const rotation = Math.sin(frame * 0.04) * 0.01;
      const opacity = 0.9 + Math.sin(frame * 0.1) * 0.1;

      // Apply transformations
      ctx.translate(canvas.width / 2, canvas.height / 2);
      ctx.scale(scale, scale);
      ctx.rotate(rotation);
      ctx.globalAlpha = opacity;
      ctx.translate(-canvas.width / 2, -canvas.height / 2);

      // Draw the image
      ctx.drawImage(originalImg, 0, 0, canvas.width, canvas.height);

      // Restore context
      ctx.restore();
      
      frame++;
      animationFrame = requestAnimationFrame(animate);
    };

    animate();
  };
  
  originalImg.src = lastGeneratedImage;
}

function stopAnimation() {
  isAnimating = false;
  if (animationFrame) {
    cancelAnimationFrame(animationFrame);
    animationFrame = null;
  }

  // Restore original image
  if (lastGeneratedImage) {
    const img = new Image();
    img.onload = () => {
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    };
    img.src = lastGeneratedImage;
  }
}

// Sigil Rating System
function rateSigil(rating) {
  const stars = document.querySelectorAll('.star-rating .star');
  stars.forEach((star, index) => {
    star.classList.toggle('active', index < rating);
  });

  // Store rating
  const sigilData = {
    phrase: document.getElementById("intentInput").value,
    vibe: selectedEnergies.join('+'),
    rating: rating,
    timestamp: Date.now()
  };

  // Save to local storage
  const ratings = JSON.parse(localStorage.getItem('sigil_ratings') || '[]');
  ratings.push(sigilData);
  localStorage.setItem('sigil_ratings', JSON.stringify(ratings.slice(-50))); // Keep last 50

  toast(`✨ Rated ${rating} star${rating !== 1 ? 's' : ''}! Thank you!`, 'success');
  updateAverageRating();
}

function updateAverageRating() {
  const ratings = JSON.parse(localStorage.getItem('sigil_ratings') || '[]');
  if (ratings.length === 0) return;

  const average = ratings.reduce((sum, r) => sum + r.rating, 0) / ratings.length;
  const avgDisplay = document.getElementById('averageRating');
  if (avgDisplay) {
    avgDisplay.textContent = `Average: ${average.toFixed(1)}⭐ (${ratings.length} ratings)`;
  }
}

// Enhanced Sharing Feature
async function shareSigil() {
  try {
    if (!lastGeneratedImage) {
      toast('⚠️ Generate a sigil first to share', 'warning');
      return;
    }

    const intentInput = document.getElementById("intentInput");
    if (!intentInput) {
      toast('⚠️ Cannot find input field', 'error');
      return;
    }

    const phrase = intentInput.value;
    const vibe = selectedEnergies.join('+');

    // Create share data
    const shareText = `🔮 I just created a ${vibe} sigil for "${phrase}" using Sigilcraft! ✨`;

    if (navigator.share) {
      // Use Web Share API if available
      try {
        const blob = await canvasToBlob();
        
        if (blob && navigator.canShare && navigator.canShare({ files: [new File([blob], 'sigil.png', { type: 'image/png' })] })) {
          const file = new File([blob], 'my-sigil.png', { type: 'image/png' });
          await navigator.share({
            title: 'My Quantum Sigil',
            text: shareText,
            files: [file]
          });
          toast('✨ Sigil shared successfully!', 'success');
          return;
        } else {
          // Fallback to text-only sharing
          await navigator.share({
            title: 'My Quantum Sigil',
            text: shareText
          });
          toast('✨ Shared successfully!', 'success');
          return;
        }
      } catch (shareError) {
        console.log('Native share failed, falling back to copy');
        fallbackShare(shareText);
      }
    } else {
      fallbackShare(shareText);
    }
  } catch (error) {
    console.error('Share error:', error);
    toast('❌ Share failed, but you can copy the text!', 'error');
  }
}

// Make function globally available
window.shareSigil = shareSigil;

function fallbackShare(text) {
  // Copy to clipboard
  navigator.clipboard.writeText(text).then(() => {
    toast('📋 Share text copied to clipboard!', 'success');
  }).catch(() => {
    // Create a temporary text area for copying
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
    toast('📋 Share text copied!', 'success');
  });
}

async function canvasToBlob() {
  return new Promise((resolve) => {
    canvas.toBlob(resolve, 'image/png', 1.0);
  });
}

// Sigil Gallery Feature
function showSigilGallery() {
  const gallery = document.getElementById('sigilGallery');
  const galleryContent = document.getElementById('galleryContent');
  
  if (!gallery || !galleryContent) {
    toast('⚠️ Gallery not available', 'error');
    return;
  }

  // Load saved sigils from localStorage
  const savedSigils = JSON.parse(localStorage.getItem('saved_sigils') || '[]');

  galleryContent.innerHTML = '';

  if (savedSigils.length === 0) {
    galleryContent.innerHTML = '<p style="text-align: center; color: var(--text-muted); padding: 40px;">No saved sigils yet. Generate and save some!</p>';
  } else {
    savedSigils.slice(-12).reverse().forEach((sigil, index) => {
      const item = document.createElement('div');
      item.className = 'gallery-item';
      item.innerHTML = `
        <img src="${sigil.image}" alt="Sigil ${index + 1}">
        <div class="gallery-info">
          <small title="${sigil.phrase}">${sigil.phrase.length > 20 ? sigil.phrase.substring(0, 20) + '...' : sigil.phrase}</small>
          <small>${sigil.vibe}</small>
        </div>
      `;
      
      // Add click handler
      item.onclick = () => loadSigilFromGallery(sigil.id);
      
      galleryContent.appendChild(item);
    });
  }

  gallery.style.display = 'flex';
}

// Make function globally available
window.showSigilGallery = showSigilGallery;

function hideSigilGallery() {
  document.getElementById('sigilGallery').style.display = 'none';
}

function saveSigilToGallery() {
  if (!lastGeneratedImage) {
    toast('⚠️ Generate a sigil first to save', 'warning');
    return;
  }

  const phrase = document.getElementById("intentInput").value;
  const vibe = selectedEnergies.join('+');

  const sigilData = {
    id: Date.now().toString(),
    phrase: phrase,
    vibe: vibe,
    image: lastGeneratedImage,
    timestamp: Date.now()
  };

  const savedSigils = JSON.parse(localStorage.getItem('saved_sigils') || '[]');
  savedSigils.push(sigilData);

  // Keep only last 50 sigils
  localStorage.setItem('saved_sigils', JSON.stringify(savedSigils.slice(-50)));

  toast('💾 Sigil saved to gallery!', 'success');
}

function loadSigilFromGallery(id) {
  const savedSigils = JSON.parse(localStorage.getItem('saved_sigils') || '[]');
  const sigil = savedSigils.find(s => s.id === id);

  if (sigil) {
    lastGeneratedImage = sigil.image;
    const intentInput = document.getElementById("intentInput");
    if (intentInput) {
      intentInput.value = sigil.phrase;
    }

    // Update selected energies
    selectedEnergies = sigil.vibe.split('+');
    highlightSelection();

    // Display the sigil
    const img = new Image();
    img.onload = async () => {
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      await drawWatermarkIfFree();
    };
    img.src = sigil.image;

    downloadBtn.style.display = 'block';
    hideSigilGallery();
    toast('✨ Sigil loaded from gallery!', 'success');
  }
}

function hideSigilGallery() {
  const gallery = document.getElementById('sigilGallery');
  if (gallery) {
    gallery.style.display = 'none';
  }
}

function saveSigilToGallery() {
  if (!lastGeneratedImage) {
    toast('⚠️ Generate a sigil first to save', 'warning');
    return;
  }

  const intentInput = document.getElementById("intentInput");
  if (!intentInput) {
    toast('⚠️ Cannot find input field', 'error');
    return;
  }

  const phrase = intentInput.value || 'Untitled Sigil';
  const vibe = selectedEnergies.join('+');

  const sigilData = {
    id: Date.now().toString(),
    phrase: phrase,
    vibe: vibe,
    image: lastGeneratedImage,
    timestamp: Date.now()
  };

  const savedSigils = JSON.parse(localStorage.getItem('saved_sigils') || '[]');
  savedSigils.push(sigilData);

  // Keep only last 50 sigils
  localStorage.setItem('saved_sigils', JSON.stringify(savedSigils.slice(-50)));

  toast('💾 Sigil saved to gallery!', 'success');
}

// Sigil Rating System
function rateSigil(rating) {
  const stars = document.querySelectorAll('.star-rating .star');
  stars.forEach((star, index) => {
    star.classList.toggle('active', index < rating);
  });

  const intentInput = document.getElementById("intentInput");
  const phrase = intentInput ? intentInput.value : 'Unknown';

  // Store rating
  const sigilData = {
    phrase: phrase,
    vibe: selectedEnergies.join('+'),
    rating: rating,
    timestamp: Date.now()
  };

  // Save to local storage
  const ratings = JSON.parse(localStorage.getItem('sigil_ratings') || '[]');
  ratings.push(sigilData);
  localStorage.setItem('sigil_ratings', JSON.stringify(ratings.slice(-50))); // Keep last 50

  toast(`✨ Rated ${rating} star${rating !== 1 ? 's' : ''}! Thank you!`, 'success');
  updateAverageRating();
}

function updateAverageRating() {
  const ratings = JSON.parse(localStorage.getItem('sigil_ratings') || '[]');
  if (ratings.length === 0) return;

  const average = ratings.reduce((sum, r) => sum + r.rating, 0) / ratings.length;
  const avgDisplay = document.getElementById('averageRating');
  if (avgDisplay) {
    avgDisplay.textContent = `Average: ${average.toFixed(1)}⭐ (${ratings.length} ratings)`;
  }
}

// Make functions globally available
window.hideSigilGallery = hideSigilGallery;
window.saveSigilToGallery = saveSigilToGallery;
window.rateSigil = rateSigil;

// -------- Stripe Checkout --------
async function goPremiumCheckout() {
  try {
    const r = await fetch("/api/create-checkout-session", { method: "POST" });
    const j = await r.json();
    if (j.url) window.location.href = j.url;
    else toast("Checkout error — try again.");
  } catch (e) {
    toast("Network error — server down?");
    console.error(e);
  }
}
window.goPremiumCheckout = goPremiumCheckout;

// init
window.addEventListener("load", async () => {
  try {
    await renderGate();

    // Initialize new features
    updateAverageRating();

    // Check for purchase success/cancel
    const p = new URLSearchParams(location.search);
    if (p.get("purchase") === "success") {
      toast("🎉 Payment successful! Check your email for your Pro key.", 'success', 5000);
    } else if (p.get("purchase") === "cancel") {
      toast("Purchase cancelled.", 'warning');
    }

    // Welcome message for new features
    setTimeout(() => {
      toast("✨ New features added: Animation, Gallery, Rating & Sharing!", 'success', 4000);
    }, 2000);

  } catch (error) {
    console.error("Initialization error:", error);
    toast("⚠️ App initialization error. Please refresh the page.", 'error');
  }
});

// keep previewSvg hidden unless you want to show the SVG string; we use direct download instead.