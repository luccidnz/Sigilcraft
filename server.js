
import express from "express";
import cookieParser from "cookie-parser";
import path from "path";
import { fileURLToPath } from "url";
import fetch from "node-fetch";

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
  let body = "";
  req.on("data", chunk => body += chunk);
  req.on("end", () => {
    try {
      const { key } = JSON.parse(body || "{}");
      const ok = key && process.env.PRO_KEY && key === process.env.PRO_KEY;
      if (ok) {
        res.cookie("sigil_pro", "1", {
          httpOnly: true,
          sameSite: "lax",
          maxAge: 1000 * 60 * 60 * 24 * 365
        });
        return res.json({ ok: true });
      }
      return res.json({ ok: false });
    } catch {
      return res.json({ ok: false });
    }
  });
});

// is-pro: read cookie
app.get("/api/is-pro", (req, res) => {
  const pro = req.cookies && req.cookies.sigil_pro === "1";
  res.json({ pro });
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

app.listen(PORT, "0.0.0.0", () => console.log("Sigilcraft running on", PORT));
