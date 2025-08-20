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
async function isUserPro() { // Renamed for clarity and consistency
  return (await serverIsPro()) || localIsPro();
}

// --- enhanced toast system ---
let toastTimer;
function toast(msg, type = 'info', duration = 3000) {
  toastEl.textContent = msg;
  toastEl.className = 'show';

  // Remove existing type classes
  toastEl.classList.remove('error', 'success', 'warning', 'info');

  // Add type-specific styling
  if (type !== 'info') {
    toastEl.classList.add(type);
  }

  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toastEl.classList.remove('show');
    setTimeout(() => {
      toastEl.style.display = "none";
      toastEl.className = '';
    }, 300);
  }, duration);
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
  const pro = await isUserPro();
  const allowed = pro ? ALL_ENERGIES : FREE_ENERGIES;
  energyList.innerHTML = "";
  ALL_ENERGIES.forEach(name => {
    const div = document.createElement("div");
    div.className = "energy" + (allowed.includes(name) ? "" : " locked");
    div.textContent = name;
    div.onclick = () => {
      if (!allowed.includes(name)) { toast("Pro feature"); return; }
      if (!comboToggle.checked) {
        // Single selection mode
        selectedEnergies = [name];
      } else {
        // Combo mode - allow multiple selections
        if (selectedEnergies.includes(name)) {
          selectedEnergies = selectedEnergies.filter(e => e !== name);
          // Ensure at least one energy is always selected
          if (selectedEnergies.length === 0) {
            selectedEnergies = [FREE_ENERGIES[0]]; // Default to mystical
          }
        } else {
          selectedEnergies.push(name);
        }
      }
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
  const pro = await isUserPro();
  proBadge.classList.toggle("hidden", !pro);
  proControls.classList.toggle("hidden", !pro);
  exportType.value = "png";
  if (pro) {
    canvas.width = 2048; canvas.height = 2048;
  } else {
    canvas.width = 1200; canvas.height = 1200;
    comboToggle.checked = false;
    batchToggle.checked = false;
  }
  await renderEnergies();
}

// --- key modal ---
enterKeyBtn.onclick = () => keyModal.showModal();
unlockBtn.onclick = async () => {
  const key = proKeyInput.value.trim();
  if (!key) return toast("Enter a key");
  const r = await fetch("/api/verify-pro", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ key })
  });
  const j = await r.json();
  if (j.ok) {
    localStorage.setItem("sigil_pro","1");
    keyModal.close();
    toast("Pro unlocked");
    await renderGate();
  } else {
    toast("Invalid key");
  }
};

