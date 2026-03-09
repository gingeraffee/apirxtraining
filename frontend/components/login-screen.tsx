import { FormEvent, useEffect, useRef, useState } from "react";

type LoginScreenProps = {
  defaultName: string;
  isPending: boolean;
  onSubmit: (fullName: string) => void;
};

type SceneNavItem = {
  label: string;
  index: number;
};

type SceneCard = {
  eyebrow: string;
  title: string;
  body: string;
};

const SCENE_NAV: SceneNavItem[] = [
  { label: "Inside the path", index: 1 },
  { label: "How it works", index: 2 },
  { label: "About AAP", index: 3 },
  { label: "Need support?", index: 4 },
];

const INSIDE_CARDS = [
  { icon: "01", label: "9 live modules", sub: "The tracked launch path, start to finish." },
  { icon: "RH", label: "Resource Hub", sub: "Live files and support contacts that stay available." },
  { icon: "✓", label: "Manual completion", sub: "You decide when a module is finished." },
  { icon: "90", label: "First 90 days", sub: "Momentum for week one and a useful reference after." },
];

const HOW_IT_WORKS: SceneCard[] = [
  {
    eyebrow: "Launch rule",
    title: "One clean path.",
    body: "The portal tracks the same nine live modules for everyone in launch instead of making you hunt through extras.",
  },
  {
    eyebrow: "Launch rule",
    title: "No fake auto-complete.",
    body: "Nothing marks itself done just because you scrolled. You finish each module intentionally.",
  },
  {
    eyebrow: "Launch rule",
    title: "Clear finish line.",
    body: "Final Review & Acknowledgment is the last tracked step, so the path feels crisp instead of fuzzy.",
  },
];

const SUPPORT_CARDS = [
  { label: "Nicole Thornton", desc: "HR Manager and your main onboarding point person." },
  { label: "Brandy Hooper", desc: "Escalation support for sensitive or unresolved HR concerns." },
  { label: "Resource Hub", desc: "Open the handbook file and support contacts whenever you need them." },
  { label: "Timeclock", desc: "Consistent employee-facing timekeeping label across launch materials." },
];

