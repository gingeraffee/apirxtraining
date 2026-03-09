import type { ExperienceContent, ProgressRecord, Section } from "@/lib/types";

import { OverviewHero } from "./overview-hero";
import { CoursePath } from "./course-path";
import { CoachTipCard } from "./coach-tip-card";

type OverviewScreenProps = {
  experience: ExperienceContent;
  progress: ProgressRecord;
  nextSection: Section | null;
  firstName: string;
};

export function OverviewScreen({ experience, progress, nextSection, firstName }: OverviewScreenProps) {
  const completedCount = progress.completed_sections.length;
  const totalCount = experience.sections.length;
  const completionPercent = totalCount ? Math.round((completedCount / totalCount) * 100) : 0;
  const remainingCount = Math.max(totalCount - completedCount, 0);
  const currentSection = experience.sections.find((section) => section.slug === progress.current_section);
  const activeLesson = currentSection && !progress.completed_sections.includes(currentSection.slug)
    ? currentSection
    : nextSection;

  const supportContact = experience.contacts.find((contact) => contact.id === experience.track.supportContactId) ?? null;
  const escalationContact = experience.contacts.find((contact) => contact.id === "brandy-hooper") ?? null;
  const supportPhoneDigits = supportContact ? supportContact.phone.replace(/\D/g, "") : "";
  const escalationPhoneDigits = escalationContact ? escalationContact.phone.replace(/\D/g, "") : "";
  const tipContext = nextSection
    ? `${nextSection.title}: ${nextSection.summary}`
    : "The employee completed the tracked launch path and may revisit Resource Hub for reference.";

  return (
    <div className="ov-page portal-page portal-page--overview">
      <div className="ov-layout-grid">
        <div className="ov-main-column">
          <OverviewHero
            firstName={firstName}
            nextSectionSlug={nextSection?.slug ?? null}
            nextSectionTitle={nextSection?.title ?? null}
            completedCount={completedCount}
            totalCount={totalCount}
            completionPercent={completionPercent}
            remainingCount={remainingCount}
            supplementalPages={experience.supplementalPages}
          />

          <section className="ov-overview-notes" aria-label="Helpful overview notes">
            <article className="ov-note-card">
              <p className="section-label">How it runs</p>
              <h3>Manual completion, one clear finish line.</h3>
              <p>The path only tracks the nine live modules. Supplemental pages stay visible without changing progress.</p>
            </article>

            <article className="ov-note-card">
              <p className="section-label">Keep close</p>
              <h3>Resource Hub stays available.</h3>
              <p>Use it for the handbook file, support contacts, and quick relaunches into the right module.</p>
            </article>
          </section>

          <CoursePath
            sections={experience.sections}
            progress={progress}
            nextSection={nextSection}
            activeLesson={activeLesson}
            firstName={firstName}
          />

          <section className="supplemental-showcase" aria-label="Supplemental pages">
            <div className="supplemental-showcase-head">
              <p className="section-label">Beyond the tracked path</p>
              <h2>Still visible, not counted.</h2>
            </div>
            <div className="supplemental-grid">
              {experience.supplementalPages.map((page) => (
                <article key={page.slug} className={`supplemental-card ${page.state === "coming_soon" ? "coming-soon" : "live"}`}>
                  <div className="supplemental-card-head">
                    <p className="section-label">{page.eyebrow}</p>
                    <span className="supplemental-badge">{page.state === "coming_soon" ? "Coming Soon" : "Live"}</span>
                  </div>
                  <h3>{page.title}</h3>
                  <p>{page.summary}</p>
                  <a className="inline-action" href={`/modules/${page.slug}`}>
                    {page.state === "coming_soon" ? "Preview page" : "Open Resource Hub"}
                  </a>
                </article>
              ))}
            </div>
          </section>
        </div>

        <aside className="ov-side-rail" aria-label="Tips and support">
          <CoachTipCard context={tipContext} variant="rail" />

          <article className="ov-rail-card ov-rail-card-secondary">
            <p className="section-label">Progress</p>
            <h3>{completionPercent}% through the tracked path.</h3>
            <div className="ov-rail-progress-track" aria-hidden="true">
              <span className="ov-rail-progress-fill" style={{ width: `${completionPercent}%` }} />
            </div>
            <ul className="ov-rail-list">
              <li>{remainingCount} module{remainingCount === 1 ? "" : "s"} left.</li>
              <li>Supplemental pages stay out of progress on purpose.</li>
            </ul>
          </article>

          {supportContact && (
            <article className="ov-rail-card ov-rail-card-support">
              <p className="section-label">Questions</p>
              <h3>{supportContact.name}</h3>
              <p>{supportContact.role}</p>
              <div className="question-contact-stack">
                <div className="question-contact-row">
                  <span>Email</span>
                  <a href={`mailto:${supportContact.email}`}>{supportContact.email}</a>
                </div>
                <div className="question-contact-row">
                  <span>Phone</span>
                  <a href={`tel:${supportPhoneDigits}`}>{supportContact.phone}</a>
                </div>
              </div>
              <p className="question-contact-note">{supportContact.note}</p>
              {escalationContact && (
                <div className="question-escalation-block">
                  <p className="question-escalation-label">Escalation support</p>
                  <strong>{escalationContact.name}</strong>
                  <span>{escalationContact.role}</span>
                  <div className="question-contact-stack question-contact-stack--secondary">
                    <div className="question-contact-row">
                      <span>Email</span>
                      <a href={`mailto:${escalationContact.email}`}>{escalationContact.email}</a>
                    </div>
                    <div className="question-contact-row">
                      <span>Phone</span>
                      <a href={`tel:${escalationPhoneDigits}`}>{escalationContact.phone}</a>
                    </div>
                  </div>
                </div>
              )}
            </article>
          )}
        </aside>
      </div>
    </div>
  );
}
