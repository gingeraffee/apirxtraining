import { FormEvent, useState, useEffect, useRef } from "react";

type LoginScreenProps = {
  defaultName: string;
  isPending: boolean;
  onSubmit: (fullName: string, employeeNumber: string) => void;
};

export function LoginScreen({ defaultName, isPending, onSubmit }: LoginScreenProps) {
  const [fullName, setFullName] = useState(defaultName);
  const [employeeNumber, setEmployeeNumber] = useState("");
  const [activeScene, setActiveScene] = useState(0);
  const storyPanelRef = useRef<HTMLElement>(null);
  const trimmedName = fullName.trim();
  const trimmedEmpNum = employeeNumber.trim();
  const isValid = !!trimmedName && !!trimmedEmpNum;

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
      {
        root: panel,
        threshold: 0.4,
      }
    );

    scenes.forEach((scene) => observer.observe(scene));
    return () => observer.disconnect();
  }, []);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!isValid || isPending) return;
    onSubmit(trimmedName, trimmedEmpNum);
  }

  const SCENE_COUNT = 5;

  return (
    <div className="login-shell">

      {/* Scroll progress dots */}
      <nav className="login-scroll-dots" aria-label="Page sections">
        {Array.from({ length: SCENE_COUNT }, (_, i) => (
          <button
            key={i}
            className={`login-scroll-dot${activeScene === i ? " active" : ""}`}
            onClick={() => {
              const panel = storyPanelRef.current;
              if (!panel) return;
              const scenes = panel.querySelectorAll<HTMLElement>(".login-scene");
              scenes[i]?.scrollIntoView({ behavior: "smooth", block: "start" });
            }}
            aria-label={`Go to section ${i + 1}`}
          />
        ))}
      </nav>

      {/* Left: scroll-snap story panel */}
      <section
        className="login-story-panel"
        aria-label="Portal introduction"
        ref={storyPanelRef}
      >

        {/* ── Scene 1: Hero ── */}
        <div className="login-scene login-scene--hero is-visible">
          <div className="login-story-inner">

            <div className="login-story-top">
              <img src="/logo.png" alt="AAP API logos" className="login-story-logo" />
              <p className="login-story-kicker">WELCOME ABOARD.</p>

            </div>

            <div className="login-story-hero">
              <h1 className="login-story-title">
                <span>Ready for day one?</span>
                <em>You are now.</em>
              </h1>
              <p className="login-story-copy">
                <span className="login-story-copy-line">A smoother start begins here.</span>
                <span className="login-story-copy-accent">Because day one already has enough surprises.</span>
              </p>
            </div>

            <div className="login-story-bottom">
              <div className="login-story-nav" aria-label="Jump to section">
                {[
                  { label: "What's Inside",  index: 1 },
                  { label: "About AAP",      index: 2 },
                  { label: "Your Benefits",  index: 3 },
                  { label: "Life at AAP",    index: 4 },
                ].map(({ label, index }) => (
                  <button
                    key={label}
                    className="login-story-nav-tile"
                    onClick={() => {
                      const panel = storyPanelRef.current;
                      if (!panel) return;
                      const scenes = panel.querySelectorAll<HTMLElement>(".login-scene");
                      scenes[index]?.scrollIntoView({ behavior: "smooth", block: "start" });
                    }}
                  >
                    <span className="login-story-nav-label">{label}</span>
                    <span className="login-story-nav-arrow" aria-hidden="true">↓</span>
                  </button>
                ))}
              </div>
              <p className="login-story-footer">© 2026 AAP — All rights reserved</p>
            </div>

          </div>
        </div>

        {/* ── Scene 2: What's Inside ── */}
        <div className="login-scene login-scene--preview">
          <div className="login-scene-inner">
            <div className="login-scene-content">
              <p className="login-scene-kicker">WHAT'S INSIDE</p>
              <h2 className="login-scene-title">Your first 90 days,<br />mapped out and ready.</h2>
              <p className="login-scene-body">
                Everything you need to hit the ground running is already waiting for you inside.
                No hunting, no guessing — just clear, structured onboarding from the moment you sign in.
              </p>
              <div className="login-preview-grid">
                {[
                  { icon: "📚", label: "6 Training Modules",  sub: "Self-paced, built around how you work" },
                  { icon: "🗺️", label: "90-Day Roadmap",      sub: "Your 30-60-90 milestones, crystal clear" },
                  { icon: "📋", label: "Handbook + Policies", sub: "Everything you need to know, in one place" },
                  { icon: "🎯", label: "Benefits Breakdown",  sub: "Your full 2026 benefits, explained simply" },
                ].map((p) => (
                  <div className="login-preview-card" key={p.label}>
                    <span className="login-preview-icon" aria-hidden="true">{p.icon}</span>
                    <div>
                      <span className="login-preview-label">{p.label}</span>
                      <span className="login-preview-sub">{p.sub}</span>
                    </div>
                  </div>
                ))}
              </div>

            </div>
          </div>
        </div>

        {/* ── Scene 3: About AAP ── */}
        <div className="login-scene login-scene--company">
          <div className="login-scene-inner">
            <div className="login-scene-content">
              <p className="login-scene-kicker">ABOUT AAP</p>
              <h2 className="login-scene-title">Powering independent<br />pharmacies across America.</h2>
              <p className="login-scene-body">
                Founded in 2009 from the union of API (Scottsboro, AL) and United Drugs
                (Phoenix, AZ), AAP became one of America's largest member-owned independent
                pharmacy cooperatives. We fight to keep community pharmacies competitive,
                profitable, and thriving — and now you're part of that mission.
              </p>
              <div className="login-scene-stats">
                <div className="login-stat-card">
                  <span className="login-stat-number">2,100+</span>
                  <span className="login-stat-label">Member Pharmacies</span>
                </div>
                <div className="login-stat-card">
                  <span className="login-stat-number">2009</span>
                  <span className="login-stat-label">Year Founded</span>
                </div>
                <div className="login-stat-card">
                  <span className="login-stat-number">Scottsboro</span>
                  <span className="login-stat-label">Headquarters, AL</span>
                </div>
              </div>
              <div className="login-scene-mission">
                <p>
                  "AAP provides support and customized solutions for independent community
                  pharmacies to enhance their profitability, streamline their operations,
                  and improve the quality of patient care."
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* ── Scene 4: Benefits ── */}
        <div className="login-scene login-scene--benefits">
          <div className="login-scene-inner">
            <div className="login-scene-content">
              <p className="login-scene-kicker">YOUR BENEFITS</p>
              <h2 className="login-scene-title">You're covered.<br />Seriously covered.</h2>
              <div className="login-benefits-grid">
                {[
                  { icon: "🏥", title: "Medical",         detail: "BlueCross BlueShield of Alabama — PPO or HDHP+HSA. Company contributes up to $1,800/yr to your HSA." },
                  { icon: "💰", title: "401(k) Match",    detail: "100% match on your first 3%, 50% on the next 2%. Fully vested from day one." },
                  { icon: "🦷", title: "Dental + Vision", detail: "Guardian dental and vision plans. Preventive care covered at 100%." },
                  { icon: "🛡️", title: "Life & AD&D",     detail: "Company-paid basic life insurance up to your annual salary — at no cost to you." },
                  { icon: "📱", title: "Free Teladoc",    detail: "24/7 telehealth for general medical and mental health visits. Completely free to you." },
                  { icon: "🌿", title: "EAP + Perks",     detail: "Confidential counseling through Life Matters, plus BenefitHub discounts on thousands of brands." },
                ].map((b) => (
                  <div className="login-benefit-card" key={b.title}>
                    <span className="login-benefit-icon" aria-hidden="true">{b.icon}</span>
                    <div>
                      <span className="login-benefit-title">{b.title}</span>
                      <span className="login-benefit-detail">{b.detail}</span>
                    </div>
                  </div>
                ))}
              </div>
              <p className="login-benefits-note">Benefits begin the first of the month following 60 days of employment.</p>
            </div>
          </div>
        </div>

        {/* ── Scene 5: Culture ── */}
        <div className="login-scene login-scene--culture">
          <div className="login-scene-inner">
            <div className="login-scene-content">
              <p className="login-scene-kicker">LIFE AT AAP</p>
              <h2 className="login-scene-title">Where good people<br />do great work.</h2>
              <p className="login-scene-body">
                At AAP, you're not a number in a headcount — you're a partner. Your ideas shape
                how things run. Your feedback drives real improvement. And your growth is
                something we actively invest in, not just talk about.
              </p>
              <div className="login-culture-values">
                {[
                  { label: "Customer Focus", desc: "Service isn't a department — it's an attitude" },
                  { label: "Integrity",       desc: "We say what we mean, and mean what we say" },
                  { label: "Respect",         desc: "Every voice matters. Every contribution counts" },
                  { label: "Excellence",      desc: "We raise the bar, then raise it again" },
                  { label: "Ownership",       desc: "We take responsibility and own our results" },
                ].map((v) => (
                  <div className="login-value-card" key={v.label}>
                    <span className="login-value-dot" aria-hidden="true" />
                    <span className="login-value-label">{v.label}</span>
                    <span className="login-value-desc">{v.desc}</span>
                  </div>
                ))}
              </div>

              <div className="login-culture-cta">
                <p className="login-culture-cta-label">You've seen what we're about.</p>
                <button
                  type="button"
                  className="login-culture-cta-btn"
                  onClick={() => {
                    const input = document.getElementById("portal-full-name");
                    input?.focus();
                    input?.scrollIntoView({ behavior: "smooth", block: "center" });
                  }}
                >
                  Sign in to your portal →
                </button>
              </div>
            </div>
          </div>
        </div>

      </section>

      {/* ── Right: locked login form ── */}
      <section className="login-form-panel" aria-label="Portal sign in">
        <div className="login-card-wrap">
          <form className="login-card" onSubmit={handleSubmit}>

            <div className="login-card-header">
              <div className="login-card-accent" aria-hidden="true" />
            </div>

            <div className="login-card-body">
              <div className="login-copy-block">
                <h2>Let's get you in.</h2>
                <p>Enter your name and employee number to jump into your portal.</p>
              </div>

              <hr className="login-card-divider" aria-hidden="true" />

              <label className="login-field-label" htmlFor="portal-full-name">Full Name</label>
              <div className="login-input-wrap">
                <input
                  id="portal-full-name"
                  type="text"
                  autoComplete="name"
                  placeholder="e.g. Jane Doe"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="login-input"
                />
              </div>

              <label className="login-field-label" htmlFor="portal-employee-number">Employee Number</label>
              <div className="login-input-wrap">
                <input
                  id="portal-employee-number"
                  type="text"
                  autoComplete="off"
                  placeholder="e.g. 10042"
                  value={employeeNumber}
                  onChange={(e) => setEmployeeNumber(e.target.value)}
                  className="login-input"
                />
              </div>

              <button className="login-submit" type="submit" disabled={!isValid || isPending}>
                {isPending ? "Verifying..." : "Sign in"}
              </button>

              <p className="login-help">Your employee number is in BambooHR under My Info.</p>
            </div>

          </form>
        </div>
      </section>
    </div>
  );
}
