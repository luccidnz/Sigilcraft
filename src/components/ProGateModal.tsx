import { useState, useEffect, useRef } from 'react';
import { useAuth } from '../auth/auth';

interface ProGateModalProps {
  open?: boolean;
  onClose?: () => void;
}

export default function ProGateModal({ open = false, onClose }: ProGateModalProps) {
  const { session, signIn } = useAuth();
  const [pending, setPending] = useState(false);
  const keyRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && open && onClose) {
        onClose();
      }
    };
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, [open, onClose]);

  if (!open && !pending) return null;

  const user = session?.user ?? null;
  const displayName = user?.name ?? 'Seeker';

  const handleActivate = async () => {
    const key = keyRef.current?.value.trim();
    if (!key) return;
    setPending(true);
    try {
      await fetch('/api/status', { method: 'GET' });
      if (onClose) onClose();
    } finally {
      setPending(false);
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-navy-950/70 backdrop-blur-sm"
      onClick={(e) => {
        if (e.target === e.currentTarget && onClose) onClose();
      }}
      role="dialog"
      aria-modal="true"
    >
      <div className="w-full max-w-md overflow-hidden rounded-2xl border border-violet-500/30 bg-navy-900/95 shadow-sigil backdrop-blur-md">
        <div className="relative">
          <div className="flex items-center gap-3 border-b border-violet-500/20 bg-navy-950 px-6 py-5">
            <span className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-violet-500/20 text-xl">
              🔮
            </span>
            <div>
              <h2 className="font-display text-lg font-semibold tracking-wide text-violet-100">
                Unlock Sigilcraft
              </h2>
              <p className="text-sm text-violet-300/70">
                For {displayName}
              </p>
            </div>
            <button
              type="button"
              onClick={onClose}
              className="ml-auto flex h-8 w-8 items-center justify-center rounded-lg text-violet-300 transition-colors hover:bg-violet-500/20 hover:text-white"
              aria-label="Close"
            >
              <span className="text-lg leading-none">×</span>
            </button>
          </div>

          <div className="space-y-5 px-6 py-6">
            <div className="space-y-3 text-sm leading-relaxed text-navy-100">
              <p className="text-violet-200 font-medium tracking-wide">
                Sigilcraft is free to explore. Upgrade to Pro when you are ready to
                keep your gallery, higher resolutions, and priority generation.
              </p>
              <ul className="space-y-2 text-navy-200">
                <li className="flex items-start gap-3">
                  <span className="mt-0.5 text-violet-400">◆</span>
                  <span>Persistent gallery stored in your account</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="mt-0.5 text-violet-400">◆</span>
                  <span>Higher resolution sigil exports</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="mt-0.5 text-violet-400">◆</span>
                  <span>No per-session generation limits</span>
                </li>
              </ul>
            </div>

            <button
              type="button"
              onClick={async () => {
                setPending(true);
                try {
                  await fetch('/api/status', { method: 'GET' });
                  setPending(false);
                  if (onClose) onClose();
                } catch {
                  setPending(false);
                }
              }}
              disabled={pending}
              className="w-full rounded-xl bg-gradient-to-r from-violet-600 to-violet-500 px-5 py-3 text-sm font-medium tracking-wide text-white shadow-glow transition-all hover:from-violet-500 hover:to-violet-400 focus:outline-none focus-visible:ring focus-visible:ring-violet-400"
            >
              {pending ? 'Opening gateway…' : 'Enter Sigilcraft'}
            </button>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t border-violet-500/20" />
              </div>
              <div className="relative flex justify-center text-xs uppercase tracking-wide text-navy-400">
                <span>or use a key</span>
              </div>
            </div>

            <div className="flex gap-3">
              <input
                ref={keyRef}
                type="text"
                placeholder="Paste your key"
                className="flex-1 rounded-lg border border-violet-500/30 bg-navy-950 px-4 py-2.5 text-sm text-navy-100 placeholder:text-navy-400 outline-none transition focus:border-violet-400 focus:ring-1 focus:ring-violet-400"
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleActivate();
                  }
                }}
                disabled={pending}
              />
              <button
                type="button"
                onClick={handleActivate}
                disabled={pending}
                className="rounded-lg border border-violet-500/40 bg-violet-500/10 px-4 py-2.5 text-sm font-medium text-violet-100 transition hover:bg-violet-500/20 disabled:opacity-50"
              >
                Activate
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
