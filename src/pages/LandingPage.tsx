import { Link } from 'react-router-dom';
import SigilPreview from '../components/SigilPreview';

export default function LandingPage() {
  return (
    <div className="relative min-h-screen bg-navy-950 text-navy-100">
      <div className="pointer-events-none fixed inset-0 overflow-hidden bg-[radial-gradient(ellipse_at_top_right,rgba(139,92,246,0.25),transparent_55%)]" />
      <div className="pointer-events-none fixed inset-0 bg-[linear-gradient(to_bottom,transparent,rgba(5,9,20,0.6))]" />

      <header className="relative z-20 border-b border-violet-500/20 bg-navy-950/70 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-3">
            <span className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-violet-500/20 text-xl">
              🔮
            </span>
            <span className="font-display text-lg font-semibold tracking-wide text-violet-100">
              Sigilcraft
            </span>
          </div>
          <nav className="hidden items-center gap-6 sm:flex">
            <NavPill href="#features">Chapters</NavPill>
            <NavPill href="#gallery">Gallery</NavPill>
            <NavPill href="#pricing">Access</NavPill>
          </nav>
          <div className="flex items-center gap-3">
            <Link
              to="/sigil"
              className="inline-flex items-center gap-2 rounded-xl bg-violet-500/10 px-4 py-2 text-sm font-medium text-violet-100 transition hover:bg-violet-500/20 hover:text-white"
            >
              Enter the studio
              <span className="text-violet-400">→</span>
            </Link>
          </div>
        </div>
      </header>

      <section className="relative z-10 pt-28 pb-20 sm:pt-36 sm:pb-28">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <span className="mb-4 inline-block rounded-full border border-violet-500/30 bg-violet-500/10 px-4 py-1.5 text-xs font-medium uppercase tracking-widest text-gold-400">
            Free to explore · Pro to keep
          </span>
          <h1 className="max-w-3xl mx-auto font-display text-5xl font-bold leading-tight tracking-wide text-balance text-white sm:text-7xl">
            Turned into signs.
            <br />
            <span className="bg-gradient-to-r from-violet-300 via-gold-300 to-cyan-200 bg-clip-text text-transparent">
              Felt by you.
            </span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-navy-200 text-balance">
            Sigilcraft lets you speak an intention and receive a compact symbol you can save,
            export, and return to. Free tiers let you experiment; Pro keeps your work and
            raises the resolution ceiling.
          </p>
          <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
            <Link
              to="/sigil"
              className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-violet-600 to-violet-500 px-7 py-3.5 text-sm font-medium tracking-wide text-white shadow-sigil transition hover:from-violet-500 hover:to-violet-400"
            >
              Create your first sigil
              <span aria-hidden="true">→</span>
            </Link>
            <Link
              to="/gallery"
              className="inline-flex items-center gap-2 rounded-xl border border-violet-500/30 bg-navy-900/60 px-7 py-3.5 text-sm font-medium tracking-wide text-navy-100 transition hover:border-violet-400 hover:bg-navy-900"
            >
              Visit the gallery
            </Link>
          </div>
        </div>
        <div className="mx-auto mt-16 max-w-5xl px-6">
          <SigilPreview />
        </div>
      </section>

      <section id="features" className="relative z-10 border-t border-violet-500/20 bg-navy-950/40">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <div className="mb-14 text-center">
            <span className="mb-3 inline-block text-xs font-medium uppercase tracking-widest text-gold-400">
              Chapters
            </span>
            <h2 className="font-display text-3xl font-bold tracking-wide text-white sm:text-4xl">
              How Sigilcraft works
            </h2>
          </div>
          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <Chapter
              number="01"
              title="Speak a phrase"
              body="Write a short intention — a wish, a boundary, a reminder — and choose the energy you want it to carry."
            />
            <Chapter
              number="02"
              title="Receive a sign"
              body="The studio returns a compact sigil tuned to your phrase and vibe. Save it to your gallery or export it immediately."
            />
            <Chapter
              number="03"
              title="Keep what matters"
              body="Free visitors can experiment. Signing in unlocks a persistent gallery, higher resolutions, and priority generation."
            />
          </div>
        </div>
      </section>

      <section id="gallery" className="relative z-10 border-t border-violet-500/20 py-24">
        <div className="mx-auto max-w-6xl px-6">
          <div className="mb-12 text-center">
            <span className="mb-3 inline-block text-xs font-medium uppercase tracking-widest text-gold-400">
              Recent signs
            </span>
            <h2 className="font-display text-3xl font-bold tracking-wide text-white sm:text-4xl">
              A gallery of intentions
            </h2>
          </div>
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            <GalleryThumb phrase="Stillness in motion" vibe="mystical" />
            <GalleryThumb phrase="Forged in attention" vibe="crystal" />
            <GalleryThumb phrase="Rooted light" vibe="aurora" />
          </div>
        </div>
      </section>

      <section id="pricing" className="relative z-10 border-t border-violet-500/20 bg-navy-950/40 py-24">
        <div className="mx-auto max-w-4xl px-6">
          <div className="mb-12 text-center">
            <span className="mb-3 inline-block text-xs font-medium uppercase tracking-widest text-gold-400">
              Access
            </span>
            <h2 className="font-display text-3xl font-bold tracking-wide text-white sm:text-4xl">
              Free to begin · Pro to keep
            </h2>
          </div>
          <div className="grid gap-6 sm:grid-cols-2">
            <div className="rounded-2xl border border-violet-500/20 bg-navy-900/50 p-6 backdrop-blur-md">
              <h3 className="mb-2 font-display text-lg font-semibold text-violet-100">Explorer</h3>
              <p className="mb-5 text-sm text-navy-300">Try the studio, generate signs, and experience the vibe palette without an account.</p>
              <ul className="space-y-3 text-sm text-navy-200">
                <li className="flex items-start gap-3"><span className="mt-0.5 text-gold-400">◆</span>Generate signs from your phrase</li>
                <li className="flex items-start gap-3"><span className="mt-0.5 text-gold-400">◆</span>Choose from the core vibes</li>
                <li className="flex items-start gap-3"><span className="mt-0.5 text-gold-400">◆</span>Export a compact PNG</li>
                <li className="flex items-start gap-3"><span className="mt-0.5 text-navy-500">◇</span>Persistent gallery</li>
                <li className="flex items-start gap-3"><span className="mt-0.5 text-navy-500">◇</span>Higher resolution exports</li>
              </ul>
            </div>
            <div className="rounded-2xl border border-gold-500/40 bg-navy-900/70 p-6 shadow-sigil backdrop-blur-md">
              <h3 className="mb-2 font-display text-lg font-semibold text-gold-300">Pro</h3>
              <p className="mb-5 text-sm text-navy-300">Sign in to keep your sigils, raise the resolution ceiling, and generate with priority.</p>
              <ul className="space-y-3 text-sm text-navy-200">
                <li className="flex items-start gap-3"><span className="mt-0.5 text-gold-400">◆</span>Persistent gallery tied to your account</li>
                <li className="flex items-start gap-3"><span className="mt-0.5 text-gold-400">◆</span>Higher resolution PNG exports</li>
                <li className="flex items-start gap-3"><span className="mt-0.5 text-gold-400">◆</span>Priority generation when you return</li>
                <li className="flex items-start gap-3"><span className="mt-0.5 text-gold-400">◆</span>Full vibe palette access</li>
              </ul>
            </div>
          </div>
          <div className="mt-10 text-center">
            <Link
              to="/auth?returnTo=/gallery"
              className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-violet-600 to-violet-500 px-6 py-3 text-sm font-medium tracking-wide text-white shadow-sigil transition hover:from-violet-500 hover:to-violet-400"
            >
              Sign in to keep your sigils
              <span aria-hidden="true">→</span>
            </Link>
          </div>
        </div>
      </section>

      <footer className="relative z-10 border-t border-violet-500/20 bg-navy-950/60 py-10">
        <div className="mx-auto max-w-6xl px-6 text-center text-sm text-navy-300">
          <p className="mb-3 tracking-wide">Sigilcraft — craft brief signs for lifelong intentions.</p>
          <p className="text-navy-400">Free to explore. Pro to keep.</p>
        </div>
      </footer>
    </div>
  );
}

