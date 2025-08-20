
import express from "express";
import cookieParser from "cookie-parser";
import Stripe from "stripe";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import fetch from "node-fetch";
import dotenv from "dotenv";
import compression from "compression";
import helmet from "helmet";
import rateLimit from "express-rate-limit";

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

// Security headers
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      imgSrc: ["'self'", "data:", "blob:"],
      scriptSrc: ["'self'", "'unsafe-inline'", "https://js.stripe.com"],
      connectSrc: ["'self'", "https://api.stripe.com"],
      frameSrc: ["'self'", "https://js.stripe.com", "https://hooks.stripe.com"]
    }
  }
}));

// Compression
app.use(compression({
  filter: (req, res) => {
    if (req.headers['x-no-compression']) return false;
    return compression.filter(req, res);
  },
  threshold: 0
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: { error: "Too many requests, please try again later." },
  standardHeaders: true,
  legacyHeaders: false
});

app.use('/api', limiter);

app.use(cookieParser());

// -------- Stripe --------
const stripe = new Stripe(process.env.STRIPE_SECRET);

// Keep raw body ONLY for the webhook route (Stripe needs it)
app.post("/api/stripe-webhook",
  express.raw({ type: "application/json" }),
  async (req, res) => {
    const sig = req.headers["stripe-signature"];
    let event;
    try {
      event = stripe.webhooks.constructEvent(
        req.body,
        sig,
        process.env.STRIPE_WEBHOOK_SECRET
      );
    } catch (err) {
      console.error("Webhook signature verify failed:", err.message);
      return res.status(400).send(`Webhook Error: ${err.message}`);
    }

    try {
      if (event.type === "checkout.session.completed") {
        const session = event.data.object;
        const email = session.customer_details?.email || "unknown@unknown";
        const key = makeKey();
        addKey({ key, email, ts: Date.now(), used: false });

        // Try emailing via Resend or SMTP; fallback to console log
        const emailed = await tryEmailKey(email, key);
        console.log("Provisioned key:", key, "for", email, "emailed:", emailed);
      }
      res.json({ received: true });
    } catch (e) {
      console.error("Webhook handler error:", e);
      res.status(500).end();
    }
  }
);

// After webhook, enable JSON for the rest
app.use(express.json());

// -------- Static with caching
app.use(express.static(path.join(__dirname, "public"), {
  setHeaders: (res, p) => {
    if (p.endsWith(".svg")) res.setHeader("Content-Type", "image/svg+xml");
    
    // Cache static assets for 1 hour
    if (p.endsWith('.css') || p.endsWith('.js') || p.endsWith('.png') || 
        p.endsWith('.jpg') || p.endsWith('.svg') || p.endsWith('.ico')) {
      res.setHeader('Cache-Control', 'public, max-age=3600');
    } else {
      // HTML files - no cache for dynamic content
      res.setHeader('Cache-Control', 'no-cache, must-revalidate');
    }
  },
  maxAge: '1h'
}));

// -------- Simple key store (JSON file)
const KEYS_FILE = path.join(__dirname, "keys.json");
function loadKeys() {
  try { return JSON.parse(fs.readFileSync(KEYS_FILE, "utf8")); }
  catch { return []; }
}
function saveKeys(list) { fs.writeFileSync(KEYS_FILE, JSON.stringify(list, null, 2)); }
function addKey(entry) { const list = loadKeys(); list.push(entry); saveKeys(list); }
function hasKey(k) { return !!loadKeys().find(x => x.key === k); }
function makeKey() {
  return [...crypto.getRandomValues(new Uint8Array(24))]
    .map(b => b.toString(16).padStart(2, "0")).join("");
}

// -------- Email helpers
async function tryEmailKey(to, key) {
  // Prefer Resend (super simple). Set RESEND_API_KEY to enable.
  if (process.env.RESEND_API_KEY) {
    try {
      const r = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${process.env.RESEND_API_KEY}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          from: "TohungaTech <noreply@tohungatech.com>",
          to: [to],
          subject: "Your Sigilcraft Pro Key",
          html: `<p>Kia ora! Thanks for your purchase.</p>
                 <p>Your Pro key: <b style="font-family:monospace">${key}</b></p>
                 <p>Open Sigilcraft → Enter Pro Key to unlock.</p>`
        })
      });
      return r.ok;
    } catch { /* fall through */ }
  }
  // TODO: add SMTP (nodemailer) if you prefer; omitted to keep this minimal.
  console.log(`Email disabled. Manual send to ${to}: KEY=${key}`);
  return false;
}

// -------- Checkout session route (frontend calls this)
app.post("/api/create-checkout-session", async (req, res) => {
  try {
    const session = await stripe.checkout.sessions.create({
      mode: "payment",
      line_items: [{ price: process.env.PRICE_ID, quantity: 1 }],
      success_url: `${req.protocol}://${req.get("host")}/?purchase=success`,
      cancel_url: `${req.protocol}://${req.get("host")}/?purchase=cancel`,
      customer_creation: "if_required",
      allow_promotion_codes: true
    });
    res.status(200).json({ url: session.url });
  } catch (err) {
    console.error("Stripe session error:", err);
    res.status(500).json({ error: "checkout_session_failed" });
  }
});

// -------- Pro check & verify
app.get("/api/is-pro", (req, res) => {
  const pro = req.cookies && req.cookies.sigil_pro === "1";
  console.log("Pro status check:", pro, "Cookies:", req.cookies);
  res.json({ pro });
});

app.post("/api/verify-pro", (req, res) => {
  try {
    const { key } = req.body;
    console.log(`Pro key verification: received="${key}", expected="${process.env.PRO_KEY}"`);
    const ok = 
      (key && process.env.PRO_KEY && key === process.env.PRO_KEY) ||
      (key && hasKey(key));
    if (ok) {
      console.log("Pro key verified successfully");
      res.cookie("sigil_pro", "1", {
        httpOnly: true,
        sameSite: "lax",
        maxAge: 1000 * 60 * 60 * 24 * 365
      });
      // Optionally mark as used:
      const list = loadKeys();
      const idx = list.findIndex(x => x.key === key);
      if (idx >= 0) { list[idx].used = true; saveKeys(list); }
      return res.json({ ok: true });
    }
    console.log("Pro key verification failed");
    return res.json({ ok: false });
  } catch (error) {
    console.log("Pro key verification error:", error);
    return res.json({ ok: false });
  }
});

// Test endpoint for debugging
app.get("/api/test", (req, res) => {
  res.json({ 
    status: "ok", 
    port: PORT,
    proKey: process.env.PRO_KEY ? "configured" : "missing",
    timestamp: new Date().toISOString()
  });
});

// Proxy sigil generation requests to Python Flask backend
app.post("/generate", async (req, res) => {
  try {
    const response = await fetch("http://localhost:5001/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body)
    });
    const data = await response.json();
    res.json(data);
  } catch (error) {
    res.status(500).json({ success: false, error: "Sigil generation service unavailable" });
  }
});

// -------- Fallback
app.get("*", (_, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Sigilcraft Node server running on http://0.0.0.0:${PORT}`);
  console.log(`Pro key configured: ${process.env.PRO_KEY ? 'Yes' : 'No'}`);
  console.log(`Stripe configured: ${process.env.STRIPE_SECRET ? 'Yes' : 'No'}`);
});
