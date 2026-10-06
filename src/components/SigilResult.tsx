import { useState, useCallback, useRef } from 'react';

interface SigilResultProps {
  image: string;
  phrase: string;
  vibe: string;
  quality: string;
  onNew: () => void;
}

export default function SigilResult({ image, phrase, vibe, quality, onNew }: SigilResultProps) {
  const [copied, setCopied] = useState(false);
  const linkRef = useRef<HTMLAnchorElement>(null);  const handleDownload = () => {
    const a = linkRef.current;
    if (!a) return;
    a.download = `${phrase.replace(/[^a-zA-Z0-9]/g, '_')}_${vibe}_${quality}.png`;
    a.click();
  };

  const download = useCallback(handleDownload, [phrase, vibe, quality]);

  return (
    <div className="overflow-hidden rounded-2xl border border-violet-500/25 bg-navy-900/60 p-6 sm:p-8 shadow-sigil backdrop-blur-md">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start">
        <div className="flex-shrink-0 overflow-hidden rounded-xl bg-navy-950 shadow-sigil">
          <img
            src={image}
            alt={phrase}
            className="h-auto max-h-80 w-full object-contain p-4"
          />
        </div>
        <div className="flex flex-1 flex-col gap-3 min-w-0">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="font-display text-xl font-semibold text-white">Your creation</h2>
              <p className="mt-1 text-sm text-navy-300">{phrase}</p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={download}
                className="inline-flex items-center gap-2 rounded-lg border border-violet-500/30 bg-violet-500/10 px-3 py-1.5 text-xs font-medium text-violet-100 transition hover:bg-violet-500/20 hover:text-white"
              >
                Download
              </button>
              <button
                onClick={async () => {
                  try {
                    await navigator.clipboard.writeText(window.location.href);
                    setCopied(true);
                    setTimeout(() => setCopied(false), 2000);
                  } catch {
                    setCopied(false);
                  }
                }}
                className="inline-flex items-center gap-2 rounded-lg border border-violet-500/30 bg-violet-500/10 px-3 py-1.5 text-xs font-medium text-violet-100 transition hover:bg-violet-500/20 hover:text-white"
              >
                {copied ? 'Copied' : 'Share link'}
              </button>
            </div>
          </div>
          <div className="flex flex-wrap gap-2 text-xs uppercase tracking-wide">
            <span className="rounded-full bg-violet-500/15 px-3 py-1 text-violet-200">{vibe}</span>
            <span className="rounded-full bg-navy-800/60 px-3 py-1 text-navy-300">{quality}</span>
          </div>
          <button
            onClick={onNew}
            className="mt-auto rounded-lg border border-violet-500/20 px-4 py-2 text-sm text-navy-300 transition hover:border-violet-400 hover:text-white"
          >
            Create another
          </button>
        </div>
      </div>
      <a
        ref={linkRef}
        href={image}
        download=""
        className="hidden"
      />
    </div>
  );
}