function NavPill({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <a
      href={href}
      className="text-sm text-navy-300 transition hover:text-violet-200"
    >
      {children}
    </a>
  );
}

function Chapter({
  number,
  title,
  body
}: {
  number: string;
  title: string;
  body: string;
}) {
  return (
    <div className="group rounded-2xl border border-violet-500/20 bg-navy-900/40 p-7 transition hover:border-violet-500/40 hover:bg-navy-900/60">
      <span className="mb-4 inline-block font-mono text-xs text-gold-400/70">{number}</span>
      <h3 className="mb-3 font-display text-xl font-semibold tracking-wide text-white">{title}</h3>
      <p className="text-sm leading-relaxed text-navy-200">{body}</p>
    </div>
  );
}

function GalleryThumb({
  phrase,
  vibe
}: {
  phrase: string;
  vibe: string;
}) {
  return (
    <Link
      to="/gallery"
      className="group relative overflow-hidden rounded-xl border border-violet-500/20 bg-navy-900/60 p-4 transition hover:border-violet-500/50"
    >
      <div className="aspect-square overflow-hidden rounded-lg bg-navy-950 shadow-sigil">
        <div className="absolute inset-0 flex items-center justify-center text-4xl opacity-40 group-hover:opacity-70 transition-opacity" aria-hidden="true">
          ◆
        </div>
      </div>
      <div className="mt-3 text-left">
        <p className="text-sm font-medium text-navy-100">{phrase}</p>
        <p className="mt-1 text-xs uppercase tracking-wider text-violet-300/60">{vibe}</p>
      </div>
    </Link>
  );
}
