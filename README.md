
# Sigilcraft – Free vs Pro

## Run
1. Copy `.env.sample` to `.env` and set `PRO_KEY=your_secret_key`.
2. `npm install`
3. `npm start`

Open the repl and click "Open in Browser".

## Monetisation
- "Upgrade to Pro" links to Stripe Checkout (replace placeholder).
- After purchase, send the buyer their **Pro Key**. They paste it via "Enter Pro Key".
- Server sets an httpOnly cookie; client also stores a local flag.

## Free vs Pro
- **Free**: 3 energies, PNG 512px, watermark, 10s cooldown
- **Pro**: all energies + combo, PNG 2048px + SVG, batch x5, seed, no watermark/cooldown
