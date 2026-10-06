import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

interface GalleryItem {
  id: string;
  phrase: string;
  vibe: string;
  quality: string;
  image: string;
  createdAt: number;
}

const SAMPLE_GALLERY: GalleryItem[] = [
  {
    id: '1',
    phrase: 'Stillness in motion',
    vibe: 'mystical',
    quality: 'standard',
    image: 'data:image/svg+xml;base64,' + btoa(`<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240"><rect width="240" height="240" fill="#0b1220"/><circle cx="120" cy="120" r="36" fill="none" stroke="#a78bfa" stroke-width="2"/><path d="M120 48 L150 100 L120 152 L90 100 Z" fill="none" stroke="#fcd34d" stroke-width="2"/><circle cx="120" cy="120" r="8" fill="#fcd34d"/></svg>`),
    createdAt: Date.now() - 1000 * 60 * 60 * 24
  },
  {
    id: '2',
    phrase: 'Forged in attention',
    vibe: 'crystal',
    quality: 'hd',
    image: 'data:image/svg+xml;base64,' + btoa(`<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240"><rect width="240" height="240" fill="#0b1220"/><path d="M120 40 L200 120 L120 200 L40 120 Z" fill="none" stroke="#c4b5fd" stroke-width="2"/><circle cx="120" cy="120" r="18" fill="none" stroke="#fcd34d" stroke-width="2"/><circle cx="120" cy="120" r="6" fill="#fbbf24"/></svg>`),
    createdAt: Date.now() - 1000 * 60 * 60 * 3
  },
  {
    id: '3',
    phrase: 'Rooted light',
    vibe: 'aurora',
    quality: 'standard',
    image: 'data:image/svg+xml;base64,' + btoa(`<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240"><rect width="240" height="240" fill="#0b1220"/><path d="M40 120 Q90 70 120 120 T200 120" fill="none" stroke="#34d399" stroke-width="2"/><path d="M40 140 Q90 100 120 140 T200 140" fill="none" stroke="#a78bfa" stroke-width="2"/><circle cx="120" cy="120" r="8" fill="#fbbf24"/></svg>`),
    createdAt: Date.now() - 1000 * 60 * 60 * 8
  }
];

export default function GalleryPage() {
  const [items, setItems] = useState<GalleryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem('sigilcraft_gallery');
    if (stored) {
      try {
        setItems(JSON.parse(stored));
      } catch {
        setItems(SAMPLE_GALLERY);
      }
    } else {
      setItems(SAMPLE_GALLERY);
    }
    setLoading(false);
  }, []);

  const savedAt = (ts: number) => {
    const d = new Date(ts);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="relative min-h-screen bg-navy-950 text-navy-100">
      <div className="pointer-events-none fixed inset-0 overflow-hidden bg-[radial-gradient(ellipse_at_top_right,rgba(139,92,246,0.2),transparent_60%)]" />

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
            <Link to="/sigil" className="text-sm text-navy-300 transition hover:text-violet-200">
              Create
            </Link>
            <Link
              to="/auth?returnTo=/gallery"
              className="rounded-lg border border-violet-500/30 bg-violet-500/10 px-4 py-1.5 text-xs font-medium text-violet-100 transition hover:bg-violet-500/20"
            >
              Sign in
            </Link>
          </div>
        </div>
      </header>

      <main className="relative z-10 px-6 py-12 sm:py-16">
        <div className="mx-auto max-w-5xl">
          <div className="mb-8 flex items-center justify-between">
            <div>
              <h1 className="font-display text-3xl font-bold tracking-wide text-white sm:text-4xl">
                Gallery
              </h1>
              <p className="mt-2 text-sm text-navy-300">
                Your saved sigils appear here. Sign in to keep them across devices.
              </p>
            </div>
            <Link
              to="/sigil"
              className="inline-flex items-center gap-2 rounded-lg border border-violet-500/30 bg-violet-500/10 px-4 py-2 text-sm font-medium text-violet-100 transition hover:bg-violet-500/20 hover:text-white"
            >
              New sigil
              <span aria-hidden="true">→</span>
            </Link>
          </div>

          {loading ? (
            <div className="flex flex-col items-center gap-3 py-16 text-navy-300">
              <div className="flex gap-1">
                <span className="h-1.5 w-1.5 rounded-full bg-violet-400 animate-pulse" />
                <span className="h-1.5 w-1.5 rounded-full bg-violet-400 animate-pulse" style={{ animationDelay: '150ms' }} />
                <span className="h-1.5 w-1.5 rounded-full bg-violet-400 animate-pulse" style={{ animationDelay: '300ms' }} />
              </div>
              <span className="text-xs uppercase tracking-widest text-navy-400">Opening gallery</span>
            </div>
          ) : items.length === 0 ? (
            <div className="flex flex-col items-center gap-4 py-16 text-center">
              <span className="text-4xl text-navy-400">◆</span>
              <p className="text-sm text-navy-300">Your gallery is empty.</p>
              <Link
                to="/sigil"
                className="rounded-lg border border-violet-500/30 bg-violet-500/10 px-5 py-2 text-sm font-medium text-violet-100 transition hover:bg-violet-500/20"
              >
                Create your first sigil
              </Link>
            </div>
          ) : (
            <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {items.map((item) => (
                <article key={item.id} className="group overflow-hidden rounded-2xl border border-violet-500/20 bg-navy-900/50 p-4 backdrop-blur-md transition hover:border-violet-500/50">
                  <div className="aspect-square overflow-hidden rounded-xl bg-navy-950 shadow-sigil">
                    <img
                      src={item.image}
                      alt={item.phrase}
                      className="h-full w-full object-contain p-5"
                    />
                  </div>
                  <div className="mt-3 flex items-start justify-between gap-3">
                    <div>
                      <p className="text-sm font-medium text-navy-100 truncate max-w-[180px]">{item.phrase}</p>
                      <div className="mt-1 flex gap-2 text-xs uppercase tracking-wide">
                        <span className="text-violet-300">{item.vibe}</span>
                        <span className="text-navy-400">{item.quality}</span>
                      </div>
                    </div>
                    <span className="text-xs text-navy-400">{savedAt(item.createdAt)}</span>
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
