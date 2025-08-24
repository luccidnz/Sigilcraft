
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import rateLimit from 'express-rate-limit';
import fetch from 'node-fetch';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 5000;
const FLASK_URL = process.env.FLASK_URL || 'http://localhost:5001';
const PRO_KEY = process.env.PRO_KEY || 'changeme_super_secret';

console.log('🚀 Starting Enhanced Sigilcraft Server...');
console.log(`- Environment: ${process.env.NODE_ENV || 'development'}`);
console.log(`- Port: ${PORT}`);
console.log(`- Flask Backend: ${FLASK_URL}`);
console.log(`- Pro Key: ${PRO_KEY ? 'CONFIGURED' : 'NOT SET'}`);

// ===== TRUST PROXY CONFIGURATION =====
app.set('trust proxy', true);

// ===== SECURITY MIDDLEWARE =====
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      imgSrc: ["'self'", "data:", "blob:"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      connectSrc: ["'self'"]
    }
  },
  crossOriginEmbedderPolicy: false
}));

// ===== RATE LIMITING =====
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: {
    error: 'Too many requests from this IP, please try again later.',
    retryAfter: 15 * 60 * 1000
  },
  standardHeaders: true,
  legacyHeaders: false
});

const generateLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10, // Limit generation requests
  message: {
    error: 'Too many generation requests, please slow down.',
    retryAfter: 60 * 1000
  }
});

app.use(limiter);

// ===== BASIC MIDDLEWARE =====
app.use(compression());
app.use(cors({
  origin: true,
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With']
}));

app.use(express.json({ 
  limit: '10mb',
  strict: true
}));

app.use(express.urlencoded({ 
  extended: true, 
  limit: '10mb' 
}));

