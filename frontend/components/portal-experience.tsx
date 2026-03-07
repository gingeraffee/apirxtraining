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
          <p className="eyebrow">API Required</p>
          <h1>Frontend is ready. Backend needs to be running.</h1>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell">
      <aside className="side-rail">
        <div className="brand-block">
          <p className="eyebrow">AAP/API</p>
          <h1>Onboarding Platform</h1>
          <p>{experience.organization.tagline}</p>
        </div>

        <div className="rail-panel">
          <p className="rail-label">Core flow</p>
          <nav className="nav-stack">
            <Link className={kind === "overview" ? "nav-link active" : "nav-link"} href="/">
              Overview
            </Link>
            {sections.map((section, index) => (
              <Link
                key={section.slug}
                className={slug === section.slug ? "nav-link active" : "nav-link"}
                href={`/modules/${section.slug}`}
              >
                <span>{index + 1}. {section.title}</span>
                <span className={completedSections.has(section.slug) ? "chip done" : "chip"}>
                  {completedSections.has(section.slug) ? "Done" : `${section.estimatedMinutes} min`}
                </span>
              </Link>
            ))}
          </nav>
        </div>

        <div className="rail-panel accent-panel">
          <p className="rail-label">Role-specific lane</p>
          <Link className={kind === "toolkit" ? "nav-link active" : "nav-link"} href="/toolkits/hr-administrative-assistant">
            <span>HR Administrative Assistant Toolkit</span>
            <span className={progress.toolkit_completed ? "chip done" : "chip"}>
              {progress.toolkit_completed ? "Complete" : "Optional"}
            </span>
          </Link>
        </div>

        <div className="rail-panel compact">
          <p className="rail-label">Need backup?</p>
          {experience.contacts.slice(0, 2).map((contact) => (
            <div key={contact.email} className="contact-mini">
              <strong>{contact.name}</strong>
              <span>{contact.role}</span>
              <span>{contact.phone}</span>
            </div>
          ))}
        </div>
      </aside>

      <main className="main-stage">
        <header className="topbar">
          <div>
            <p className="eyebrow">New hire lane</p>
            <h2>{DISPLAY_NAME}</h2>
          </div>
          <div className="progress-pill">
            <span>{completionPercent}% complete</span>
            <strong>{progress.completed_sections.length}/{sections.length} sections</strong>
          </div>
        </header>

        {kind === "overview" && <OverviewScreen experience={experience} progress={progress} completionPercent={completionPercent} />}
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
  completionPercent: number;
};