export function LoginScreen({ defaultName, isPending, onSubmit }: LoginScreenProps) {
  const [fullName, setFullName] = useState(defaultName);
  const [activeScene, setActiveScene] = useState(0);
  const storyPanelRef = useRef<HTMLElement>(null);
  const trimmedName = fullName.trim();
  const isValid = !!trimmedName;
  const sceneCount = 5;

  useEffect(() => {
    const panel = storyPanelRef.current;
    if (!panel) return;

    const scenes = panel.querySelectorAll<HTMLElement>(".login-scene");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            const idx = Array.from(scenes).indexOf(entry.target as HTMLElement);
            if (idx !== -1) setActiveScene(idx);
          }
        });
      },
      { root: panel, threshold: 0.4 }
    );

    scenes.forEach((scene) => observer.observe(scene));
    return () => observer.disconnect();
  }, []);

  function scrollToScene(index: number) {
    const panel = storyPanelRef.current;
    if (!panel) return;
    const scenes = panel.querySelectorAll<HTMLElement>(".login-scene");
    scenes[index]?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!isValid || isPending) return;
    onSubmit(trimmedName);
  }

  return (
    <div className="login-shell">
      <nav className="login-scroll-dots" aria-label="Page sections">
        {Array.from({ length: sceneCount }, (_, i) => (
          <button
            key={i}
            className={`login-scroll-dot${activeScene === i ? " active" : ""}`}
            onClick={() => scrollToScene(i)}
            aria-label={`Go to section ${i + 1}`}
          />
        ))}
      </nav>

      <section className="login-story-panel" aria-label="Portal introduction" ref={storyPanelRef}>
        <div className="login-scene login-scene--hero is-visible">
          <div className="login-story-inner">
            <div className="login-story-top">
              <div className="portal-brand portal-brand-login">
                <span className="portal-brand-overline">Launch onboarding</span>
                <strong>AAP Start</strong>
                <span className="portal-brand-subline">American Associated Pharmacies</span>
              </div>
              <p className="login-story-kicker">WELCOME ABOARD</p>
            </div>

            <div className="login-story-hero">
              <h1 className="login-story-title">
                <span>Your first week,</span>
                <em>cleaned up and ready.</em>
              </h1>
              <p className="login-story-copy">
                <span className="login-story-copy-line">AAP Start keeps the essentials in one calm, modern flow.</span>
                <span className="login-story-copy-accent">Less document dump. More confidence, momentum, and clear next steps.</span>
              </p>
            </div>

            <div className="login-story-bottom">
              <div className="login-story-nav" aria-label="Jump to section">
                {SCENE_NAV.map(({ label, index }) => (
                  <button key={label} className="login-story-nav-tile" onClick={() => scrollToScene(index)}>
                    <span className="login-story-nav-label">{label}</span>
                    <span className="login-story-nav-arrow" aria-hidden="true">↓</span>
                  </button>
                ))}
              </div>
              <p className="login-story-footer">AAP Start is the launch onboarding portal for American Associated Pharmacies.</p>
            </div>
          </div>
        </div>

        <div className="login-scene login-scene--preview">
          <div className="login-scene-inner">
            <div className="login-scene-content">
              <p className="login-scene-kicker">WHAT'S INSIDE</p>
              <h2 className="login-scene-title">A polished launch path, not a compliance swamp.</h2>
              <p className="login-scene-body">
                Everything inside is organized around what a new hire actually needs first: the company, the standards, the systems, the support map, and a clear finish line.
              </p>
              <div className="login-preview-grid">
                {INSIDE_CARDS.map((card) => (
                  <div className="login-preview-card" key={card.label}>
                    <span className="login-preview-icon login-preview-icon--code" aria-hidden="true">{card.icon}</span>
                    <div>
                      <span className="login-preview-label">{card.label}</span>
                      <span className="login-preview-sub">{card.sub}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="login-scene login-scene--company">
          <div className="login-scene-inner">
            <div className="login-scene-content">
              <p className="login-scene-kicker">HOW IT WORKS</p>
              <h2 className="login-scene-title">Structured enough to guide you, light enough to use.</h2>
              <p className="login-scene-body">
                The launch version stays focused on the universal onboarding path. Resource Hub stays visible, Where You Make an Impact stays visible as coming soon, and neither one distorts your progress.
              </p>
              <div className="login-benefits-grid login-how-grid">
                {HOW_IT_WORKS.map((card) => (
                  <div className="login-benefit-card login-how-card" key={card.title}>
                    <div>
                      <span className="login-benefit-title">{card.eyebrow}</span>
                      <strong className="login-how-card-title">{card.title}</strong>
                      <span className="login-benefit-detail">{card.body}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="login-scene login-scene--benefits">
          <div className="login-scene-inner">
            <div className="login-scene-content">
              <p className="login-scene-kicker">ABOUT AAP</p>
              <h2 className="login-scene-title">Built to support independent community pharmacies.</h2>
              <p className="login-scene-body">
                American Associated Pharmacies exists to support independent pharmacies with practical programs, operational help, and dependable service. AAP Start is the employee-facing version of that same idea: useful, clear, and built to help people move with confidence.
              </p>
              <div className="login-scene-stats login-scene-stats--launch">
                <div className="login-stat-card">
                  <span className="login-stat-number">AAP</span>
                  <span className="login-stat-label">Company short name</span>
                </div>
                <div className="login-stat-card">
                  <span className="login-stat-number">Start</span>
                  <span className="login-stat-label">Portal product name</span>
                </div>
                <div className="login-stat-card">
                  <span className="login-stat-number">9</span>
                  <span className="login-stat-label">Tracked launch modules</span>
                </div>
              </div>
              <div className="login-scene-mission">
                <p>
                  "The goal is not to throw everything at you at once. The goal is to make the right things easy to find, easy to finish, and easy to revisit."
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="login-scene login-scene--culture">
          <div className="login-scene-inner">
            <div className="login-scene-content">
              <p className="login-scene-kicker">NEED SUPPORT?</p>
              <h2 className="login-scene-title">Good onboarding still feels human.</h2>
              <p className="login-scene-body">
                AAP Start is meant to reduce noise, not replace people. When something needs context, interpretation, or a real conversation, the right support path is already built in.
              </p>
              <div className="login-culture-values login-support-values">
                {SUPPORT_CARDS.map((card) => (
                  <div className="login-value-card" key={card.label}>
                    <span className="login-value-dot" aria-hidden="true" />
                    <span className="login-value-label">{card.label}</span>
                    <span className="login-value-desc">{card.desc}</span>
                  </div>
                ))}
              </div>

              <div className="login-culture-cta">
                <p className="login-culture-cta-label">Ready to step into the portal?</p>
                <button type="button" className="login-culture-cta-btn" onClick={() => document.getElementById("portal-full-name")?.focus()}>
                  Enter AAP Start →
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="login-form-panel" aria-label="Portal sign in">
        <div className="login-card-wrap">
          <form className="login-card" onSubmit={handleSubmit}>
            <div className="login-card-header">
              <div className="login-card-accent" aria-hidden="true" />
              <div className="portal-brand portal-brand-card">
                <span className="portal-brand-overline">Launch onboarding</span>
                <strong>AAP Start</strong>
                <span className="portal-brand-subline">American Associated Pharmacies</span>
              </div>
            </div>

            <div className="login-card-body">
              <div className="login-copy-block">
                <h2>Jump into your portal.</h2>
                <p>Use the name you want shown inside AAP Start. This launch build keeps sign-in simple so the experience stays front and center.</p>
              </div>

              <hr className="login-card-divider" aria-hidden="true" />

              <label className="login-field-label" htmlFor="portal-full-name">Your Name</label>
              <div className="login-input-wrap">
                <input
                  id="portal-full-name"
                  type="text"
                  autoComplete="name"
                  placeholder="e.g. Nicole Thornton"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="login-input"
                />
              </div>

              <button className="login-submit" type="submit" disabled={!isValid || isPending}>
                {isPending ? "Opening portal..." : "Enter AAP Start"}
              </button>

              <p className="login-help">Your name personalizes the launch experience locally. Progress still follows the shared demo path in this build.</p>
            </div>
          </form>
        </div>
      </section>
    </div>
  );
}
