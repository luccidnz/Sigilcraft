
# 🔮 Sigil Generator Pro

A mystical sigil generator with Free and Pro tiers featuring quantum energy manipulation and sacred geometry.

## Features

### Free Tier
- 3 energy types: Mystical, Elemental, Light
- PNG export (512x512)
- 10-second cooldown between generations
- Watermarked output

### Pro Tier
- All 6 energy types + Combo mode
- PNG export (2048x2048) and SVG export
- Batch generation (5 variants with ZIP download)
- No cooldown or watermarks
- Quantum seed control
- Pro badge display

## Setup

### Environment Variables

Create a `.env` file in your project root:

```bash
PRO_KEY=your_secret_pro_key_here
PORT=5000
```

Replace `your_secret_pro_key_here` with a secure, random string that will serve as your pro unlock key.

### Installation

```bash
npm install
npm start
```

The server will run on `http://localhost:5000` or the port specified in your environment.

### Pro Key Usage

1. Users can purchase pro access through the Stripe checkout link
2. After payment, provide them with the PRO_KEY value
3. Users enter this key in the app to unlock pro features
4. Pro status is remembered via localStorage and HTTP-only cookies

### Stripe Integration

Update the checkout URL in `templates/index.html`:
- Replace `https://buy.stripe.com/test_xyz` with your actual Stripe payment link
- Set up webhook handling for automatic pro key delivery (optional)

## API Endpoints

- `POST /api/verify-pro` - Verify pro key and set authentication cookie
- `GET /api/is-pro` - Check current pro status via cookie
- `GET /test` - Health check endpoint

## Security Notes

- Pro keys are verified server-side only
- HTTP-only cookies prevent client-side tampering
- Environment variables keep sensitive data secure
- Double verification (localStorage + server cookie) for redundancy

## File Structure

```
├── server.js              # Express server with pro verification
├── package.json           # Node.js dependencies and scripts
├── templates/
│   └── index.html         # Main application with pro features
├── README.md              # This file
└── .env                   # Environment variables (create this)
```