// --- cooldown (free only) ---
function startCooldownIfNeeded() {
  isUserPro().then(pro => { // Use isUserPro
    if (pro) return;
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
  const pro = await isUserPro();
  if (pro) return;
  ctx.globalAlpha = 0.6;
  ctx.fillStyle = "#ffffff";
  ctx.font = `${Math.max(14, Math.floor(canvas.width * 0.04))}px monospace`;
  const text = "Sigilcraft";
  const m = ctx.measureText(text);
  ctx.fillText(text, canvas.width - m.width - 16, canvas.height - 16);
  ctx.globalAlpha = 1;
}

// Generate sigil using backend with retry logic
async function renderSigil(phrase = "default", vibe = "mystical", retryCount = 0) {
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
        throw new Error(`Server error (${response.status}). Please try again.`);
      }
    }

    const data = await response.json();
    console.log("Received response:", data.success ? "Success" : "Failed", data.error || "");

    if (data.success && data.image) {
      lastGeneratedImage = data.image; // Store for download
      console.log("Stored image for download, length:", data.image.length);

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
        toast("Failed to display generated image");
      };
      img.src = data.image;
      return data;
    } else {
      throw new Error(data.error || "Generation failed - no image data received");
    }
  } catch (error) {
    console.error("Sigil generation error:", error);

    // Retry logic for network errors or timeouts
    if (retryCount < maxRetries && (
      error.name === 'AbortError' || 
      error.message.includes('Failed to fetch') ||
      error.message.includes('temporarily unavailable') ||
      error.message.includes('NetworkError') || // Common for fetch issues
      error.message.includes('timeout')
    )) {
      console.log(`Retrying generation (attempt ${retryCount + 1}/${maxRetries})... Delay: ${retryDelay}ms`);
      await new Promise(resolve => setTimeout(resolve, retryDelay)); // Use progressive delay
      return renderSigil(phrase, vibe, retryCount + 1);
    }

    throw error; // Re-throw if not a retryable error or max retries reached
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
        toast("JSZip library not loaded");
        return;
      }

      const zip = new JSZip();
      for (let i = 0; i < 5; i++){
        const batchPhrase = `${phrase} variant ${i + 1}`;
        const data = await renderSigil(batchPhrase, vibe);
        if (data && data.image) {
          const base64Data = data.image.split(",")[1];
          zip.file(`sigil_${i+1}.png`, base64Data, {base64: true});
        }
      }
      const blob = await zip.generateAsync({type:"blob"});
      triggerDownload(blob, "sigils.zip");
      toast("✨ Batch sigils ready for download!", 'success', 4000);
    } else {
      // single
      await renderSigil(phrase, vibe);
      toast("✨ Quantum sigil generated successfully!", 'success', 3000);
    }
  } catch (error) {
    console.error("Generation process error:", error);
    toast(`❌ Generation failed: ${error.message}`, 'error', 5000);
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
    showLoading("Preparing download...");

    const isPro = await isUserPro(); // Use isUserPro
    const seed = Number(seedInput.value) || 0;

    // Check if we have a current sigil to download
    if (!lastGeneratedImage) {
      console.log("No image available for download");
      toast("⚠️ Generate a sigil first to download", 'warning');
      return;
    }

    console.log("Image available for download, size:", lastGeneratedImage.length);

    if (isPro && exportType.value === "svg") {
      console.log("Downloading as SVG");
      const svg = buildSvg(seed, 2048);
      const blob = new Blob([svg], {type:"image/svg+xml"});

      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
      const filename = `quantum_sigil_${timestamp}.svg`;

      await downloadBlob(blob, filename);
      toast("✨ SVG sigil downloaded!", 'success');

    } else {
      console.log("Downloading as PNG");

      // Validate image data format
      if (!lastGeneratedImage.startsWith('data:image/png;base64,') && !lastGeneratedImage.startsWith('data:image/png;')) {
        console.error("Invalid image data format:", lastGeneratedImage.substring(0, 50));
        toast("❌ Invalid image format detected", 'error');
        return;
      }

      try {
        // Convert data URL to blob
        const blob = await dataURLToBlobAsync(lastGeneratedImage);

        if (!blob || blob.size === 0) {
          throw new Error("Failed to create download blob");
        }

        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
        const filename = `quantum_sigil_${timestamp}.png`;

        console.log("Created blob for download:", {
          filename,
          size: blob.size,
          type: blob.type
        });

        await downloadBlob(blob, filename);
        toast("✨ Quantum Sigil downloaded successfully!", 'success');

      } catch (blobError) {
        console.error("Blob creation failed:", blobError);

        // Fallback: try canvas download
        try {
          console.log("Attempting canvas fallback...");

          if (!canvas || canvas.width === 0 || canvas.height === 0) {
            throw new Error("Canvas not available or invalid");
          }

          const canvasBlob = await new Promise((resolve, reject) => {
            canvas.toBlob((blob) => {
              if (blob) {
                resolve(blob);
              } else {
                reject(new Error("Canvas toBlob returned null"));
              }
            }, 'image/png', 1.0);
          });

          const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
          const filename = `quantum_sigil_canvas_${timestamp}.png`;

          await downloadBlob(canvasBlob, filename);
          toast("✨ Sigil downloaded via canvas backup!", 'success');

        } catch (canvasError) {
          console.error("Canvas fallback failed:", canvasError);
          toast("❌ Download failed - please regenerate the sigil and try again", 'error', 6000);
        }
      }
    }

  } catch (error) {
    console.error("Download error:", error);
    toast(`❌ Download failed: ${error.message}`, 'error', 5000);
  } finally {
    hideLoading();
  }
};

