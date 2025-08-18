
import express from "express";
import cookieParser from "cookie-parser";
import path from "path";
import { fileURLToPath } from "url";
import fetch from "node-fetch";
import dotenv from "dotenv";

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(express.json());
app.use(cookieParser());

// static
app.use(express.static(path.join(__dirname, "public"), {
  setHeaders: (res, p) => {
    if (p.endsWith(".svg")) res.setHeader("Content-Type", "image/svg+xml");
  }
}));

// verify-pro: compare against env var
app.post("/api/verify-pro", (req, res) => {
  try {
    const { key } = req.body;
    console.log(`Pro key verification: received="${key}", expected="${process.env.PRO_KEY}"`);
    const ok = key && process.env.PRO_KEY && key === process.env.PRO_KEY;
    if (ok) {
      console.log("Pro key verified successfully");
      res.cookie("sigil_pro", "1", {
        httpOnly: true,
        sameSite: "lax",
        maxAge: 1000 * 60 * 60 * 24 * 365
      });
      return res.json({ ok: true });
    }
    console.log("Pro key verification failed");
    return res.json({ ok: false });
  } catch (error) {
    console.log("Pro key verification error:", error);
    return res.json({ ok: false });
  }
});

// is-pro: read cookie
app.get("/api/is-pro", (req, res) => {
  const pro = req.cookies && req.cookies.sigil_pro === "1";
  console.log("Pro status check:", pro, "Cookies:", req.cookies);
  res.json({ pro });
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

// fallback to index
app.get("*", (_, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

const PORT = process.env.PORT || 5000;

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

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Sigilcraft Node server running on http://0.0.0.0:${PORT}`);
  console.log(`Pro key configured: ${process.env.PRO_KEY ? 'Yes' : 'No'}`);
});
