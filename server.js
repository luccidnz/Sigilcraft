
const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;
const FLASK_URL = process.env.FLASK_URL || 'http://localhost:5001';
const PRO_KEY = process.env.PRO_KEY || 'changeme_super_secret';

console.log('🚀 Starting Sigilcraft Node.js server...');
console.log('🔧 Server configuration:');
console.log(`- Port: ${PORT}`);
console.log(`- Pro Key: ${PRO_KEY ? 'SET' : 'NOT SET'}`);

// Middleware
app.use(cors({
  origin: ['http://localhost:5000', 'http://0.0.0.0:5000'],
  credentials: true
}));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

console.log('📁 Setting up static file middleware...');
app.use(express.static('public'));
console.log('✅ Static file middleware configured');

// Health check endpoint
app.get('/health', (req, res) => {
  console.log(`🔌 [API] GET /health from ${req.ip}`);
  res.json({ 
    status: 'healthy', 
    server: 'node',
    timestamp: new Date().toISOString(),
    pro_configured: !!PRO_KEY
  });
});

app.get('/api/health', (req, res) => {
  console.log(`🔌 [API] GET /api/health from ${req.ip}`);
  res.json({ 
    status: 'healthy', 
    server: 'node-api',
    timestamp: new Date().toISOString()
  });
});

// Pro status endpoint - FIX THE MISSING ENDPOINT
app.get('/api/pro-status', (req, res) => {
  console.log(`🔌 [API] GET /api/pro-status from ${req.ip}`);
  const providedKey = req.headers['x-pro-key'] || req.query.key;
  
  res.json({
    success: true,
    isPro: providedKey === PRO_KEY,
    serverPro: true, // Server has pro features available
    timestamp: new Date().toISOString()
  });
});

// Pro key validation endpoint
app.post('/api/validate-key', (req, res) => {
  console.log(`🔌 [API] POST /api/validate-key from ${req.ip}`);
  const { key } = req.body;
  
  const isValid = key === PRO_KEY;
  
  res.json({
    success: true,
    valid: isValid,
    message: isValid ? 'Pro key validated successfully' : 'Invalid pro key'
  });
});

// Sigil generation proxy endpoint
app.post('/api/generate', async (req, res) => {
  const startTime = Date.now();
  console.log(`🔌 [API] POST /api/generate from ${req.ip}`);
  
  try {
    const { phrase, vibe } = req.body;
    
    if (!phrase || !phrase.trim()) {
      return res.status(400).json({
        success: false,
        error: 'Phrase is required'
      });
    }

    // Forward to Flask backend
    const fetch = (await import('node-fetch')).default;
    const response = await fetch(`${FLASK_URL}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ phrase: phrase.trim(), vibe: vibe || 'mystical' }),
      timeout: 45000
    });

    if (!response.ok) {
      throw new Error(`Flask server error: ${response.status}`);
    }

    const data = await response.json();
    const duration = Date.now() - startTime;
    
    console.log(`✅ [API] Generation completed in ${duration}ms`);
    res.json(data);

  } catch (error) {
    const duration = Date.now() - startTime;
    console.error(`❌ [API] Generation failed after ${duration}ms:`, error.message);
    
    res.status(500).json({
      success: false,
      error: 'Generation service temporarily unavailable'
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
    error: 'Endpoint not found',
    path: req.path,
    available_endpoints: ['/health', '/api/health', '/api/pro-status', '/api/validate-key', '/api/generate']
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  res.status(500).json({ 
    success: false, 
    error: 'Internal server error' 
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Sigilcraft Node server running on http://0.0.0.0:${PORT}`);
  console.log(`Pro key configured: ${PRO_KEY ? 'Yes' : 'No'}`);
});

module.exports = app;
