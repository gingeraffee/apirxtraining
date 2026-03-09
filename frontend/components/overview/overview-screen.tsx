import type { Contact, ExperienceContent, ProgressRecord, Section } from "@/lib/types";

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
  const supportFirstName = supportContact?.name.split(" ")[0] ?? "Support";
  const supportPhoneDigits = supportContact ? supportContact.phone.replace(/\D/g, "") : "";
  const tipContext = nextSection
    ? `${nextSection.title}: ${nextSection.summary}`
    : "The employee completed the tracked launch path and may revisit Resource Hub for reference.";

  return (
    <div className="ov-page">
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
              <h3>{supportFirstName} is your person.</h3>
              <p>{supportContact.role}. Helpful answers, actual human.</p>
              <div className="ov-rail-actions">
                <a className="inline-action" href={`mailto:${supportContact.email}`}>
                  Email {supportFirstName}
                </a>
                <a className="inline-action" href={`tel:${supportPhoneDigits}`}>
                  Call {supportFirstName}
                </a>
              </div>
            </article>
          )}
        </aside>
      </div>
    </div>
  );
}
