
const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const app = express();

app.use(express.json());
app.use(cookieParser());
app.use(express.static('.'));

// Serve the main HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'index.html'));
});

// Pro verification endpoint
app.post('/api/verify-pro', (req, res) => {
    const { key } = req.body;
    
    if (key === process.env.PRO_KEY) {
        res.cookie('sigil_pro', '1', { 
            httpOnly: true, 
            sameSite: 'Lax',
            maxAge: 30 * 24 * 60 * 60 * 1000 // 30 days
        });
        res.json({ ok: true });
    } else {
        res.json({ ok: false });
    }
});

// Check pro status endpoint
app.get('/api/is-pro', (req, res) => {
    const isPro = req.cookies.sigil_pro === '1';
    res.json({ pro: isPro });
});

// Health check
app.get('/test', (req, res) => {
    res.json({ status: 'ok' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Sigil Generator Pro server running on port ${PORT}`);
});
