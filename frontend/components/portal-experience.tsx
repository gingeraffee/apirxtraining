"use client";

import Link from "next/link";
import { useEffect, useState, useTransition } from "react";

import { acknowledgeSection, fetchExperience, fetchProgress, saveProgress } from "@/lib/api";
import type { ExperienceContent, ProgressRecord, Section, Toolkit } from "@/lib/types";

type PortalKind = "overview" | "section" | "toolkit";

type PortalExperienceProps = {
  kind: PortalKind;
  slug?: string;
};

const EMPLOYEE_ID = "demo-employee";
const DISPLAY_NAME = "New Hire Demo";

export function PortalExperience({ kind, slug }: PortalExperienceProps) {
  const [experience, setExperience] = useState<ExperienceContent | null>(null);
  const [progress, setProgress] = useState<ProgressRecord | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [checkedItems, setCheckedItems] = useState<Record<string, boolean[]>>({});
  const [isPending, startTransition] = useTransition();

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
        display_name: DISPLAY_NAME,
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
    if (kind === "section" && slug && progress) {
      void syncCurrentSection(slug);
    }
    if (kind === "toolkit" && slug && progress) {
      void syncCurrentSection(slug);
    }
  }, [kind, slug, progress]);

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
      void acknowledgeSection(EMPLOYEE_ID, section.slug, DISPLAY_NAME).then((updated) => {
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
        display_name: DISPLAY_NAME,
        current_section: roleToolkit.slug,
        completed_sections: progress.completed_sections,
        acknowledged_sections: progress.acknowledged_sections,
        toolkit_completed: true,
      }).then((updated) => {
        setProgress(updated);
      });
    });
  }

  if (loading) {
    return <div className="status-screen">Loading the onboarding experience...</div>;
  }

  if (error || !experience || !progress) {
    return (
      <div className="status-screen">
        <div className="status-card">
          <p className="section-label">API Required</p>
          <h1>Frontend is ready. Backend needs to be running.</h1>
          <p>{error}</p>
        </div>
      </div>
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
            <div className="brand-block">
              <p className="section-label">AAP/API</p>
              <h1>Onboarding</h1>
              <p>{experience.organization.tagline}</p>
            </div>

            <div className="rail-panel progress-panel">
              <p className="section-label">Progress</p>
              <strong>{completionPercent}% complete</strong>
              <p>{progress.completed_sections.length} of {sections.length} general sections reviewed.</p>
              <div className="rail-progress" aria-hidden="true">
                <div className="rail-progress-track">
                  <span className="rail-progress-fill" style={{ width: `${completionPercent}%` }} />
                </div>
              </div>
              {nextSection && (
                <Link className="inline-action" href={`/modules/${nextSection.slug}`}>
                  Continue with {nextSection.title}
                </Link>
              )}
            </div>

            <div className="rail-panel">
              <p className="rail-group-label">General flow</p>
              <nav className="nav-stack">
                <Link className={kind === "overview" ? "nav-link active" : "nav-link"} href="/">
                  <span>Overview</span>
                </Link>
                {sections.map((section, index) => (
                  <Link
                    key={section.slug}
                    className={slug === section.slug ? "nav-link active" : "nav-link"}
                    href={`/modules/${section.slug}`}
                  >
                    <div>
                      <strong>{index + 1}. {section.title}</strong>
                      <p>{section.summary}</p>
                    </div>
                    <span className={completedSections.has(section.slug) ? "status-chip done" : "status-chip"}>
                      {completedSections.has(section.slug) ? "Done" : `${section.estimatedMinutes} min`}
                    </span>
                  </Link>
                ))}
              </nav>
            </div>

            <div className="rail-panel">
              <p className="rail-group-label">Separate role-specific lane</p>
              <Link className="nav-link" href="/toolkits/hr-administrative-assistant">
                <div>
                  <strong>HR Administrative Assistant Toolkit</strong>
                  <p>Operational reference only. Not part of the core new-hire path.</p>
                </div>
                <span className={progress.toolkit_completed ? "status-chip done" : "status-chip"}>
                  {progress.toolkit_completed ? "Reviewed" : "Separate"}
                </span>
              </Link>
            </div>
          </>
        )}
      </aside>

      <main className={kind === "toolkit" ? "main-stage toolkit-stage" : kind === "section" ? "main-stage section-stage" : "main-stage"}>
        <header className={kind === "toolkit" ? "topbar toolkit-topbar" : kind === "section" ? "topbar section-topbar" : "topbar"}>
          <div>
            <p className="section-label">
              {kind === "toolkit" ? "Role-specific reference" : kind === "section" ? "General onboarding section" : "General onboarding"}
            </p>
            <h2>{DISPLAY_NAME}</h2>
          </div>
          <div className="topbar-meta">
            <span>{progress.updated_at ? "Progress saved" : "Progress ready"}</span>
            <strong>{progress.completed_sections.length}/{sections.length}</strong>
            <div className="topbar-progress-track" aria-hidden="true">
              <span className="topbar-progress-fill" style={{ width: `${completionPercent}%` }} />
            </div>
          </div>
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
                  Continue section
                </Link>
              </article>
            )}
            <article className="context-chip">
              <span>Completion</span>
              <strong>{completionPercent}%</strong>
              <p>{progress.completed_sections.length} of {sections.length} core sections complete</p>
            </article>
          </section>
        )}

        {kind === "overview" && (
          <OverviewScreen experience={experience} progress={progress} nextSection={nextSection} />
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

type OverviewProps = {
  experience: ExperienceContent;
  progress: ProgressRecord;
  nextSection: Section | null;
};

function OverviewScreen({ experience, progress, nextSection }: OverviewProps) {
  const completedCount = progress.completed_sections.length;
  const totalCount = experience.sections.length;
  const completionPercent = totalCount ? Math.round((completedCount / totalCount) * 100) : 0;
  const remainingCount = Math.max(totalCount - completedCount, 0);
  const remainingMinutes = experience.sections
    .filter((section) => !progress.completed_sections.includes(section.slug))
    .reduce((runningTotal, section) => runningTotal + section.estimatedMinutes, 0);
  const currentSection = experience.sections.find((section) => section.slug === progress.current_section);
  const activeLesson = currentSection && !progress.completed_sections.includes(currentSection.slug)
    ? currentSection
    : nextSection;
  const nextStepLabel = nextSection
    ? completedCount === 0
      ? `Start ${nextSection.title}`
      : `Continue ${nextSection.title}`
    : "Review completed lessons";

  const supportContact = {
    name: "Nicole Thornton",
    role: "HR Manager",
    phone: "256-574-7528",
    email: "nicole.thornton330@gmail.com",
  };

  const nicoleCard = [
    "BEGIN:VCARD",
    "VERSION:3.0",
    "FN:Nicole Thornton",
    "N:Thornton;Nicole;;;",
    "TITLE:HR Manager",
    "TEL;TYPE=WORK,VOICE:256-574-7528",
    "EMAIL;TYPE=INTERNET:nicole.thornton330@gmail.com",
    "END:VCARD",
  ].join("\n");
  const encodedVCard = encodeURIComponent(nicoleCard);
  const vCardDownloadUrl = `data:text/vcard;charset=utf-8,${encodedVCard}`;

  return (
    <div className="page-stack overview-page">
      <section className="page-hero overview-hero">
        <div className="overview-hero-copy">
          <p className="section-label">Welcome to your onboarding course</p>
          <h1>A guided onboarding flow built around what new employees need first.</h1>
          <p className="lead">You are in the right place. This onboarding path is practical, clear, and built to help you feel confident fast.</p>
          <p className="purpose-line">Work lesson by lesson, complete each checkpoint, and keep moving with one clear next step.</p>
          <div className="overview-hero-actions">
            {nextSection ? (
              <Link className="primary-action" href={`/modules/${nextSection.slug}`}>
                {nextStepLabel}
              </Link>
            ) : (
              <span className="primary-action done-action">Core path complete</span>
            )}
            <span className="overview-hero-note">{completedCount}/{totalCount} lessons complete</span>
          </div>
        </div>

        <aside className="summary-panel overview-summary-panel">
          <p className="section-label">What to expect</p>
          <h3>Clear lessons. Practical takeaways. Real momentum.</h3>
          <ul className="plain-list compact-list">
            <li>Each lesson explains what it covers and why it matters.</li>
            <li>You always have a clear current lesson and next lesson.</li>
            <li>Your progress and time remaining stay visible in one place.</li>
          </ul>
        </aside>
      </section>

      <section className="content-panel overview-journey" aria-label="Progress and course path">
        <div className="overview-journey-head">
          <div>
            <p className="section-label">Your onboarding path</p>
            <h3>Progress and lesson journey</h3>
          </div>
          <div className="overview-journey-meta">
            <strong>{completedCount}/{totalCount} complete</strong>
            <span>{remainingMinutes} minutes remaining</span>
          </div>
        </div>

        <div className="overview-journey-progress">
          <div className="rail-progress" aria-hidden="true">
            <div className="rail-progress-track">
              <span className="rail-progress-fill" style={{ width: `${completionPercent}%` }} />
            </div>
          </div>
          {nextSection ? (
            <Link className="inline-action journey-action" href={`/modules/${nextSection.slug}`}>
              Next lesson: {nextSection.title}
            </Link>
          ) : (
            <p className="journey-complete-note">You have completed all core lessons.</p>
          )}
        </div>

        <ol className="overview-journey-list">
          {experience.sections.map((section, index) => {
            const complete = progress.completed_sections.includes(section.slug);
            const current = !complete && activeLesson?.slug === section.slug;
            const nextUp = !complete && nextSection?.slug === section.slug && !current;
            const state = complete ? "Completed" : current ? "Current" : nextUp ? "Up next" : "Upcoming";
            const keyTakeaway = section.essentials[0]?.title ?? section.focuses[0] ?? "Key lesson takeaway included.";

            return (
              <li key={section.slug} className={complete ? "journey-item done" : current ? "journey-item current" : nextUp ? "journey-item next" : "journey-item"}>
                <div className="journey-step">{index + 1}</div>
                <div className="journey-content">
                  <div className="journey-top">
                    <strong className="journey-title">{section.title}</strong>
                    <span className="journey-state">{state} | {section.estimatedMinutes} min</span>
                  </div>
                  <p className="journey-why">Why it matters: {section.purpose}</p>
                  <p className="journey-covers">Covers: {section.summary}</p>
                  <p className="journey-covers">Key takeaway: {keyTakeaway}</p>
                  {!complete && (
                    <Link className={current || nextUp ? "primary-action compact-primary" : "inline-action"} href={`/modules/${section.slug}`}>
                      {current || nextUp ? "Open lesson" : "Preview lesson"}
                    </Link>
                  )}
                </div>
              </li>
            );
          })}
        </ol>
      </section>

      <section className="content-panel overview-help">
        <div className="overview-help-copy">
          <p className="section-label">Need help?</p>
          <h3>{supportContact.name}, {supportContact.role}</h3>
          <p>Use your assigned HR contact anytime a lesson feels unclear or a policy scenario needs direct guidance.</p>
        </div>

        <div className="overview-help-contact">
          <p>Phone: <a href="tel:2565747528">{supportContact.phone}</a></p>
          <p>Email: <a href="mailto:nicole.thornton330@gmail.com">{supportContact.email}</a></p>
          <div className="overview-help-actions">
            <a className="inline-action" href="tel:2565747528">Call Nicole</a>
            <a className="inline-action" href="mailto:nicole.thornton330@gmail.com">Email Nicole</a>
            <a className="inline-action" href={vCardDownloadUrl} download="nicole-thornton.vcf">Save contact card</a>
          </div>
          <p className="overview-help-note">Virtual business card area is ready for QR rollout.</p>
        </div>
      </section>
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
          <div className="hero-support-divider" />
          <p className="section-label">Completion status</p>
          <div className="hero-progress-copy">
            <strong>{checkedCount}/{section.acknowledgment.items.length} checkpoints marked</strong>
            <p>{isAcknowledged ? "Section acknowledged and saved." : remainingChecks === 0 ? "Ready to mark complete." : `${remainingChecks} checks left before completion.`}</p>
            <a className="inline-action" href="#section-acknowledgment">
              Jump to completion
            </a>
          </div>
        </aside>
      </section>

      <div className="jump-chip-row">
        <a className="jump-chip" href="#section-takeaways">Takeaways</a>
        <a className="jump-chip" href="#section-policy">Policy map</a>
        <a className="jump-chip emphasis" href="#section-acknowledgment">{isAcknowledged ? "Acknowledged" : "Complete section"}</a>
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
          <h2>What the documents actually cover here</h2>
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
            <button key={item} className={selections[index] ? "check-item active" : "check-item"} onClick={() => onToggle(section.slug, index)} type="button">
              <span>{selections[index] ? "Checked" : "Mark"}</span>
              <strong>{item}</strong>
            </button>
          ))}
        </div>
        <button className="primary-action" disabled={isAcknowledged || !allChecked || isPending} onClick={() => onAcknowledge(section)} type="button">
          {isAcknowledged ? "Section acknowledged" : isPending ? "Saving..." : "Mark section complete"}
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
            <span>core flow complete</span>
          </div>
        </div>
        {nextSection && (
          <Link className="section-rail-inline" href={`/modules/${nextSection.slug}`}>
            Continue with {nextSection.title}
          </Link>
        )}
      </div>

      <div className="section-rail-context">
        <p className="section-label">Now in view</p>
        <strong>{activeSection ? activeSection.title : "Overview"}</strong>
        <p>{activeSection ? `${activeSection.estimatedMinutes} min section` : "Start here, then move into the core modules."}</p>
        {nextSection && (
          <Link className="section-rail-inline" href={`/modules/${nextSection.slug}`}>
            {activeSection?.slug === nextSection.slug ? "This section is your next completion target" : `Up next: ${nextSection.title}`}
          </Link>
        )}
      </div>

      <div className="rail-nav-group">
        <p className="rail-group-label">Core onboarding</p>
        <nav className="section-rail-nav">
          <Link className={slug ? "section-rail-link" : "section-rail-link active"} href="/">
            <span>Overview</span>
            <em>{progressCount === totalCount ? "Done" : "Start here"}</em>
          </Link>
          {sections.map((section, index) => (
            <Link
              key={section.slug}
              className={slug === section.slug ? "section-rail-link active" : "section-rail-link"}
              href={`/modules/${section.slug}`}
            >
              <span>{index + 1}. {section.title}</span>
              <em>{completedSections.has(section.slug) ? "Done" : `${section.estimatedMinutes} min`}</em>
            </Link>
          ))}
        </nav>
      </div>

      <div className="section-rail-footer">
        <p className="rail-group-label">Separate role-specific lane</p>
        <Link className="section-rail-link" href="/toolkits/hr-administrative-assistant">
          <span>HR Administrative Assistant Toolkit</span>
          <em>{toolkitComplete ? "Reviewed" : "Separate"}</em>
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
        <a className="jump-chip emphasis" href="#toolkit-review">{complete ? "Reviewed" : "Mark reviewed"}</a>
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
          <button className="primary-action" disabled={complete || isPending} onClick={() => onComplete(toolkit)} type="button">
            {complete ? "Toolkit marked complete" : isPending ? "Saving..." : "Mark toolkit reviewed"}
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
            <span>general flow done</span>
          </div>
        </div>
      </div>

      <div className="section-rail-context toolkit-context">
        <p className="section-label">Mode</p>
        <strong>Role-specific reference</strong>
        <p>{toolkitComplete ? "Toolkit reviewed and saved." : "Complete this lane without mixing it into the core flow."}</p>
        <Link className="section-rail-inline" href="/">
          Return to overview
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
              {completedSections.has(section.slug) && <em>Done</em>}
            </Link>
          ))}
          <Link className="toolkit-rail-link active toolkit-link-current" href="/toolkits/hr-administrative-assistant">
            <span>HR Administrative Assistant Toolkit</span>
            <em>{toolkitComplete ? "Reviewed" : "Current"}</em>
          </Link>
        </nav>
      </div>
    </div>
  );
}
