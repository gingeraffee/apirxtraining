"use client";

import Link from "next/link";
import { useEffect, useState, useTransition } from "react";

import { acknowledgeSection, fetchExperience, fetchProgress, saveProgress } from "@/lib/api";
import type { ExperienceContent, ProgressRecord, Section, Toolkit } from "@/lib/types";
import { OverviewScreen } from "@/components/overview/overview-screen";
import { LoginScreen } from "@/components/login-screen";

type PortalKind = "overview" | "section" | "toolkit";

type PortalExperienceProps = {
  kind: PortalKind;
  slug?: string;
};

const EMPLOYEE_ID = "demo-employee";
const AUTH_NAME_KEY = "aap_portal_name";
const FALLBACK_DISPLAY_NAME = "";

export function PortalExperience({ kind, slug }: PortalExperienceProps) {
  const [experience, setExperience] = useState<ExperienceContent | null>(null);
  const [progress, setProgress] = useState<ProgressRecord | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [profileName, setProfileName] = useState<string | null>(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem(AUTH_NAME_KEY) ?? null;
    }
    return null;
  });
  const [checkedItems, setCheckedItems] = useState<Record<string, boolean[]>>({});
  const [isPending, startTransition] = useTransition();
  const [isSigningIn, setIsSigningIn] = useState(false);

  useEffect(() => {
    let isCancelled = false;

    async function load() {
      setLoading(true);
      setError(null);

      try {
        const [nextExperience, nextProgress] = await Promise.all([
          fetchExperience(),
          fetchProgress(EMPLOYEE_ID),
        ]);

        if (isCancelled) {
          return;
        }

        setExperience(nextExperience);
        setProgress(nextProgress);
      } catch {
        if (!isCancelled) {
          setError("The onboarding API is unavailable. Start the FastAPI backend and reload this page.");
        }
      } finally {
        if (!isCancelled) {
          setLoading(false);
        }
      }
    }

    void load();

    return () => {
      isCancelled = true;
    };
  }, []);

  const displayName = profileName ?? progress?.display_name ?? FALLBACK_DISPLAY_NAME;
  const firstName = displayName.split(" ")[0] ?? displayName;
  const sections = experience?.sections ?? [];
  const toolkit = experience?.toolkits[0];
  const activeSection = sections.find((section) => section.slug === slug);
  const completedSections = new Set(progress?.completed_sections ?? []);
  const acknowledgedSections = new Set(progress?.acknowledged_sections ?? []);
  const completionPercent = sections.length
    ? Math.round(((progress?.completed_sections.length ?? 0) / sections.length) * 100)
    : 0;
  const nextSection = sections.find((section) => !completedSections.has(section.slug)) ?? sections[0] ?? null;
  const contextTitle = kind === "section" && activeSection
    ? activeSection.title
    : kind === "toolkit" && toolkit
      ? toolkit.title
      : "Overview";
  const contextType = kind === "toolkit"
    ? "Role-specific toolkit"
    : kind === "section"
      ? "Core onboarding section"
      : "Core onboarding overview";

  useEffect(() => {
    if (!activeSection) {
      return;
    }

    setCheckedItems((current) => {
      if (current[activeSection.slug]) {
        return current;
      }

      return {
        ...current,
        [activeSection.slug]: activeSection.acknowledgment.items.map(() => false),
      };
    });
  }, [activeSection]);

  async function syncCurrentSection(currentSlug: string) {
    if (!progress || progress.current_section === currentSlug) {
      return;
    }

    try {
      const updated = await saveProgress(EMPLOYEE_ID, {
        display_name: displayName,
        current_section: currentSlug,
        completed_sections: progress.completed_sections,
        acknowledged_sections: progress.acknowledged_sections,
        toolkit_completed: progress.toolkit_completed,
      });
      setProgress(updated);
    } catch {
      // Ignore background sync failures.
    }
  }

  useEffect(() => {
    if (!profileName) {
      return;
    }

    if (kind === "section" && slug && progress) {
      void syncCurrentSection(slug);
    }
    if (kind === "toolkit" && slug && progress) {
      void syncCurrentSection(slug);
    }
  }, [kind, slug, progress, profileName]);

  // Post-render DOM customisation for the overview page.
  // overview-screen.tsx is not directly editable, so we adjust three areas:
  //   1. Hero actions — swap the duplicate "Continue" button for a quiet
  //      "Next up — [module name]" text line.
  //   2. NEXT UP rail card — replace the auto-generated description (which
  //      includes a time estimate) with a genuine module preview: title,
  //      what you'll learn, and why it matters. No button — the active
  //      module card in the main content area is the sole CTA.
  //   3. Contact rail card — replace the generic Questions card with
  //      Nicole's actual contact details.
  useEffect(() => {
    if (kind !== "overview") return;

    const nextTitle   = nextSection?.title   ?? null;
    const nextEyebrow = nextSection?.eyebrow ?? null;
    const nextSummary = nextSection?.summary ?? null;
    const nextPurpose = nextSection?.purpose ?? null;

    function injectOverview(): boolean {
      let allReady = true;

      // ── 1. Hero: replace button with quiet "Next up" text ──────────────
      const heroActions = document.querySelector<HTMLElement>(".ov-hero .ov-hero-actions");
      if (heroActions) {
        if (!heroActions.dataset.heroInjected) {
          heroActions.dataset.heroInjected = "true";
          heroActions.innerHTML = nextTitle
            ? `<div class="hero-next-label">
                 <span class="hero-next-prefix">Next up</span>
                 <span class="hero-next-sep">—</span>
                 <span class="hero-next-title">${nextTitle}</span>
               </div>`
            : "";
        }
      } else {
        allReady = false;
      }

      // ── 2. NEXT UP rail card: informational preview, no button ─────────
      const priorityCard = document.querySelector<HTMLElement>(
        ".ov-side-rail .ov-rail-card-priority"
      );
      if (priorityCard) {
        if (!priorityCard.dataset.nextupInjected) {
          priorityCard.dataset.nextupInjected = "true";
          priorityCard.innerHTML = `
            <p class="section-label">NEXT UP</p>
            ${nextTitle   ? `<h3 class="nextup-title">${nextTitle}</h3>` : ""}
            ${nextEyebrow ? `<p  class="nextup-eyebrow">${nextEyebrow}</p>` : ""}
            ${nextSummary ? `<p  class="nextup-summary">${nextSummary}</p>` : ""}
            ${nextPurpose ? `<p  class="nextup-purpose">${nextPurpose}</p>` : ""}
          `;
        }
      } else {
        allReady = false;
      }

      // ── 3. Contact card: inject only into the last non-priority card ───
      // Filter out any hidden progress cards (they have a progress track element).
      const contactTarget = Array.from(
        document.querySelectorAll<HTMLElement>(
          ".ov-side-rail .ov-rail-card:not(.ov-rail-card-priority)"
        )
      )
        .filter((c) => !c.querySelector(".ov-rail-progress-track, .ov-progress-bar"))
        .at(-1);

      if (!contactTarget) {
        allReady = false;
      } else if (!contactTarget.dataset.contactInjected) {
        contactTarget.dataset.contactInjected = "true";
        contactTarget.innerHTML = `
          <p class="section-label">YOUR PEOPLE PERSON</p>
          <div class="contact-identity">
            <div class="contact-avatar" aria-hidden="true">NT</div>
            <div class="contact-identity-text">
              <strong>Nicole Thornton</strong>
              <span>HR Manager</span>
            </div>
          </div>
          <p class="contact-blurb">Questions, nerves, confusion, or just want to say hi — Nicole's your person. Genuinely happy to help.</p>
          <div class="contact-details">
            <a class="contact-link contact-link--phone" href="tel:2565747528">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 11.5a19.79 19.79 0 01-3.07-8.67A2 2 0 012 .84h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 8.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>
              256-574-7528
            </a>
            <a class="contact-link contact-link--email" href="mailto:nicole.thornton@apirx.com">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,12 2,6"/></svg>
              nicole.thornton@apirx.com
            </a>
          </div>
        `;
      }

      return allReady;
    }

    if (!injectOverview()) {
      const id = requestAnimationFrame(() => {
        if (!injectOverview()) {
          setTimeout(injectOverview, 120);
        }
      });
      return () => cancelAnimationFrame(id);
    }
  }, [kind, experience, nextSection]);

  function toggleItem(sectionSlug: string, itemIndex: number) {
    setCheckedItems((current) => {
      const existing = current[sectionSlug] ?? [];
      const next = [...existing];
      next[itemIndex] = !next[itemIndex];
      return {
        ...current,
        [sectionSlug]: next,
      };
    });
  }

  function handleAcknowledge(section: Section) {
    const selected = checkedItems[section.slug] ?? [];
    const complete = selected.length === section.acknowledgment.items.length && selected.every(Boolean);
    if (!complete) {
      return;
    }

    startTransition(() => {
      void acknowledgeSection(EMPLOYEE_ID, section.slug, displayName).then((updated) => {
        setProgress(updated);
      });
    });
  }

  function handleToolkitComplete(roleToolkit: Toolkit) {
    if (!progress) {
      return;
    }

    startTransition(() => {
      void saveProgress(EMPLOYEE_ID, {
        display_name: displayName,
        current_section: roleToolkit.slug,
        completed_sections: progress.completed_sections,
        acknowledged_sections: progress.acknowledged_sections,
        toolkit_completed: true,
      }).then((updated) => {
        setProgress(updated);
      });
    });
  }

  async function handleLogin(nextName: string) {
    if (!progress) {
      return;
    }

    setIsSigningIn(true);
    setProfileName(nextName);
    localStorage.setItem(AUTH_NAME_KEY, nextName);

    try {
      const updated = await saveProgress(EMPLOYEE_ID, {
        display_name: nextName,
        current_section: progress.current_section,
        completed_sections: progress.completed_sections,
        acknowledged_sections: progress.acknowledged_sections,
        toolkit_completed: progress.toolkit_completed,
      });
      setProgress(updated);
    } catch {
      // Let the user continue even if the profile sync misses once.
    } finally {
      setIsSigningIn(false);
    }
  }

  function handleLogout() {
    setProfileName(null);
    localStorage.removeItem(AUTH_NAME_KEY);
  }

  if (loading) {
    return (
      <div className="status-screen">
        <div className="status-card">
          <p className="section-label">AAP/API Onboarding</p>
          <h1>Loading your experience...</h1>
          <p>Connecting to the onboarding API.</p>
        </div>
      </div>
    );
  }

  if (error || !experience || !progress) {
    return (
      <div className="status-screen">
        <div className="status-card">
          <p className="section-label">Setup needed</p>
          <h1>Backend not running.</h1>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!profileName) {
    return (
      <LoginScreen
        defaultName=""
        isPending={isSigningIn}
        onSubmit={handleLogin}
      />
    );
  }

  return (
    <div className={kind === "toolkit" ? "app-shell toolkit-shell" : kind === "section" ? "app-shell section-shell" : "app-shell"}>
      <aside className={kind === "toolkit" ? "side-rail toolkit-rail" : kind === "section" ? "side-rail section-rail" : "side-rail"}>
        {kind === "toolkit" ? (
          <ToolkitRail
            sections={sections}
            slug={slug}
            completedSections={completedSections}
            progressCount={progress.completed_sections.length}
            totalCount={sections.length}
            toolkitComplete={progress.toolkit_completed}
          />
        ) : kind === "section" ? (
          <SectionRail
            sections={sections}
            slug={slug}
            completedSections={completedSections}
            progressCount={progress.completed_sections.length}
            totalCount={sections.length}
            nextSection={nextSection}
            toolkitComplete={progress.toolkit_completed}
          />
        ) : (
          <>
            {/* Brand block — logo only */}
            <div className="brand-block">
              <img
                src="/logo.png"
                alt="AAP / API - American Associated Pharmacies"
                className="brand-logo-img"
              />
            </div>

            {/* Progress panel */}
            <div className="rail-panel progress-panel">
              <p className="section-label">Your progress</p>
              <strong>{completionPercent}%</strong>
              <p>{progress.completed_sections.length} of {sections.length} modules complete</p>
              <div className="rail-progress" aria-hidden="true">
                <div className="rail-progress-track">
                  <span className="rail-progress-fill" style={{ width: `${completionPercent}%` }} />
                </div>
              </div>
            </div>

            {/* Module nav */}
            <div className="rail-nav-group">
              <p className="rail-group-label">Core modules</p>
              <nav className="nav-stack">
                <Link className={kind === "overview" ? "nav-link active" : "nav-link"} href="/">
                  <span className="nav-link-num">
                    <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                      <rect x="1" y="1" width="3.5" height="3.5" rx="1" fill="currentColor"/>
                      <rect x="5.5" y="1" width="3.5" height="3.5" rx="1" fill="currentColor"/>
                      <rect x="1" y="5.5" width="3.5" height="3.5" rx="1" fill="currentColor"/>
                      <rect x="5.5" y="5.5" width="3.5" height="3.5" rx="1" fill="currentColor"/>
                    </svg>
                  </span>
                  <span className="nav-link-title">Overview</span>
                </Link>
                {sections.map((section, index) => (
                  <Link
                    key={section.slug}
                    className={slug === section.slug ? "nav-link active" : "nav-link"}
                    href={`/modules/${section.slug}`}
                  >
                    <span className="nav-link-num">
                      {completedSections.has(section.slug) ? (
                        <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                          <path d="M1.5 5L4 7.5L8.5 2.5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                      ) : (index + 1)}
                    </span>
                    <span className="nav-link-title">{section.title}</span>
                  </Link>
                ))}
              </nav>
            </div>

            {/* Toolkit link */}
            <div className="rail-nav-group">
              <p className="rail-group-label">Toolkit</p>
              <Link className="nav-link" href="/toolkits/hr-administrative-assistant">
                <span className="nav-link-num">
                  <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                    <path d="M5 1L6.18 3.4L9 3.81L7 5.76L7.47 8.56L5 7.31L2.53 8.56L3 5.76L1 3.81L3.82 3.4L5 1Z" fill="currentColor"/>
                  </svg>
                </span>
                <span className="nav-link-title">HR Admin Toolkit</span>
              </Link>
            </div>

            {/* User + sign out — sidebar bottom */}
            <button className="rail-user-chip" type="button" onClick={handleLogout}>
              <div className="rail-user-avatar" aria-hidden="true">
                {firstName.charAt(0).toUpperCase()}
              </div>
              <div className="rail-user-info">
                <strong>{firstName}</strong>
                <span>Sign out</span>
              </div>
              <svg className="rail-user-signout" width="13" height="13" viewBox="0 0 14 14" fill="none" aria-hidden="true">
                <path d="M5 2.25H3.875C3.379 2.25 2.902 2.447 2.552 2.798C2.201 3.148 2.004 3.625 2.004 4.121V9.879C2.004 10.375 2.201 10.852 2.552 11.202C2.902 11.553 3.379 11.75 3.875 11.75H5" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M8.25 9.75L11 7L8.25 4.25" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M11 7H5" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </>
        )}
      </aside>

      <main className={kind === "toolkit" ? "main-stage toolkit-stage" : kind === "section" ? "main-stage section-stage" : "main-stage"}>
        <header className={kind === "toolkit" ? "topbar toolkit-topbar" : kind === "section" ? "topbar section-topbar" : "topbar overview-topbar"}>
          <div>
            <p className="section-label">
              {kind === "toolkit" ? "Role-specific reference" : kind === "section" ? "General onboarding section" : "Onboarding overview"}
            </p>
          </div>
          {kind !== "overview" && (
            <div className="topbar-right">
              <div className="topbar-meta">
                <span>Welcome back</span>
                <strong>{firstName}</strong>
              </div>
              <button className="topbar-logout" type="button" onClick={handleLogout}>
                <span className="topbar-logout-icon" aria-hidden="true">
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M5 2.25H3.875C3.37868 2.25 2.90247 2.4471 2.55178 2.79779C2.20112 3.14848 2.004 3.62469 2.004 4.121V9.879C2.004 10.3753 2.20112 10.8515 2.55178 11.2022C2.90247 11.5529 3.37868 11.75 3.875 11.75H5" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M8.25 9.75L11 7L8.25 4.25" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M11 7H5" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </span>
                <span>Sign out</span>
              </button>
            </div>
          )}
        </header>

        {kind !== "overview" && (
          <section className="context-strip" aria-label="Current onboarding context">
            <article className="context-chip">
              <span>Now viewing</span>
              <strong>{contextTitle}</strong>
              <p>{contextType}</p>
            </article>
            {nextSection && (
              <article className="context-chip emphasis">
                <span>Next up</span>
                <strong>{nextSection.title}</strong>
                <Link className="inline-action" href={`/modules/${nextSection.slug}`}>
                  Continue
                </Link>
              </article>
            )}
          </section>
        )}

        {kind === "overview" && (
          <OverviewScreen experience={experience} progress={progress} nextSection={nextSection} firstName={firstName} />
        )}
        {kind === "section" && activeSection && (
          <SectionScreen
            section={activeSection}
            isAcknowledged={acknowledgedSections.has(activeSection.slug)}
            selections={checkedItems[activeSection.slug] ?? []}
            onToggle={toggleItem}
            onAcknowledge={handleAcknowledge}
            isPending={isPending}
          />
        )}
        {kind === "toolkit" && toolkit && (
          <ToolkitScreen toolkit={toolkit} complete={progress.toolkit_completed} onComplete={handleToolkitComplete} isPending={isPending} />
        )}
      </main>
    </div>
  );
}

type SectionProps = {
  section: Section;
  isAcknowledged: boolean;
  selections: boolean[];
  onToggle: (sectionSlug: string, itemIndex: number) => void;
  onAcknowledge: (section: Section) => void;
  isPending: boolean;
};

function SectionScreen({ section, isAcknowledged, selections, onToggle, onAcknowledge, isPending }: SectionProps) {
  const allChecked = selections.length === section.acknowledgment.items.length && selections.every(Boolean);
  const checkedCount = selections.filter(Boolean).length;
  const remainingChecks = Math.max(section.acknowledgment.items.length - checkedCount, 0);

  return (
    <div className="page-stack section-page">
      <section className="page-hero single-focus-hero section-hero">
        <div className="section-hero-copy">
          <p className="section-label">{section.eyebrow}</p>
          <h1>{section.title}</h1>
          <p className="lead">{section.summary}</p>
          <p className="purpose-line">{section.purpose}</p>
        </div>
        <aside className="summary-panel hero-support-panel">
          <p className="section-label">Focus areas</p>
          <div className="focus-list">
            {section.focuses.map((focus) => <span key={focus} className="focus-pill">{focus}</span>)}
          </div>
          <hr className="hero-support-divider" />
          <p className="section-label">Completion status</p>
          <div className="hero-progress-copy">
            <strong>{checkedCount}/{section.acknowledgment.items.length} checkpoints marked</strong>
            <p>
              {isAcknowledged
                ? "Section acknowledged and saved."
                : remainingChecks === 0
                  ? "Ready to mark complete."
                  : `${remainingChecks} check${remainingChecks === 1 ? "" : "s"} left.`}
            </p>
            <a className="inline-action" href="#section-acknowledgment">
              Jump to completion
            </a>
          </div>
        </aside>
      </section>

      <div className="jump-chip-row">
        <a className="jump-chip" href="#section-takeaways">Takeaways</a>
        <a className="jump-chip" href="#section-policy">Policy map</a>
        <a className="jump-chip emphasis" href="#section-acknowledgment">
          {isAcknowledged ? "\u2713 Acknowledged" : "Complete section"}
        </a>
      </div>

      <section className="section-band takeaway-band" id="section-takeaways">
        <div className="section-band-head">
          <p className="section-label">Core takeaways</p>
          <h2>Read this first</h2>
        </div>
        <div className="essential-grid compact-takeaways">
          {section.essentials.map((item) => (
            <article key={item.title} className="essential-card">
              <strong>{item.title}</strong>
              <p>{item.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section-band policy-band" id="section-policy">
        <div className="section-band-head">
          <p className="section-label">Policy structure</p>
          <h2>What the documents actually cover</h2>
        </div>
        <div className="policy-area-list">
          {section.policyAreas.map((area) => (
            <article key={area.title} className="policy-area">
              <h3>{area.title}</h3>
              <dl className="policy-list">
                {area.items.map((item) => (
                  <div key={item.label} className="policy-row">
                    <dt>{item.label}</dt>
                    <dd>{item.body}</dd>
                  </div>
                ))}
              </dl>
            </article>
          ))}
        </div>
      </section>

      <section className="content-columns section-support-grid">
        <div className="content-panel quiet-content-panel">
          <p className="section-label">What to do</p>
          <h3>Use this section in practice</h3>
          <ul className="plain-list">
            {section.actions.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
        <div className="content-panel warning-panel quiet-content-panel">
          <p className="section-label">Escalate when</p>
          <h3>Do not improvise these scenarios</h3>
          <ul className="plain-list">
            {section.escalation.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
      </section>

      <section className="content-panel acknowledgment-panel" id="section-acknowledgment">
        <p className="section-label">Acknowledge this section</p>
        <h3>{section.acknowledgment.title}</h3>
        <p>{section.acknowledgment.statement}</p>
        <div className="checklist-list">
          {section.acknowledgment.items.map((item, index) => (
            <button
              key={item}
              className={selections[index] ? "check-item active" : "check-item"}
              onClick={() => onToggle(section.slug, index)}
              type="button"
            >
              <span className="check-item-indicator" aria-hidden="true">
                {selections[index] && (
                  <svg width="11" height="11" viewBox="0 0 11 11" fill="none">
                    <path d="M1.5 5.5L4.5 8.5L9.5 2.5" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                )}
              </span>
              <strong>{item}</strong>
            </button>
          ))}
        </div>
        <button
          className="primary-action"
          disabled={isAcknowledged || !allChecked || isPending}
          onClick={() => onAcknowledge(section)}
          type="button"
        >
          {isAcknowledged ? "\u2713 Section acknowledged" : isPending ? "Saving..." : "Mark section complete"}
        </button>
      </section>
    </div>
  );
}

type SectionRailProps = {
  sections: Section[];
  slug?: string;
  completedSections: Set<string>;
  progressCount: number;
  totalCount: number;
  nextSection: Section | null;
  toolkitComplete: boolean;
};

function SectionRail({
  sections,
  slug,
  completedSections,
  progressCount,
  totalCount,
  nextSection,
  toolkitComplete,
}: SectionRailProps) {
  const progressPercent = totalCount ? Math.round((progressCount / totalCount) * 100) : 0;
  const activeSection = sections.find((section) => section.slug === slug);

  return (
    <div className="section-rail-inner">
      <div className="section-rail-header">
        <p className="section-label">AAP/API</p>
        <h1>Onboarding</h1>
        <div className="rail-progress" aria-hidden="true">
          <div className="rail-progress-track">
            <span className="rail-progress-fill" style={{ width: `${progressPercent}%` }} />
          </div>
          <div className="rail-progress-meta">
            <strong>{progressPercent}%</strong>
            <span>complete</span>
          </div>
        </div>
        {nextSection && (
          <Link className="section-rail-inline" href={`/modules/${nextSection.slug}`}>
            Next: {nextSection.title}
          </Link>
        )}
      </div>

      <div className="section-rail-context">
        <p className="section-label">Now in view</p>
        <strong>{activeSection ? activeSection.title : "Overview"}</strong>
        <p>{activeSection ? activeSection.eyebrow : "Start here, then move into the core modules."}</p>
        {nextSection && (
          <Link className="section-rail-inline" href={`/modules/${nextSection.slug}`}>
            {activeSection?.slug === nextSection.slug ? "Your next target" : `Up next: ${nextSection.title}`}
          </Link>
        )}
      </div>

      <div className="rail-nav-group">
        <p className="rail-group-label">Core onboarding</p>
        <nav className="section-rail-nav">
          <Link className={slug ? "section-rail-link" : "section-rail-link active"} href="/">
            <span>Overview</span>
          </Link>
          {sections.map((section, index) => (
            <Link
              key={section.slug}
              className={slug === section.slug ? "section-rail-link active" : "section-rail-link"}
              href={`/modules/${section.slug}`}
            >
              <span>{index + 1}. {section.title}</span>
              {completedSections.has(section.slug) && <em>✓</em>}
            </Link>
          ))}
        </nav>
      </div>

      <div className="section-rail-footer">
        <p className="rail-group-label">Role-specific</p>
        <Link className="section-rail-link" href="/toolkits/hr-administrative-assistant">
          <span>HR Admin Toolkit</span>
          {toolkitComplete && <em>✓</em>}
        </Link>
      </div>
    </div>
  );
}

type ToolkitProps = {
  toolkit: Toolkit;
  complete: boolean;
  onComplete: (toolkit: Toolkit) => void;
  isPending: boolean;
};

function ToolkitScreen({ toolkit, complete, onComplete, isPending }: ToolkitProps) {
  return (
    <div className="page-stack toolkit-page">
      <section className="page-hero single-focus-hero toolkit-hero">
        <div className="toolkit-hero-copy">
          <p className="section-label">{toolkit.eyebrow}</p>
          <h1>{toolkit.title}</h1>
          <p className="lead">{toolkit.summary}</p>
          <p className="purpose-line">{toolkit.purpose}</p>
          <div className="toolkit-callout">
            <p className="section-label">Use this when</p>
            <ul className="plain-list compact-list">
              {toolkit.whenToUse.map((item) => <li key={item}>{item}</li>)}
            </ul>
          </div>
        </div>
      </section>

      <div className="jump-chip-row">
        <a className="jump-chip" href="#toolkit-systems">Systems</a>
        <a className="jump-chip" href="#toolkit-playbooks">Playbooks</a>
        <a className="jump-chip emphasis" href="#toolkit-review">{complete ? "\u2713 Reviewed" : "Mark reviewed"}</a>
      </div>

      <section className="content-panel primary-panel systems-panel" id="toolkit-systems">
        <p className="section-label">Systems</p>
        <h3>Where the HR admin work happens</h3>
        <div className="system-list primary-system-list">
          {toolkit.systems.map((system) => (
            <article key={system.name} className="system-row">
              <div>
                <strong>{system.name}</strong>
                <span>{system.link}</span>
              </div>
              <p>{system.use}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="content-columns toolkit-secondary-grid">
        <div className="content-panel quiet-panel">
          <p className="section-label">Quick answers</p>
          <h3>Useful approved responses</h3>
          <div className="quick-answer-list">
            {toolkit.quickAnswers.map((item) => (
              <details key={item.question} className="quick-answer-item">
                <summary>{item.question}</summary>
                <p>{item.answer}</p>
                <span>{item.reference}</span>
              </details>
            ))}
          </div>
        </div>

        <div className="content-panel quiet-panel warning-panel soft-warning-panel">
          <p className="section-label">Escalate immediately</p>
          <h3>High-risk topics should leave the front desk fast</h3>
          <ul className="plain-list">
            {toolkit.escalateImmediately.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
      </section>

      <section className="content-panel quiet-panel" id="toolkit-playbooks">
        <p className="section-label">Playbooks</p>
        <h3>Use these patterns instead of improvising</h3>
        {toolkit.playbooks.map((playbook) => (
          <details key={playbook.title} className="playbook">
            <summary>{playbook.title}</summary>
            <p>{playbook.summary}</p>
            <div className="content-columns playbook-columns">
              <div>
                <h4>Do this</h4>
                <ul className="plain-list compact-list">
                  {playbook.doThis.map((item) => <li key={item}>{item}</li>)}
                </ul>
              </div>
              <div>
                <h4>Escalate when</h4>
                <ul className="plain-list compact-list">
                  {playbook.escalateWhen.map((item) => <li key={item}>{item}</li>)}
                </ul>
              </div>
            </div>
          </details>
        ))}
      </section>

      <section className="content-columns toolkit-support-grid">
        <div className="content-panel quiet-panel">
          <p className="section-label">Contacts</p>
          <h3>People to pull in</h3>
          <div className="contact-list">
            {toolkit.contacts.map((contact) => (
              <article key={contact.email} className="contact-card">
                <strong>{contact.name}</strong>
                <span>{contact.role}</span>
                <span>{contact.phone}</span>
                <p>{contact.email}</p>
              </article>
            ))}
          </div>
        </div>

        <div className="content-panel acknowledgment-panel quiet-panel" id="toolkit-review">
          <p className="section-label">Toolkit review</p>
          <h3>{toolkit.acknowledgment.title}</h3>
          <p>{toolkit.acknowledgment.statement}</p>
          <ul className="plain-list compact-list">
            {toolkit.acknowledgment.items.map((item) => <li key={item}>{item}</li>)}
          </ul>
          <button
            className="primary-action"
            disabled={complete || isPending}
            onClick={() => onComplete(toolkit)}
            type="button"
          >
            {complete ? "\u2713 Toolkit marked complete" : isPending ? "Saving..." : "Mark toolkit reviewed"}
          </button>
        </div>
      </section>
    </div>
  );
}

type ToolkitRailProps = {
  sections: Section[];
  slug?: string;
  completedSections: Set<string>;
  progressCount: number;
  totalCount: number;
  toolkitComplete: boolean;
};

function ToolkitRail({ sections, slug, completedSections, progressCount, totalCount, toolkitComplete }: ToolkitRailProps) {
  const progressPercent = totalCount ? Math.round((progressCount / totalCount) * 100) : 0;

  return (
    <div className="toolkit-rail-inner">
      <div className="toolkit-rail-header">
        <p className="section-label">AAP/API</p>
        <h1>Toolkit</h1>
        <div className="rail-progress" aria-hidden="true">
          <div className="rail-progress-track">
            <span className="rail-progress-fill" style={{ width: `${progressPercent}%` }} />
          </div>
          <div className="rail-progress-meta">
            <strong>{progressPercent}%</strong>
            <span>general flow</span>
          </div>
        </div>
      </div>

      <div className="section-rail-context toolkit-context">
        <p className="section-label">Mode</p>
        <strong>Role-specific reference</strong>
        <p>{toolkitComplete ? "Toolkit reviewed and saved." : "Complete this lane separately from the core flow."}</p>
        <Link className="section-rail-inline" href="/">
          {"\u2190"} Return to overview
        </Link>
      </div>

      <div className="rail-nav-group">
        <p className="rail-group-label">General onboarding</p>
        <nav className="toolkit-rail-nav">
          <Link className="toolkit-rail-link" href="/">
            <span>Overview</span>
          </Link>
          {sections.map((section, index) => (
            <Link
              key={section.slug}
              className={slug === section.slug ? "toolkit-rail-link active" : "toolkit-rail-link"}
              href={`/modules/${section.slug}`}
            >
              <span>{index + 1}. {section.title}</span>
              {completedSections.has(section.slug) && <em>{"\u2713"}</em>}
            </Link>
          ))}
          <Link className="toolkit-rail-link active toolkit-link-current" href="/toolkits/hr-administrative-assistant">
            <span>HR Admin Toolkit</span>
            <em>{toolkitComplete ? "\u2713" : "Here"}</em>
          </Link>
        </nav>
      </div>
    </div>
  );
}
