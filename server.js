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
import { webcrypto } from 'crypto';
import crypto from 'crypto';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

// Trust proxy for proper IP detection in Replit
app.set('trust proxy', 1);

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "blob:"],
      connectSrc: ["'self'", "https://api.stripe.com"]
    }
  }
}));

// Compression middleware
app.use(compression());

// Rate limiting with proper IP detection
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: { error: "Too many requests, please try again later." },
  standardHeaders: true,
  legacyHeaders: false,
  trustProxy: true
});

app.use('/api', limiter);

// Stricter rate limiting for generation endpoints
const generationLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10, // limit each IP to 10 generations per minute
  message: { error: "Generation rate limit exceeded. Please wait before trying again." },
  trustProxy: true
});

// CORS and additional headers
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
  res.header('X-Content-Type-Options', 'nosniff');
  res.header('X-Frame-Options', 'DENY');
  res.header('X-XSS-Protection', '1; mode=block');
  
  if (req.method === 'OPTIONS') {
    res.sendStatus(200);
  } else {
    next();
  }
});

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
  return crypto.randomBytes(24).toString('hex');
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

// Health check endpoint
app.get("/api/health", async (req, res) => {
  try {
    // Check Flask backend health with proper timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);
    
    // Try multiple Flask ports
    let flaskHealthy = false;
    for (const port of [5001, 5002, 5003, 5004, 5005]) {
      try {
        const flaskResponse = await fetch(`http://127.0.0.1:${port}/health`, { 
          signal: controller.signal 
        });
        if (flaskResponse.ok) {
          flaskHealthy = true;
          break;
        }
      } catch (e) {
        continue;
      }
    }
    clearTimeout(timeoutId);
    
    clearTimeout(timeoutId);
    
    res.json({
      status: "healthy",
      services: {
        node: "online",
        flask: flaskHealthy ? "online" : "offline"
      },
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error("Health check error:", error.message);
    res.status(503).json({
      status: "degraded",
      services: {
        node: "online",
        flask: "offline"
      },
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Proxy sigil generation requests to Python Flask backend
app.post("/generate", generationLimiter, async (req, res) => {
  let timeoutId = null;
  let controller = null;
  
  try {
    console.log("Proxying generation request to Flask backend...");

    controller = new AbortController();
    const isComplexRequest = req.body.vibe && req.body.vibe.includes('+');
    const timeoutDuration = isComplexRequest ? 30000 : 20000; // Much shorter timeouts for faster response
    
    timeoutId = setTimeout(() => {
      console.log("Request timeout reached, aborting...");
      if (controller) {
        controller.abort();
      }
    }, timeoutDuration);

    // Try multiple Flask ports for generation
    let response = null;
    let lastError = null;
    
    for (const port of [5001, 5002, 5003, 5004, 5005]) {
      try {
        if (controller.signal.aborted) {
          throw new Error('Request was aborted due to timeout');
        }

        response = await fetch(`http://127.0.0.1:${port}/generate`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Sigilcraft-Proxy/1.0",
            "Connection": "keep-alive"
          },
          body: JSON.stringify(req.body),
          signal: controller.signal
        }).catch(fetchError => {
          // Wrap fetch errors to prevent unhandled rejections
          if (fetchError.name === 'AbortError') {
            const wrappedError = new Error('Request timed out');
            wrappedError.name = 'TimeoutError';
            throw wrappedError;
          }
          throw fetchError;
        });
        
        if (response && response.ok) {
          console.log(`Successfully connected to Flask on port ${port}`);
          break;
        }
      } catch (error) {
        if (error.name === 'AbortError' || error.name === 'TimeoutError') {
          lastError = new Error('Request timed out');
          lastError.name = 'TimeoutError';
          break; // Don't try other ports if we timed out
        } else {
          console.log(`Port ${port} failed: ${error.message}`);
          lastError = error;
          continue;
        }
      }
    }
    
    // Clean up timeout
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutId = null;
    }
    
    // Check if we were aborted
    if (controller && controller.signal.aborted) {
      console.log("Request was aborted due to timeout");
      return res.status(408).json({
        success: false,
        error: "Generation timed out. Please try a simpler phrase or try again."
      });
    }
    
    if (!response) {
      throw lastError || new Error("Flask backend not available on any port");
    }

    if (!response.ok) {
      const errorText = await response.text().catch(() => 'Unknown error');
      throw new Error(`Flask backend returned ${response.status}: ${errorText}`);
    }

    const data = await response.json();
    console.log("Successfully proxied generation request");
    res.json(data);

  } catch (error) {
    // Always clean up timeout
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutId = null;
    }
    
    console.error("Flask backend proxy error:", error.message);

    // Handle timeout/abort errors specifically to prevent server crashes
    if (error.name === 'AbortError' || error.name === 'TimeoutError' || error.message.includes('timeout')) {
      console.log("Request timed out or was aborted");
      return res.status(408).json({
        success: false,
        error: "Generation timed out. Please try a simpler phrase or try again."
      });
    }
    
    if (error.message.includes('ECONNREFUSED') || error.code === 'ECONNREFUSED') {
      return res.status(503).json({
        success: false,
        error: "Sigil generation service is starting up. Please try again in a moment."
      });
    }
    
    if (error.message.includes('fetch')) {
      return res.status(503).json({
        success: false,
        error: "Network error connecting to generation service. Please try again."
      });
    }
    
    return res.status(500).json({
      success: false,
      error: "Sigil generation temporarily unavailable. Please try again."
    });
  }
});

// -------- Fallback
app.get("*", (_, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// Global error handlers to prevent server crashes
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // Don't exit the process - just log the error
});

process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  // Don't exit the process - just log the error
});

const PORT = process.env.PORT || 5000;

// Function to find available port if default is in use
function startServer(port) {
  const server = app.listen(port, "0.0.0.0", () => {
    console.log(`Sigilcraft Node server running on http://0.0.0.0:${port}`);
    console.log(`Pro key configured: ${process.env.PRO_KEY ? 'Yes' : 'No'}`);
    console.log(`Stripe configured: ${process.env.STRIPE_SECRET ? 'Yes' : 'No'}`);
  });

  server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
      console.log(`Port ${port} is in use, trying port ${port + 1}...`);
      setTimeout(() => {
        server.close();
        if (port < 5010) {
          startServer(port + 1);
        } else {
          console.error('Could not find available port after trying 5000-5010');
          process.exit(1);
        }
      }, 1000);
    } else {
      console.error('Server error:', err);
      process.exit(1);
    }
  });

  return server;
}

startServer(PORT);