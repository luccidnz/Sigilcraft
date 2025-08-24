
import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 5000;
const FLASK_URL = process.env.FLASK_URL || 'http://127.0.0.1:5001';
const PRO_KEY = process.env.PRO_KEY || 'changeme_super_secret';

console.log('🚀 Starting Sigilcraft server...');
console.log(`- Port: ${PORT}`);
console.log(`- Pro Key: ${PRO_KEY ? 'SET' : 'NOT SET'}`);

// Middleware
app.use(cors({
  origin: true,
  credentials: true
}));
app.use(express.json({ limit: '10mb' }));
app.use(express.static('public'));

// Health check
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    server: 'sigilcraft',
    timestamp: new Date().toISOString()
  });
});

// Pro status endpoint
app.get('/api/pro-status', (req, res) => {
  try {
    const providedKey = req.headers['x-pro-key'] || req.query.key;
    
    // Ensure we always send JSON
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Cache-Control', 'no-cache');
    
    const response = {
      success: true,
      isPro: providedKey === PRO_KEY,
      timestamp: new Date().toISOString()
    };
    
    res.json(response);
  } catch (error) {
    console.error('Pro status error:', error);
    res.setHeader('Content-Type', 'application/json');
    res.status(500).json({
      success: false,
      error: 'Failed to check pro status',
      details: error.message
    });
  }
});

// Pro key validation
app.post('/api/validate-key', (req, res) => {
  const { key } = req.body;
  const isValid = key === PRO_KEY;
  
  res.json({
    success: true,
    valid: isValid,
    message: isValid ? 'Pro key validated' : 'Invalid pro key'
  });
});

// Sigil generation
app.post('/api/generate', async (req, res) => {
  const startTime = Date.now();
  
  try {
    const { phrase, vibe } = req.body;
    
    if (!phrase?.trim()) {
      return res.status(400).json({
        success: false,
        error: 'Phrase is required'
      });
    }

    console.log(`🎨 Generating sigil: "${phrase}" with vibe: ${vibe || 'mystical'}`);

    const response = await fetch(`${FLASK_URL}/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phrase: phrase.trim(), vibe: vibe || 'mystical' }),
      signal: AbortSignal.timeout(30000)
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Backend error ${response.status}:`, errorText);
      throw new Error(`Backend error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    const duration = Date.now() - startTime;
    
    console.log(`✅ Generation completed in ${duration}ms`);
    
    res.setHeader('Content-Type', 'application/json');
    res.json(data);

  } catch (error) {
    const duration = Date.now() - startTime;
    console.error(`❌ Generation failed after ${duration}ms:`, error);
    
    let errorMessage = 'Generation service unavailable';
    if (error.name === 'AbortError') {
      errorMessage = 'Generation timed out';
    } else if (error.code === 'ECONNREFUSED') {
      errorMessage = 'Backend service not available';
    } else if (error.message) {
      errorMessage = error.message;
    }
    
    res.setHeader('Content-Type', 'application/json');
    res.status(500).json({
      success: false,
      error: errorMessage,
      details: error.message || 'Unknown error'
    });
  }
});

// Serve main page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ 
    error: 'Not found',
    path: req.path
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Sigilcraft running on http://0.0.0.0:${PORT}`);
});
