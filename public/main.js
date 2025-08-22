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

// --- pro detection ---
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
  return (await serverIsPro()) || localIsPro();
}

// --- enhanced toast system ---
let toastTimer;
function toast(msg, type = 'info', duration = 3000) {
  toastEl.textContent = msg;
  toastEl.className = 'toast show';

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
      } else {
        div.title = "🔒 Pro Energy - Upgrade to unlock";
      }
    }

    div.onclick = () => {
      if (isLocked) { 
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
      keyModal.close();
      proKeyInput.value = ''; // Clear the input
      toast("✨ Pro unlocked successfully!", 'success', 4000);

      // Force UI refresh
      await renderGate();
      await updateProButtons();
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
async function renderSigil(imageSrc, isSvg = false) { // Modified to accept imageSrc and isSvg flag
  clearCanvas();

  if (isSvg) {
    // Handle SVG rendering if needed, though current flow uses PNG
    console.warn("SVG rendering path not fully implemented in this example.");
    // If you had an SVG rendering library, you would use it here.
    // For now, we'll log a warning and proceed as if it's a data URL.
  }

  const img = new Image();
  img.onload = async () => {
    // Use high quality scaling
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    await drawWatermarkIfFree();
    console.log("Image rendered to canvas");
  };
  img.onerror = () => {
    console.error("Failed to load generated image");
    toast("Failed to display generated image", 'error');
  };
  img.src = imageSrc;
}


// Generate sigil using backend with retry logic
async function generateSigilRequest(phrase = "default", vibe = "mystical", retryCount = 0) {
  const maxRetries = 3;
  const retryDelay = 1000 * Math.min(retryCount + 1, 5); // Progressive delay with cap

  clearCanvas();

  try {
    console.log(`Sending sigil generation request (attempt ${retryCount + 1}):`, { phrase, vibe });

    // Add timeout to fetch request with longer timeout for complex requests
    const controller = new AbortController();
    const isComplexRequest = vibe.includes('+') || phrase.length > 50;
    const timeoutDuration = isComplexRequest ? 45000 : 30000;
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

    if (!response.ok) {
      if (response.status === 429) {
        throw new Error("Rate limit exceeded. Please wait before generating another sigil.");
      } else if (response.status === 503) {
        throw new Error("Sigil generation service temporarily unavailable. Please try again.");
      } else {
        // Attempt to get error message from response body
        const errorData = await response.json().catch(() => ({ error: `Server error: ${response.status}` }));
        throw new Error(errorData.error || `Server error: ${response.status}`);
      }
    }

    const data = await response.json();
    console.log("Received response:", data.success ? "Success" : "Failed", data.error || "");

    if (data.success && data.image) { // Assuming 'image' field contains the base64 PNG data
      lastGeneratedImage = data.image; // Store for download
      console.log("Stored image for download, length:", data.image.length);
      await renderSigil(data.image, false); // Render the PNG
      downloadBtn.style.display = 'block'; // Ensure download button is visible
      return { success: true };
    } else {
      return {
        success: false,
        error: data.error || "Generation failed - no image data received"
      };
    }
  } catch (error) {
    console.error("Sigil generation error:", error);

    // Retry logic for network errors or timeouts
    if (retryCount < maxRetries && (
      error.name === 'AbortError' ||
      error.message.includes('Failed to fetch') ||
      error.message.includes('temporarily unavailable') ||
      error.message.includes('NetworkError') || // Common for fetch issues
      error.message.includes('timeout') ||
      error.message.includes('Rate limit exceeded') // Explicitly catch rate limit for retries
    )) {
      console.log(`Retrying generation (attempt ${retryCount + 1}/${maxRetries})... Delay: ${retryDelay}ms`);
      await new Promise(resolve => setTimeout(resolve, retryDelay)); // Use progressive delay
      return generateSigilRequest(phrase, vibe, retryCount + 1);
    }

    // Handle specific error messages for user feedback
    let errorMessage = '⚠️ Generation failed. Please try again.';
    if (error.message.includes('timeout')) {
      errorMessage = '⏱️ Generation timed out. Try a simpler phrase or try again.';
    } else if (error.message.includes('503')) {
      errorMessage = '🔄 Service starting up. Please wait a moment and try again.';
    } else if (error.message.includes('rate limit')) {
      errorMessage = '⏳ Too many requests. Please wait before trying again.';
    } else if (error.message.includes('Invalid characters detected')) {
      errorMessage = '🚫 Invalid characters in your intent. Please remove them.';
    } else if (error.message.includes('Intent is too long') || error.message.includes('Intent is too short')) {
      errorMessage = `📝 ${error.message}`;
    } else if (error.message.includes('not available')) {
      errorMessage = `⚡ ${error.message}`;
    }

    // Display error message in the designated display area or via toast
    const sigilDisplay = document.getElementById('sigil-display');
    if (sigilDisplay) {
      sigilDisplay.innerHTML = `<p style="color: #ff6b6b; text-align: center;">${errorMessage}</p>`;
    } else {
      toast(errorMessage, 'error', 5000);
    }

    return {
      success: false,
      error: errorMessage,
      retryable: false
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
  // Validate energies
  const isPro = await isUserPro();
  const energyValidation = validateEnergies(selectedEnergies, isPro);
  if (!energyValidation.valid) {
    toast(energyValidation.error);
    return;
  }

  // Get and validate phrase
  const intentInput = document.getElementById("intentInput");
  if (!intentInput) {
    toast("Intent input field not found");
    return;
  }

  const phraseValidation = validatePhrase(intentInput.value);
  if (!phraseValidation.valid) {
    toast(phraseValidation.error);
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

  try {
    if (isPro && batchToggle.checked) {
      // batch create zip of 5
      if (typeof JSZip === 'undefined') {
        toast("JSZip library not loaded", 'error');
        return;
      }

      const zip = new JSZip();
      let successCount = 0;

      for (let i = 0; i < 5; i++){
        try {
          showLoading(`Creating sigil ${i + 1} of 5...`);
          const batchPhrase = `${phrase} variant ${i + 1}`;
          const result = await generateSigilRequest(batchPhrase, vibe); // Use the refined generation function

          if (result && result.success && lastGeneratedImage) { // Check if image was successfully stored
            const base64Data = lastGeneratedImage.includes(',') ? lastGeneratedImage.split(",")[1] : lastGeneratedImage;
            zip.file(`sigil_${i+1}.png`, base64Data, {base64: true});
            successCount++;
          } else {
            console.warn(`Failed to generate sigil ${i + 1}:`, result?.error || 'Unknown error');
          }
        } catch (error) {
          console.error(`Error generating sigil ${i + 1}:`, error);
          // Continue with other sigils even if one fails
        }
      }

      if (successCount > 0) {
        const blob = await zip.generateAsync({type:"blob"});
        downloadFile(blob, "sigils.zip");
        toast(`✨ ${successCount} sigils ready for download!`, 'success', 4000);
      } else {
        toast("❌ Failed to generate batch sigils", 'error');
      }
    } else {
      // single
      const result = await generateSigilRequest(phrase, vibe); // Use the refined generation function

      if (result && result.success) {
        toast("✨ Quantum sigil generated successfully!", 'success', 3000);
      } else {
        const errorMsg = result?.error || 'Unknown generation error';
        toast(`❌ Generation failed: ${errorMsg}`, 'error', 5000);
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

    // Check for purchase success/cancel
    const p = new URLSearchParams(location.search);
    if (p.get("purchase") === "success") {
      toast("🎉 Payment successful! Check your email for your Pro key.", 'success', 5000);
    } else if (p.get("purchase") === "cancel") {
      toast("Purchase cancelled.", 'warning');
    }
  } catch (error) {
    console.error("Initialization error:", error);
    toast("⚠️ App initialization error. Please refresh the page.", 'error');
  }
});

// keep previewSvg hidden unless you want to show the SVG string; we use direct download instead.