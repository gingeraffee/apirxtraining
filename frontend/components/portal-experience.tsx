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
              {nextSection && (
                <Link className="inline-action" href={`/modules/${nextSection.slug}`}>
                  Continue with {nextSection.title}
                </Link>
              )}
            </div>

            <div className="rail-panel">
              <p className="section-label">General flow</p>
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
              <p className="section-label">Separate role-specific lane</p>
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
          </div>
        </header>

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
  return (
    <div className="page-stack">
      <section className="page-hero">
        <div>
          <p className="section-label">Welcome to AAP/API</p>
          <h1>{experience.organization.headline}</h1>
          <p className="lead">{experience.organization.story}</p>
          <p className="purpose-line">{experience.organization.mission}</p>
        </div>
        <div className="summary-panel">
          <p className="section-label">What this page is for</p>
          <h3>Get oriented, then move through the core flow one section at a time.</h3>
          <ul className="plain-list compact-list">
            <li>The main path is for all new employees.</li>
            <li>The HR Administrative Assistant toolkit stays separate.</li>
            <li>Use HR when a policy question becomes specific or sensitive.</li>
          </ul>
          {nextSection && (
            <Link className="primary-action" href={`/modules/${nextSection.slug}`}>
              Start {nextSection.title}
            </Link>
          )}
        </div>
      </section>

      <section className="content-columns overview-columns">
        <div className="content-panel">
          <p className="section-label">Core onboarding flow</p>
          <h3>One focused section at a time</h3>
          <ol className="roadmap-list">
            {experience.sections.map((section, index) => {
              const complete = progress.completed_sections.includes(section.slug);
              return (
                <li key={section.slug} className="roadmap-item">
                  <div className="roadmap-index">{index + 1}</div>
                  <div className="roadmap-copy">
                    <div className="roadmap-head">
                      <strong>{section.title}</strong>
                      <span className={complete ? "status-chip done" : "status-chip"}>{complete ? "Done" : `${section.estimatedMinutes} min`}</span>
                    </div>
                    <p>{section.summary}</p>
                    <Link className="inline-action" href={`/modules/${section.slug}`}>
                      Open section
                    </Link>
                  </div>
                </li>
              );
            })}
          </ol>
        </div>

        <div className="stack-column">
          <section className="content-panel">
            <p className="section-label">Support contacts</p>
            <h3>Use the right escalation path early</h3>
            <div className="contact-list">
              {experience.contacts.slice(0, 3).map((contact) => (
                <article key={contact.email} className="contact-card">
                  <strong>{contact.name}</strong>
                  <span>{contact.role}</span>
                  <span>{contact.phone}</span>
                  <p>{contact.note}</p>
                </article>
              ))}
            </div>
          </section>

          <section className="content-panel subtle-panel">
            <p className="section-label">Role-specific content</p>
            <h3>Keep the HR toolkit in its own lane</h3>
            <p>The HR Administrative Assistant toolkit is a separate operational reference. It should not crowd the core employee onboarding path.</p>
            <Link className="inline-action" href="/toolkits/hr-administrative-assistant">
              Open the HR toolkit
            </Link>
          </section>
        </div>
      </section>

      <section className="content-panel">
        <p className="section-label">Values and culture</p>
        <h3>What should feel visible in the work</h3>
        <div className="value-grid compact-values">
          {experience.organization.values.map((value) => (
            <article key={value.name} className="value-card">
              <strong>{value.name}</strong>
              <p>{value.body}</p>
            </article>
          ))}
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
        </aside>
      </section>

      <section className="section-band takeaway-band">
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

      <section className="section-band policy-band">
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

      <section className="content-panel acknowledgment-panel">
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

      <div className="section-rail-footer">
        <p className="section-label">Separate role-specific lane</p>
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

      <section className="content-panel primary-panel systems-panel">
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

      <section className="content-panel quiet-panel">
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

        <div className="content-panel acknowledgment-panel quiet-panel">
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
  );
}