// Enhanced blob conversion with better error handling
async function dataURLToBlobAsync(dataURL) {
  return new Promise((resolve, reject) => {
    try {
      const arr = dataURL.split(',');
      if (arr.length !== 2) {
        throw new Error("Invalid data URL format");
      }

      const mimeMatch = arr[0].match(/:(.*?);/);
      if (!mimeMatch) {
        throw new Error("Invalid MIME type in data URL");
      }

      const mime = mimeMatch[1];
      const bstr = atob(arr[1]);
      let n = bstr.length;
      const u8 = new Uint8Array(n);

      while(n--) {
        u8[n] = bstr.charCodeAt(n);
      }

      const blob = new Blob([u8], {type: mime});
      resolve(blob);

    } catch (error) {
      reject(new Error(`Data URL conversion failed: ${error.message}`));
    }
  });
}

// Enhanced download function with better error handling
async function downloadBlob(blob, filename) {
  return new Promise((resolve, reject) => {
    try {
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');

      link.href = url;
      link.download = filename;
      link.style.display = 'none';

      // Handle download completion
      link.addEventListener('click', () => {
        setTimeout(() => {
          URL.revokeObjectURL(url);
          document.body.removeChild(link);
          resolve();
        }, 100);
      });

      // Handle download errors
      link.addEventListener('error', (event) => {
        URL.revokeObjectURL(url);
        document.body.removeChild(link);
        reject(new Error('Download link failed'));
      });

      document.body.appendChild(link);
      link.click();

    } catch (error) {
      reject(new Error(`Download setup failed: ${error.message}`));
    }
  });
}

// Legacy download function for batch downloads
function triggerDownload(blob, filename) {
  try {
    console.log("Triggering download:", filename, "blob size:", blob.size);
    const a = document.createElement("a");
    const url = URL.createObjectURL(blob);
    a.href = url;
    a.download = filename;
    document.body.appendChild(a); // Add to DOM for Firefox compatibility
    a.click();
    document.body.removeChild(a); // Remove from DOM

    // Clean up after a delay to ensure download starts
    setTimeout(() => {
      URL.revokeObjectURL(url);
    }, 1000);

    console.log("Download triggered successfully");
  } catch (error) {
    console.error("Download failed:", error);
    toast("Download failed: " + error.message);
  }
}

// Legacy blob conversion (kept for batch functionality)
function dataURLtoBlob(dataURL){
  const arr = dataURL.split(","), mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]); let n = bstr.length; const u8 = new Uint8Array(n);
  while(n--) u8[n] = bstr.charCodeAt(n);
  return new Blob([u8], {type:mime});
}

// ---- downloadPNG function ----
function downloadPNG() {
  if (!lastGeneratedImage) {
    toast("No image to download");
    return;
  }

  try {
    console.log("Image available for download, size:", lastGeneratedImage.length);
    console.log("Downloading as PNG");

    // More robust base64 to blob conversion
    const response = lastGeneratedImage.startsWith('data:') ? lastGeneratedImage : `data:image/png;base64,${lastGeneratedImage}`;

    fetch(response)
      .then(res => res.blob())
      .then(blob => {
        const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
        const filename = `quantum_sigil_${timestamp}.png`;

        console.log("Triggering download:", filename, "blob size:", blob.size);
        triggerDownload(blob, filename);
        toast("Downloaded PNG");
      })
      .catch(error => {
        console.error("PNG download error:", error);

        // Fallback method
        try {
          const base64Data = lastGeneratedImage.includes(',') ? lastGeneratedImage.split(",")[1] : lastGeneratedImage;
          const byteCharacters = atob(base64Data);
          const byteNumbers = new Array(byteCharacters.length);
          for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
          }
          const byteArray = new Uint8Array(byteNumbers);
          const blob = new Blob([byteArray], { type: "image/png" });

          const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
          const filename = `quantum_sigil_${timestamp}.png`;

          triggerDownload(blob, filename);
          toast("Downloaded PNG (fallback method)");
        } catch (fallbackError) {
          console.error("Fallback download failed:", fallbackError);
          toast("Download failed - please try again");
        }
      });
  } catch (error) {
    console.error("PNG download error:", error);
    toast("Download failed");
  }
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
  await renderGate();

  // Check for purchase success/cancel
  const p = new URLSearchParams(location.search);
  if (p.get("purchase") === "success") {
    toast("Chur! Payment successful. Check your email for your Pro key.");
  } else if (p.get("purchase") === "cancel") {
    toast("Purchase cancelled.");
  }
});

// keep previewSvg hidden unless you want to show the SVG string; we use direct download instead.