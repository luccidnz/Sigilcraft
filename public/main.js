
// ---- simple state ----
const FREE_ENERGIES = ["Mystical","Elemental","Light"];
const ALL_ENERGIES  = ["Mystical","Ethereal","Cosmic","Elemental","Crystal","Shadow","Light"]; // adjust names to your list
let selectedEnergies = [FREE_ENERGIES[0]];
let lastGenAt = 0;

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
async function isPro() {
  return (await serverIsPro()) || localIsPro();
}

// --- ui toast ---
let toastTimer;
function toast(msg) {
  toastEl.textContent = msg;
  toastEl.style.display = "block";
  clearTimeout(toastTimer);
  toastTimer = setTimeout(()=> toastEl.style.display = "none", 2500);
}

// --- energy grid ---
async function renderEnergies() {
  const pro = await isPro();
  const allowed = pro ? ALL_ENERGIES : FREE_ENERGIES;
  energyList.innerHTML = "";
  ALL_ENERGIES.forEach(name => {
    const div = document.createElement("div");
    div.className = "energy" + (allowed.includes(name) ? "" : " locked");
    div.textContent = name;
    div.onclick = () => {
      if (!allowed.includes(name)) { toast("Pro feature"); return; }
      if (!comboToggle.checked) selectedEnergies = [name];
      else {
        if (selectedEnergies.includes(name)) {
          selectedEnergies = selectedEnergies.filter(e => e !== name);
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
  const pro = await isPro();
  proBadge.classList.toggle("hidden", !pro);
  proControls.classList.toggle("hidden", !pro);
  exportType.value = "png";
  if (pro) {
    canvas.width = 2048; canvas.height = 2048;
  } else {
    canvas.width = 512; canvas.height = 512;
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
  serverIsPro().then(pro => {
    if (pro || localIsPro()) return;
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
function drawWatermarkIfFree() {
  if (localIsPro()) return;
  ctx.globalAlpha = 0.6;
  ctx.fillStyle = "#ffffff";
  ctx.font = `${Math.max(14, Math.floor(canvas.width * 0.04))}px monospace`;
  const text = "Sigilcraft";
  const m = ctx.measureText(text);
  ctx.fillText(text, canvas.width - m.width - 16, canvas.height - 16);
  ctx.globalAlpha = 1;
}

// TODO: Replace this placeholder geometry with YOUR existing sigil-generation logic.
// Respect: selectedEnergies, seedInput.value, canvas size.
function renderSigil(seed = 0) {
  clearCanvas();
  // simple seeded lines demo:
  const r = mulberry32(seed || 1);
  const n = 120;
  ctx.strokeStyle = "#9ad0ff"; ctx.lineWidth = Math.max(2, canvas.width * 0.004);
  ctx.beginPath();
  for (let i=0;i<n;i++){
    const x = canvas.width  * r();
    const y = canvas.height * r();
    i===0 ? ctx.moveTo(x,y) : ctx.lineTo(x,y);
  }
  ctx.stroke();
  drawWatermarkIfFree();
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
genBtn.onclick = async () => {
  const pro = await isPro();
  const seed = Number(seedInput.value) || 0;
  const size = pro ? 2048 : 512;

  canvas.width = size; canvas.height = size;

  if (pro && batchToggle.checked) {
    // batch create zip of 5
    const zip = new JSZip();
    for (let i=0;i<5;i++){
      const s = seed ? seed + i : Math.floor(Math.random()*1e9);
      if (exportType.value === "svg") {
        const svg = buildSvg(s, size);
        zip.file(`sigil_${i+1}.svg`, svg);
      } else {
        renderSigil(s);
        const png = canvas.toDataURL("image/png").split(",")[1];
        zip.file(`sigil_${i+1}.png`, png, {base64:true});
      }
    }
    const blob = await zip.generateAsync({type:"blob"});
    triggerDownload(blob, "sigils.zip");
    toast("Batch ready");
  } else {
    // single
    renderSigil(seed);
    toast("Sigil generated");
  }

  startCooldownIfNeeded();
};

downloadBtn.onclick = async () => {
  const pro = await isPro();
  const seed = Number(seedInput.value) || 0;
  if (pro && exportType.value === "svg") {
    const svg = buildSvg(seed, 2048);
    const blob = new Blob([svg], {type:"image/svg+xml"});
    triggerDownload(blob, "sigil.svg");
  } else {
    const url = canvas.toDataURL("image/png");
    triggerDownload(dataURLtoBlob(url), "sigil.png");
  }
};

function triggerDownload(blobOrUrl, filename){
  const blob = typeof blobOrUrl === "string" ? dataURLtoBlob(blobOrUrl) : blobOrUrl;
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = filename; a.click();
  URL.revokeObjectURL(url);
}

function dataURLtoBlob(dataURL){
  const arr = dataURL.split(","), mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]); let n = bstr.length; const u8 = new Uint8Array(n);
  while(n--) u8[n] = bstr.charCodeAt(n);
  return new Blob([u8], {type:mime});
}

// init
window.addEventListener("load", async () => {
  await renderGate();
});

// keep previewSvg hidden unless you want to show the SVG string; we use direct download instead.
