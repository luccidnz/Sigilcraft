import { useState, useCallback } from 'react';
import { Link } from 'react-router-dom';
import SigilResult from '../components/SigilResult';

const VIBES = [
  { value: 'mystical', label: 'Mystical', hint: 'Ancient wisdom & sacred geometry' },
  { value: 'cosmic', label: 'Cosmic', hint: 'Universal stellar connection' },
  { value: 'elemental', label: 'Elemental', hint: 'Natural organic forces' },
  { value: 'crystal', label: 'Crystal', hint: 'Prismatic geometric precision' },
  { value: 'shadow', label: 'Shadow', hint: 'Hidden mysterious power' },
  { value: 'light', label: 'Light', hint: 'Pure divine radiance' },
  { value: 'storm', label: 'Storm', hint: 'Raw electric chaos' },
  { value: 'void', label: 'Void', hint: 'Infinite recursive potential' }
];

const QUALITIES = [
  { value: 'standard', label: 'Standard', note: '512px', pro: false },
  { value: 'hd', label: 'HD', note: '2048px', pro: true },
  { value: '4k', label: '4K', note: '4096px', pro: true }
];

export default function SigilPage() {
  const [phrase, setPhrase] = useState('');
  const [vibe, setVibe] = useState('mystical');
  const [quality, setQuality] = useState('standard');
  const [generating, setGenerating] = useState(false);
  const [result, setResult] = useState<{ image: string; phrase: string; vibe: string; quality: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const isValid = phrase.trim().length >= 2 && phrase.trim().length <= 500;

  const handleGenerate = useCallback(async () => {
    if (!isValid || generating) return;
    setGenerating(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          phrase: phrase.trim(),
          vibe,
          quality,
          advanced: quality !== 'standard'
        })
      });
      const data = await res.json();
      if (!res.ok || !data?.image) {
        setError(data?.error ?? 'Generation failed.');
        return;
      }
      setResult({
        image: data.image,
        phrase: data.metadata?.phrase ?? phrase.trim(),
        vibe: data.metadata?.vibe ?? vibe,
        quality: data.metadata?.quality ?? quality
      });
    } catch {
      setError('Network error. Please try again.');
    } finally {
      setGenerating(false);
    }
  }, [phrase, vibe, quality, isValid, generating]);

  return (
    <div className="relative min-h-screen bg-navy-950 text-navy-100">
      <div className="pointer-events-none fixed inset-0 overflow-hidden bg-[radial-gradient(ellipse_at_bottom_left,rgba(139,92,246,0.25),transparent_60%)]" />

      <header className="relative z-20 border-b border-violet-500/20 bg-navy-950/70 backdrop-blur-md">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <Link to="/" className="flex items-center gap-3">
            <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-violet-500/20 text-lg">
              🔮
            </span>
            <span className="font-display text-base font-semibold tracking-wide text-violet-100">
              Sigilcraft
            </span>
          </Link>
          <div className="flex items-center gap-3">
            <Link
              to="/gallery"
              className="text-sm text-navy-300 transition hover:text-violet-200"
            >
              Gallery
            </Link>
            <Link
              to="/auth?returnTo=/sigil"
              className="rounded-lg border border-violet-500/30 bg-violet-500/10 px-4 py-1.5 text-xs font-medium text-violet-100 transition hover:bg-violet-500/20"
            >
              Sign in
            </Link>
          </div>
        </div>
      </header>

      <main className="relative z-10 px-6 py-12 sm:py-16">
        <div className="mx-auto max-w-3xl">
          <div className="mb-8 text-center">
            <h1 className="font-display text-3xl font-bold tracking-wide text-white sm:text-4xl">
              Manifest your vision
            </h1>
            <p className="mt-3 text-sm text-navy-300 text-balance max-w-lg mx-auto">
              Write an intention and choose the energy you want it to carry.
            </p>
          </div>

          <div className="space-y-6 rounded-2xl border border-violet-500/20 bg-navy-900/40 p-6 sm:p-8 backdrop-blur-md">
            <div>
              <label htmlFor="phrase" className="mb-2 block text-sm font-medium text-violet-200">
                Sacred intention
              </label>
              <textarea
                id="phrase"
                value={phrase}
                onChange={(e) => setPhrase(e.target.value)}
                placeholder="Speak your intention into existence…"
                maxLength={500}
                rows={4}
                className="w-full resize-y rounded-xl border border-violet-500/30 bg-navy-950/70 px-4 py-3 text-sm text-navy-100 placeholder:text-navy-400 transition focus:border-violet-400 focus:ring-1 focus:ring-violet-400"
              />
              <div className="mt-2 flex items-center justify-between text-xs text-navy-400">
                <span>{phrase.length}/500</span>
                <span className="text-violet-200/60">At least 2 characters</span>
              </div>
            </div>

            <div className="grid gap-5 sm:grid-cols-2">
              <div>
                <label htmlFor="vibe" className="mb-2 block text-sm font-medium text-violet-200">
                  Mystical energy
                </label>
                <select
                  id="vibe"
                  value={vibe}
                  onChange={(e) => setVibe(e.target.value)}
                  className="w-full rounded-xl border border-violet-500/30 bg-navy-950/70 px-4 py-2.5 text-sm text-navy-100 transition focus:border-violet-400 focus:ring-1 focus:ring-violet-400"
                >
                  {VIBES.map((v) => (
                    <option key={v.value} value={v.value}>
                      {v.label}
                    </option>
                  ))}
                </select>
                <p className="mt-1.5 text-xs text-navy-400">{VIBES.find((v) => v.value === vibe)?.hint}</p>
              </div>

              <div>
                <label htmlFor="quality" className="mb-2 block text-sm font-medium text-violet-200">
                  Manifestation power
                </label>
                <select
                  id="quality"
                  value={quality}
                  onChange={(e) => setQuality(e.target.value)}
                  className="w-full rounded-xl border border-violet-500/30 bg-navy-950/70 px-4 py-2.5 text-sm text-navy-100 transition focus:border-violet-400 focus:ring-1 focus:ring-violet-400"
                >
                  {QUALITIES.map((q) => (
                    <option key={q.value} value={q.value} disabled={q.pro}>
                      {q.label} — {q.note}
                      {q.pro ? ' · Pro' : ''}
                    </option>
                  ))}
                </select>
                <p className="mt-1.5 text-xs text-navy-500">
                  Higher tiers unlock larger exports.
                </p>
              </div>
            </div>

            <button
              onClick={handleGenerate}
              disabled={!isValid || generating}
              className="w-full rounded-xl bg-gradient-to-r from-violet-600 to-violet-500 px-5 py-3.5 text-sm font-medium tracking-wide text-white shadow-sigil transition disabled:opacity-50 disabled:cursor-not-allowed hover:from-violet-500 hover:to-violet-400"
            >
              {generating ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                  Composing…
                </span>
              ) : (
                <span className="flex items-center justify-center gap-2">
                  Manifest sigil
                  <span aria-hidden="true">→</span>
                </span>
              )}
            </button>

            {error && (
              <p className="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-2.5 text-sm text-red-200">
                {error}
              </p>
            )}
          </div>

          {result && (
            <div className="mt-8">
              <SigilResult
                image={result.image}
                phrase={result.phrase}
                vibe={result.vibe}
                quality={result.quality}
                onNew={() => setResult(null)}
              />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
