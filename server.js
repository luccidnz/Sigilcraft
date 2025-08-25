
import express from 'express';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import compression from 'compression';
import helmet from 'helmet';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import fetch from 'node-fetch';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 5000;
const FLASK_URL = process.env.FLASK_URL || 'http://localhost:5001';

// ===== SECURITY & PERFORMANCE =====
app.use(helmet({
  contentSecurityPolicy: false,
  crossOriginEmbedderPolicy: false
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: {
    error: 'Too many requests from this IP, please try again later.',
    retryAfter: 15 * 60 * 1000
  }
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

// Sigil generation endpoint (proxy to Flask backend)
app.post('/api/generate', generateLimiter, async (req, res) => {
  const startTime = Date.now();
  const requestId = Math.random().toString(36).substring(7);
  
  try {
    const { phrase, vibe, advanced } = req.body;

    // Validation
    if (!phrase || typeof phrase !== 'string' || phrase.trim().length === 0) {
      return res.status(400).json({
        success: false,
        error: 'Phrase is required and must be a non-empty string'
      });
    }

    const cleanPhrase = phrase.trim();
    if (cleanPhrase.length < 2) {
      return res.status(400).json({
        success: false,
        error: 'Phrase must be at least 2 characters long'
      });
    }

    if (cleanPhrase.length > 500) {
      return res.status(400).json({
        success: false,
        error: 'Phrase is too long (max 500 characters)'
      });
    }

    const validVibes = ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light', 'storm', 'void'];
    const selectedVibe = validVibes.includes(vibe) ? vibe : 'mystical';

    console.log(`🎨 [${requestId}] Generating sigil: "${cleanPhrase}" (${selectedVibe}) [Advanced: ${advanced}]`);

    // Create abort controller for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

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

    if (error.message.includes('ECONNREFUSED') || error.message.includes('fetch failed')) {
      return res.status(503).json({
        success: false,
        error: 'Backend service unavailable - please try again',
        code: 'SERVICE_UNAVAILABLE'
      });
    }

    res.status(500).json({
      success: false,
      error: 'Internal server error',
      code: 'INTERNAL_ERROR',
      requestId
    });
  }
});

// Available vibes endpoint
app.get('/api/vibes', async (req, res) => {
  try {
    const response = await fetch(`${FLASK_URL}/vibes`);
    
    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }
    
    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error('Error fetching vibes:', error);
    
    // Fallback response if backend is unavailable
    res.json({
      success: true,
      vibes: ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light', 'storm', 'void'],
      descriptions: {
        'mystical': 'Ancient wisdom & sacred geometry with curved flowing energy',
        'cosmic': 'Universal stellar connection with radiant burst patterns',
        'elemental': 'Natural organic forces with flowing growth patterns',
        'crystal': 'Prismatic clarity with angular geometric precision',
        'shadow': 'Hidden mysterious power with jagged consuming energy',
        'light': 'Pure divine radiance with emanating luminous patterns',
        'storm': 'Raw electric chaos with explosive lightning energy',
        'void': 'Infinite recursive potential with impossible geometry'
      }
    });
  }
});

// Catch all route - serve index.html for client-side routing
app.get('*', (req, res) => {
  res.sendFile(join(__dirname, 'public', 'index.html'));
});

// ===== ERROR HANDLERS =====
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    success: false,
    error: 'Internal server error',
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
