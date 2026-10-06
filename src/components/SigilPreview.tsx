import { useState, useEffect } from 'react';

export default function SigilPreview() {
  const [src, setSrc] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phrase: 'Quiet intention',
        vibe: 'mystical',
        quality: 'standard',
        advanced: false
      })
    })
      .then((r) => r.json())
      .then((data) => {
        if (!cancelled && data?.image) {
          setSrc(typeof data.image === 'string' ? data.image : '');
        }
      })
      .catch(() => {
        if (!cancelled) {
          setSrc('data:image/svg+xml;base64,' + btoa(`<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240"><rect width="240" height="240" fill="#0b1220"/><path d="M120 40 L180 140 L120 200 L60 140 Z" fill="none" stroke="#a78bfa" stroke-width="2"/><circle cx="120" cy="120" r="14" fill="#fcd34d"/></svg>`));
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="relative overflow-hidden rounded-2xl border border-violet-500/25 bg-navy-900/60 shadow-sigil">
      <div className="aspect-square flex items-center justify-center bg-navy-950">
        {loading ? (
          <div className="flex flex-col items-center gap-3 text-navy-300">
            <div className="flex gap-1">
              <span className="h-1.5 w-1.5 rounded-full bg-violet-400 animate-pulse" />
              <span className="h-1.5 w-1.5 rounded-full bg-violet-400 animate-pulse" style={{ animationDelay: '150ms' }} />
              <span className="h-1.5 w-1.5 rounded-full bg-violet-400 animate-pulse" style={{ animationDelay: '300ms' }} />
            </div>
            <span className="text-xs uppercase tracking-widest text-navy-400">Composing sign</span>
          </div>
        ) : (
          <img
            src={src ?? ''}
            alt="Preview sigil"
            className="h-full w-full object-contain p-6"
          />
        )}
      </div>
      <div className="absolute bottom-4 left-5 right-5 flex items-center justify-between rounded-lg border border-violet-500/20 bg-navy-950/80 px-4 py-2 backdrop-blur-md">
        <span className="text-sm text-navy-200">“Quiet intention”</span>
        <span className="text-xs uppercase tracking-wider text-gold-400">mystical</span>
      </div>
    </div>
  );
}
