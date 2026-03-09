"use client";

import Link from "next/link";
import { useEffect, useMemo, useState, useTransition } from "react";

import { acknowledgeSection, fetchExperience, fetchProgress, saveProgress } from "@/lib/api";
import type { Contact, ExperienceContent, ProgressRecord, Section, SupplementalPage } from "@/lib/types";
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
  const supplementalPages = experience?.supplementalPages ?? [];
  const activeSection = sections.find((section) => section.slug === slug) ?? null;
  const activeSupplemental = supplementalPages.find((page) => page.slug === slug) ?? null;
  const completedSections = new Set(progress?.completed_sections ?? []);
  const acknowledgedSections = new Set(progress?.acknowledged_sections ?? []);
  const overviewNextSection = sections.find((section) => !completedSections.has(section.slug)) ?? null;
  const sectionSequenceNext = activeSection
    ? sections[sections.findIndex((section) => section.slug === activeSection.slug) + 1] ?? null
    : null;
  const contextNextSection = activeSection ? sectionSequenceNext : overviewNextSection;
  const completionPercent = sections.length
    ? Math.round(((progress?.completed_sections.length ?? 0) / sections.length) * 100)
    : 0;
  const supportContact = useMemo(() => {
    if (!experience) {
      return null;
    }
    return experience.contacts.find((contact) => contact.id === experience.track.supportContactId) ?? null;
  }, [experience]);

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
      });
      setProgress(updated);
    } catch {
      // Ignore background sync failures.
    }
  }

  useEffect(() => {
    if (!profileName || !progress || !slug) {
      return;
    }

    void syncCurrentSection(slug);
  }, [slug, progress, profileName]);

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
    const items = section.acknowledgment.items;
    const selected = checkedItems[section.slug] ?? [];
    const complete = section.acknowledgment.mode === "manual"
      || items.length === 0
      || (selected.length === items.length && selected.every(Boolean));

    if (!complete) {
      return;
    }

    startTransition(() => {
      void acknowledgeSection(EMPLOYEE_ID, section.slug, displayName).then((updated) => {
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
          <p className="section-label">AAP Start</p>
          <h1>Loading your launch experience...</h1>
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
    return <LoginScreen defaultName="" isPending={isSigningIn} onSubmit={handleLogin} />;
  }

  const contextTitle = kind === "overview"
    ? "Overview"
    : activeSection?.title ?? activeSupplemental?.title ?? "Page not found";
  const contextType = activeSection
    ? "Tracked module"
    : activeSupplemental?.state === "coming_soon"
      ? "Visible, untracked launch preview"
      : activeSupplemental
        ? "Visible, untracked reference page"
        : "Launch overview";

  return (
    <div className={kind === "overview" ? "app-shell" : "app-shell section-shell"}>
      <aside className="side-rail">
        <div className="brand-block portal-brand-block">
          <div className="portal-brand portal-brand-sidebar">
            <span className="portal-brand-overline">Launch onboarding</span>
            <strong>AAP Start</strong>
            <span className="portal-brand-subline">American Associated Pharmacies</span>
          </div>
        </div>

        <div className="rail-panel progress-panel">
          <p className="section-label">Tracked progress</p>
          <strong>{completionPercent}%</strong>
          <p>{progress.completed_sections.length} of {sections.length} live modules complete</p>
          <div className="rail-progress" aria-hidden="true">
            <div className="rail-progress-track">
              <span className="rail-progress-fill" style={{ width: `${completionPercent}%` }} />
            </div>
          </div>
        </div>

        <div className="rail-nav-group">
          <p className="rail-group-label">Launch path</p>
          <nav className="nav-stack">
            <Link className={kind === "overview" ? "nav-link active" : "nav-link"} href="/">
              <span className="nav-link-num">•</span>
              <span className="nav-link-title">Overview</span>
            </Link>
            {sections.map((section, index) => (
              <Link
                key={section.slug}
                className={slug === section.slug ? "nav-link active" : "nav-link"}
                href={`/modules/${section.slug}`}
              >
                <span className="nav-link-num">{completedSections.has(section.slug) ? "✓" : index + 1}</span>
                <span className="nav-link-title">{section.title}</span>
              </Link>
            ))}
          </nav>
        </div>

        <div className="rail-nav-group">
          <p className="rail-group-label">Also in AAP Start</p>
          <nav className="nav-stack">
            {supplementalPages.map((page) => (
              <Link
                key={page.slug}
                className={slug === page.slug ? "nav-link active" : "nav-link"}
                href={`/modules/${page.slug}`}
              >
                <span className="nav-link-num">{page.state === "coming_soon" ? "…" : "↗"}</span>
                <span className="nav-link-title">{page.title}</span>
                <span className={`nav-link-badge ${page.state}`}>{page.state === "coming_soon" ? "Soon" : "Live"}</span>
              </Link>
            ))}
          </nav>
        </div>

        {supportContact && (
          <div className="rail-panel contact-rail-panel">
            <p className="section-label">Support</p>
            <strong>{supportContact.name}</strong>
            <p>{supportContact.role}</p>
            <a className="inline-action" href={`mailto:${supportContact.email}`}>Email support</a>
          </div>
        )}

        <button className="rail-user-chip" type="button" onClick={handleLogout}>
          <div className="rail-user-avatar" aria-hidden="true">{firstName.charAt(0).toUpperCase()}</div>
          <div className="rail-user-info">
            <strong>{firstName}</strong>
            <span>Sign out</span>
          </div>
        </button>
      </aside>

      <main className={kind === "overview" ? "main-stage" : "main-stage section-stage"}>
        <header className={kind === "overview" ? "topbar overview-topbar" : "topbar section-topbar"}>
          <div>
            <p className="section-label">{experience.brand.portalName}</p>
            <h1 className="topbar-title">{contextTitle}</h1>
          </div>
          <div className="topbar-right">
            <div className="topbar-meta">
              <span>Now viewing</span>
              <strong>{contextType}</strong>
            </div>
            <button className="topbar-logout" type="button" onClick={handleLogout}>
              <span>Sign out</span>
            </button>
          </div>
        </header>

        {kind !== "overview" && (
          <section className="context-strip" aria-label="Current onboarding context">
            <article className="context-chip">
              <span>Now viewing</span>
              <strong>{contextTitle}</strong>
              <p>{contextType}</p>
            </article>
            {contextNextSection && (
              <article className="context-chip emphasis">
                <span>Next in line</span>
                <strong>{contextNextSection.title}</strong>
                <Link className="inline-action" href={`/modules/${contextNextSection.slug}`}>
                  Continue
                </Link>
              </article>
            )}
          </section>
        )}

        {kind === "overview" && (
          <OverviewScreen experience={experience} progress={progress} nextSection={overviewNextSection} firstName={firstName} />
        )}

        {kind !== "overview" && activeSection && (
          <SectionScreen
            section={activeSection}
            isAcknowledged={acknowledgedSections.has(activeSection.slug)}
            selections={checkedItems[activeSection.slug] ?? []}
            onToggle={toggleItem}
            onAcknowledge={handleAcknowledge}
            isPending={isPending}
          />
        )}

        {kind !== "overview" && !activeSection && activeSupplemental && (
          <SupplementalPageScreen page={activeSupplemental} contacts={experience.contacts} />
        )}

        {kind !== "overview" && !activeSection && !activeSupplemental && (
          <div className="status-screen inline-status-screen">
            <div className="status-card">
              <p className="section-label">AAP Start</p>
              <h1>Page not found.</h1>
              <p>This launch page is not part of the current experience payload.</p>
            </div>
          </div>
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
  const showChecklist = section.acknowledgment.mode !== "manual" && section.acknowledgment.items.length > 0;
  const allChecked = !showChecklist || (selections.length === section.acknowledgment.items.length && selections.every(Boolean));
  const checkedCount = selections.filter(Boolean).length;

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
            <strong>{isAcknowledged ? "Completed" : showChecklist ? `${checkedCount}/${section.acknowledgment.items.length} ready` : "Manual completion"}</strong>
            <p>{isAcknowledged ? "Section saved." : section.acknowledgment.statement}</p>
            <a className="inline-action" href="#section-acknowledgment">Jump to finish</a>
          </div>
        </aside>
      </section>

      <div className="jump-chip-row">
        <a className="jump-chip" href="#section-takeaways">Takeaways</a>
        <a className="jump-chip" href="#section-policy">Policy map</a>
        <a className="jump-chip emphasis" href="#section-acknowledgment">{isAcknowledged ? "Completed" : "Finish module"}</a>
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
          <h2>What to keep in mind</h2>
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
          <h3>Use this in practice</h3>
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
        <p className="section-label">Finish this module</p>
        <h3>{section.acknowledgment.title}</h3>
        <p>{section.acknowledgment.statement}</p>

        {showChecklist && (
          <div className="checklist-list">
            {section.acknowledgment.items.map((item, index) => (
              <button
                key={item}
                className={selections[index] ? "check-item active" : "check-item"}
                onClick={() => onToggle(section.slug, index)}
                type="button"
              >
                <span className="check-item-indicator" aria-hidden="true">{selections[index] ? "✓" : ""}</span>
                <strong>{item}</strong>
              </button>
            ))}
          </div>
        )}

        <button
          className="primary-action"
          disabled={isAcknowledged || !allChecked || isPending}
          onClick={() => onAcknowledge(section)}
          type="button"
        >
          {isAcknowledged ? "Section complete" : isPending ? "Saving..." : "Mark module complete"}
        </button>
      </section>
    </div>
  );
}

type SupplementalPageScreenProps = {
  page: SupplementalPage;
  contacts: Contact[];
};

function SupplementalPageScreen({ page, contacts }: SupplementalPageScreenProps) {
  const contactMap = new Map(contacts.map((contact) => [contact.id, contact]));

  return (
    <div className="page-stack section-page supplemental-page">
      <section className="page-hero single-focus-hero section-hero supplemental-hero">
        <div className="section-hero-copy">
          <p className="section-label">{page.eyebrow}</p>
          <h1>{page.title}</h1>
          <p className="lead">{page.summary}</p>
          <p className="purpose-line">{page.description}</p>
        </div>
        <aside className="summary-panel hero-support-panel supplemental-status-panel">
          <p className="section-label">Launch status</p>
          <strong>{page.state === "coming_soon" ? page.callout ?? "Coming Soon" : "Live"}</strong>
          <p>{page.state === "coming_soon" ? "Visible in nav, excluded from progress." : "Reference page, excluded from progress."}</p>
        </aside>
      </section>

      {page.state === "coming_soon" && (
        <section className="content-panel quiet-content-panel supplemental-callout-panel">
          <p className="section-label">Preview</p>
          <h3>Visible on purpose, not live yet.</h3>
          <div className="essential-grid compact-takeaways">
            {(page.content ?? []).map((item) => (
              <article key={item.title} className="essential-card">
                <strong>{item.title}</strong>
                <p>{item.body}</p>
              </article>
            ))}
          </div>
        </section>
      )}

      {page.state === "live" && (
        <section className="resource-hub-shell">
          {(page.resourceCategories ?? []).map((category) => (
            <article key={category.id} className="content-panel quiet-content-panel resource-category-panel">
              <p className="section-label">Resource category</p>
              <h3>{category.title}</h3>
              <p>{category.description}</p>
              <div className="resource-item-list">
                {category.items.map((item) => {
                  const contact = item.contactId ? contactMap.get(item.contactId) : null;
                  return (
                    <article key={item.id} className="resource-item-card">
                      <p className="section-label">{item.type === "contact" ? "Contact" : item.type === "file" ? "File" : "Link"}</p>
                      <h4>{item.title}</h4>
                      <p>{item.description}</p>
                      {contact ? (
                        <div className="resource-contact-stack">
                          <strong>{contact.name}</strong>
                          <span>{contact.role}</span>
                          {contact.email && <a className="inline-action" href={`mailto:${contact.email}`}>Email</a>}
                          {contact.phone && <a className="inline-action" href={`tel:${contact.phone.replace(/\D/g, "")}`}>Call</a>}
                        </div>
                      ) : item.href ? (
                        <a className="inline-action" href={item.href} download={item.download}>
                          {item.type === "file" ? "Open file" : "Open link"}
                        </a>
                      ) : null}
                    </article>
                  );
                })}
              </div>
            </article>
          ))}
        </section>
      )}
    </div>
  );
}