// ===== LOGGING MIDDLEWARE =====
app.use((req, res, next) => {
  const start = Date.now();
  const originalSend = res.send;
  
  res.send = function(data) {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} - ${res.statusCode} (${duration}ms)`);
    originalSend.call(this, data);
  };
  
  next();
});

// ===== STATIC FILES =====
app.use(express.static(join(__dirname, 'public'), {
  maxAge: process.env.NODE_ENV === 'production' ? '1d' : '0',
  etag: true,
  lastModified: true
}));

// ===== API ROUTES =====

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    server: 'sigilcraft-enhanced',
    version: '2.0.0',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    environment: process.env.NODE_ENV || 'development'
  });
});

// Enhanced sigil generation endpoint
app.post('/api/generate', generateLimiter, async (req, res) => {
  const startTime = Date.now();
  const requestId = Math.random().toString(36).substring(7);

  try {
    const { phrase, vibe, advanced = false } = req.body;

    // Enhanced validation
    if (!phrase || typeof phrase !== 'string') {
      return res.status(400).json({
        success: false,
        error: 'Valid phrase is required',
        code: 'INVALID_PHRASE'
      });
    }

    const cleanPhrase = phrase.trim();
    if (cleanPhrase.length < 2) {
      return res.status(400).json({
        success: false,
        error: 'Phrase must be at least 2 characters long',
        code: 'PHRASE_TOO_SHORT'
      });
    }

    if (cleanPhrase.length > 500) {
      return res.status(400).json({
        success: false,
        error: 'Phrase is too long (max 500 characters)',
        code: 'PHRASE_TOO_LONG'
      });
    }

    const validVibes = ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light', 'storm', 'void'];
    const selectedVibe = validVibes.includes(vibe) ? vibe : 'mystical';

    console.log(`🎨 [${requestId}] Generating sigil: "${cleanPhrase}" (${selectedVibe})`);

    // Create abort controller for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);

    const response = await fetch(`${FLASK_URL}/generate`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'X-Request-ID': requestId
      },
      body: JSON.stringify({ 
        phrase: cleanPhrase, 
        vibe: selectedVibe,
        advanced: advanced 
      }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`❌ [${requestId}] Backend error ${response.status}:`, errorText);
      
      throw new Error(`Backend service error: ${response.status}`);
    }

    const data = await response.json();
    const duration = Date.now() - startTime;

    console.log(`✅ [${requestId}] Generation completed in ${duration}ms`);

    res.json({
      success: true,
      image: data.image,
      phrase: cleanPhrase,
      vibe: selectedVibe,
      metadata: {
        requestId,
        duration,
        advanced,
        timestamp: new Date().toISOString()
      },
      message: `Revolutionary sigil manifested for: "${cleanPhrase}"`
    });

  } catch (error) {
    const duration = Date.now() - startTime;
    console.error(`❌ [${requestId}] Generation failed (${duration}ms):`, error.message);

    if (error.name === 'AbortError') {
      return res.status(408).json({
        success: false,
        error: 'Request timeout - please try again',
        code: 'TIMEOUT'
      });
    }

    if (error.code === 'ECONNREFUSED') {
      return res.status(503).json({
        success: false,
        error: 'Backend service unavailable',
        code: 'SERVICE_UNAVAILABLE'
      });
    }

    res.status(500).json({
      success: false,
      error: 'Internal server error during generation',
      code: 'GENERATION_ERROR',
      requestId
    });
  }
});

// Pro status endpoint
app.get('/api/pro-status', (req, res) => {
  const authHeader = req.headers.authorization;
  const proKey = req.headers['x-pro-key'];
  
  let isPro = false;
  
  if (authHeader && authHeader.startsWith('Bearer ')) {
    const token = authHeader.substring(7);
    isPro = token === PRO_KEY;
  } else if (proKey) {
    isPro = proKey === PRO_KEY;
  }

  res.json({
    isPro,
    features: isPro ? {
      unlimitedGeneration: true,
      advancedEnergies: true,
      highResolution: true,
      batchGeneration: true,
      noWatermark: true
    } : {
      unlimitedGeneration: false,
      advancedEnergies: false,
      highResolution: false,
      batchGeneration: false,
      noWatermark: false
    }
  });
});

// Pro key validation endpoint
app.post('/api/validate-pro-key', (req, res) => {
  const { key } = req.body;
  
  if (!key || typeof key !== 'string') {
    return res.status(400).json({
      success: false,
      error: 'Pro key is required'
    });
  }

  const isValid = key.trim() === PRO_KEY;
  
  res.json({
    success: true,
    valid: isValid,
    message: isValid ? 'Pro key validated successfully' : 'Invalid pro key'
  });
});

// Analytics endpoint (placeholder for future implementation)
app.post('/api/analytics', (req, res) => {
  const { event, data } = req.body;
  
  // In production, you would log this to your analytics service
  console.log(`📊 Analytics Event: ${event}`, data);
  
  res.json({ success: true });
});

// ===== ERROR HANDLING =====

// 404 handler
app.use((req, res) => {
  if (req.path.startsWith('/api/')) {
    res.status(404).json({
      success: false,
      error: 'API endpoint not found',
      code: 'NOT_FOUND',
      path: req.path
    });
  } else {
    // Serve index.html for client-side routing
    res.sendFile(join(__dirname, 'public', 'index.html'));
  }
});

// Global error handler
app.use((error, req, res, next) => {
  console.error('💥 Unhandled error:', error);
  
  res.status(500).json({
    success: false,
    error: process.env.NODE_ENV === 'production' 
      ? 'Internal server error' 
      : error.message,
    code: 'INTERNAL_ERROR',
    timestamp: new Date().toISOString()
  });
});

// ===== GRACEFUL SHUTDOWN =====
const gracefulShutdown = (signal) => {
  console.log(`\n🛑 Received ${signal}. Graceful shutdown...`);
  
  process.exit(0);
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// ===== SERVER STARTUP =====
const server = app.listen(PORT, '0.0.0.0', () => {
  console.log('✅ Enhanced Sigilcraft server running successfully!');
  console.log(`🌍 Server: http://0.0.0.0:${PORT}`);
  console.log(`🎯 Health: http://0.0.0.0:${PORT}/api/health`);
  console.log('🚀 Ready to manifest revolutionary sigils!');
});

// Handle server errors
server.on('error', (error) => {
  if (error.code === 'EADDRINUSE') {
    console.error(`❌ Port ${PORT} is already in use`);
  } else {
    console.error('❌ Server error:', error);
  }
  process.exit(1);
});

export default app;