function OverviewScreen({ experience, progress, completionPercent }: OverviewProps) {
  return (
    <div className="page-stack">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">Welcome to AAP/API</p>
          <h1>{experience.organization.headline}</h1>
          <p className="hero-copy">{experience.organization.story}</p>
        </div>
        <div className="hero-metrics">
          <div className="metric-card primary">
            <span>Current momentum</span>
            <strong>{completionPercent}%</strong>
            <p>{progress.completed_sections.length} of {experience.sections.length} core sections complete.</p>
          </div>
          <div className="metric-card secondary">
            <span>Next move</span>
            <strong>{progress.current_section ?? experience.sections[0]?.slug}</strong>
            <p>Use the rail to jump into any section, then acknowledge it when the essentials are clear.</p>
          </div>
        </div>
      </section>

      <section className="stats-grid">
        {experience.dashboardStats.map((stat) => (
          <article key={stat.label} className="glass-card stat-card">
            <span>{stat.label}</span>
            <strong>{stat.value}</strong>
            <p>{stat.detail}</p>
          </article>
        ))}
      </section>

      <section className="content-grid two-up">
        <div className="glass-card">
          <p className="eyebrow">Values in motion</p>
          <h3>What the culture rewards</h3>
          <div className="value-list">
            {experience.organization.values.map((value) => (
              <article key={value.name} className="mini-card">
                <strong>{value.name}</strong>
                <p>{value.body}</p>
              </article>
            ))}
          </div>
        </div>
        <div className="glass-card">
          <p className="eyebrow">Support map</p>
          <h3>Real people, clear escalation</h3>
          <div className="contact-list">
            {experience.contacts.map((contact) => (
              <article key={contact.email} className="contact-card">
                <strong>{contact.name}</strong>
                <span>{contact.role}</span>
                <span>{contact.phone}</span>
                <p>{contact.note}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section-card-grid">
        {experience.sections.map((section, index) => {
          const complete = progress.completed_sections.includes(section.slug);
          return (
            <article key={section.slug} className="section-card">
              <div className="section-card-head">
                <span className="sequence">{index + 1}</span>
                <span className={complete ? "chip done" : "chip"}>{complete ? "Done" : `${section.estimatedMinutes} min`}</span>
              </div>
              <h3>{section.title}</h3>
              <p>{section.summary}</p>
              <p className="punchline">{section.punchline}</p>
              <Link className="action-link" href={`/modules/${section.slug}`}>
                Open section
              </Link>
            </article>
          );
        })}
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
    <div className="page-stack">
      <section className="hero-panel section-hero">
        <div>
          <p className="eyebrow">{section.eyebrow}</p>
          <h1>{section.title}</h1>
          <p className="hero-copy">{section.summary}</p>
          <p className="punchline">{section.punchline}</p>
        </div>
        <div className="fact-stack">
          {section.quickFacts.map((fact) => (
            <article key={fact.label} className="fact-card">
              <span>{fact.label}</span>
              <strong>{fact.value}</strong>
            </article>
          ))}
        </div>
      </section>

      <section className="card-grid">
        {section.highlightCards.map((card) => (
          <article key={card.title} className={`glass-card tone-${card.tone}`}>
            <h3>{card.title}</h3>
            <p>{card.body}</p>
          </article>
        ))}
      </section>

      <section className="content-grid two-up">
        <div className="glass-card">
          <p className="eyebrow">Flow</p>
          <h3>What to know in order</h3>
          <div className="timeline-list">
            {section.timeline.map((item) => (
              <article key={item.title} className="timeline-card">
                <span>{item.label}</span>
                <strong>{item.title}</strong>
                <p>{item.body}</p>
              </article>
            ))}
          </div>
        </div>
        <div className="glass-card">
          <p className="eyebrow">Keep this close</p>
          <h3>Takeaways and reminders</h3>
          <ul className="bullet-list">
            {section.takeaways.map((item) => <li key={item}>{item}</li>)}
          </ul>
          <div className="divider" />
          <ul className="bullet-list subtle">
            {section.reminders.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
      </section>

      <section className="content-grid two-up">
        <div className="glass-card">
          <p className="eyebrow">Resources</p>
          <h3>Fast-reference notes</h3>
          <div className="resource-list">
            {section.resources.map((resource) => (
              <article key={resource.title} className="mini-card">
                <strong>{resource.title}</strong>
                <p>{resource.body}</p>
              </article>
            ))}
          </div>
        </div>
        <div className="glass-card">
          <p className="eyebrow">FAQ</p>
          <h3>Answers worth keeping handy</h3>
          {section.faq.map((item) => (
            <details key={item.question} className="faq-item">
              <summary>{item.question}</summary>
              <p>{item.answer}</p>
            </details>
          ))}
        </div>
      </section>

      <section className="glass-card acknowledgement-panel">
        <p className="eyebrow">Acknowledge</p>
        <h3>{section.acknowledgment.title}</h3>
        <p>{section.acknowledgment.statement}</p>
        <div className="checklist-grid">
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

type ToolkitProps = {
  toolkit: Toolkit;
  complete: boolean;
  onComplete: (toolkit: Toolkit) => void;
  isPending: boolean;
};

function ToolkitScreen({ toolkit, complete, onComplete, isPending }: ToolkitProps) {
  return (
    <div className="page-stack">
      <section className="hero-panel section-hero">
        <div>
          <p className="eyebrow">{toolkit.eyebrow}</p>
          <h1>{toolkit.title}</h1>
          <p className="hero-copy">{toolkit.summary}</p>
          <p className="punchline">{toolkit.punchline}</p>
        </div>
        <div className="fact-stack">
          <article className="fact-card">
            <span>Reference depth</span>
            <strong>{toolkit.estimatedMinutes} min</strong>
          </article>
          <article className="fact-card">
            <span>Purpose</span>
            <strong>Fast routing</strong>
          </article>
        </div>
      </section>

      <section className="card-grid">
        {toolkit.overviewCards.map((card, index) => (
          <article key={card.title} className={`glass-card tone-${index === 0 ? "red" : index === 1 ? "cyan" : "navy"}`}>
            <h3>{card.title}</h3>
            <p>{card.body}</p>
          </article>
        ))}
      </section>

      <section className="content-grid two-up">
        <div className="glass-card">
          <p className="eyebrow">Systems</p>
          <h3>Where the work happens</h3>
          <div className="resource-list">
            {toolkit.systems.map((system) => (
              <article key={system.name} className="mini-card">
                <strong>{system.name}</strong>
                <span>{system.link}</span>
                <p>{system.use}</p>
              </article>
            ))}
          </div>
        </div>
        <div className="glass-card">
          <p className="eyebrow">Escalation contacts</p>
          <h3>Who to call when it turns specific</h3>
          <div className="contact-list">
            {toolkit.escalationContacts.map((contact) => (
              <article key={contact.email} className="contact-card">
                <strong>{contact.name}</strong>
                <span>{contact.role}</span>
                <span>{contact.phone}</span>
                <p>{contact.email}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="glass-card">
        <p className="eyebrow">Playbooks</p>
        <h3>Approved response patterns</h3>
        {toolkit.playbooks.map((playbook) => (
          <details key={playbook.title} className="faq-item" open>
            <summary>{playbook.title}</summary>
            <p>{playbook.body}</p>
            <ul className="bullet-list">
              {playbook.steps.map((step) => <li key={step}>{step}</li>)}
            </ul>
            <div className="divider" />
            <ul className="bullet-list subtle">
              {playbook.escalateWhen.map((item) => <li key={item}>{item}</li>)}
            </ul>
          </details>
        ))}
      </section>

      <section className="glass-card acknowledgement-panel">
        <p className="eyebrow">Toolkit finish</p>
        <h3>Keep this lane separate and operational</h3>
        <ul className="bullet-list">
          {toolkit.reminders.map((item) => <li key={item}>{item}</li>)}
        </ul>
        <button className="primary-action" disabled={complete || isPending} onClick={() => onComplete(toolkit)} type="button">
          {complete ? "Toolkit marked complete" : isPending ? "Saving..." : "Mark toolkit reviewed"}
        </button>
      </section>
    </div>
  );
}


