import express from 'express';

const app = express();
app.use(express.json());

app.get('/api/status', (_req, res) => {
  res.json({
    status: 'ok',
    service: 'sigilcraft',
    backend: 'node',
  });
});

app.post('/api/auth', (req, res) => {
  const body = req.body as { name?: unknown } | null | undefined;
  const name = body?.name;
  if (!name || typeof name !== 'string' || name.trim().length === 0) {
    res.status(400).json({ error: 'name is required' });
    return;
  }
  res.json({
    ok: true,
    user: { name: name.trim() },
  });
});

app.post('/api/generate', (req, res) => {
  const hue = 258;
  const gold = 48;
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240">
  <rect width="240" height="240" fill="#0b1220"/>
  <path d="M120 40 L180 140 L120 200 L60 140 Z" fill="none" stroke="hsl(${hue},80%,65%)" stroke-width="2"/>
  <circle cx="120" cy="120" r="14" fill="hsl(${gold},95%,68%)"/>
</svg>`;
  res.json({
    image: `data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}`,
    metadata: {
      phrase: 'Quiet intention',
      vibe: 'mystical',
      quality: 'standard',
    },
  });
});

const port = 5000;
const host = '0.0.0.0';
app.listen(port, host, () => {
  console.log(`sigilcraft api listening on ${host}:${port}`);
});
