import Link from "next/link";

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
  const remainingMinutes = experience.sections
    .filter((section) => !progress.completed_sections.includes(section.slug))
    .reduce((sum, section) => sum + section.estimatedMinutes, 0);
  const averageMinutes = totalCount
    ? Math.round(experience.sections.reduce((sum, section) => sum + section.estimatedMinutes, 0) / totalCount)
    : 0;

  const currentSection = experience.sections.find((s) => s.slug === progress.current_section);
  const activeLesson =
    currentSection && !progress.completed_sections.includes(currentSection.slug)
      ? currentSection
      : nextSection;

  const supportContact = experience.track?.support_contact ?? null;
  const supportFirstName = supportContact?.name.split(" ")[0] ?? "Support";
  const supportPhoneDigits = supportContact ? supportContact.phone.replace(/\D/g, "") : "";

  // Build context string for the AI tip — pulls from next module or current state
  const tipContext = nextSection
    ? `${nextSection.title}: ${nextSection.summary ?? ""}`.trim()
    : completedCount === 0
      ? "General onboarding — employee is just getting started at AAP/API Rx"
      : "Employee has just completed all core onboarding modules at AAP/API Rx";

  return (
    <div className="ov-page">
      <div className="ov-layout-grid">
        <div className="ov-main-column">
          <OverviewHero
            firstName={firstName}
            nextSection={nextSection}
            completedCount={completedCount}
            totalCount={totalCount}
            completionPercent={completionPercent}
            remainingCount={remainingCount}
            remainingMinutes={remainingMinutes}
          />

          <section className="ov-overview-notes" aria-label="Helpful overview notes">
            <article className="ov-note-card">
              <p className="section-label">How it runs</p>
              <h3>One module at a time, in the right order.</h3>
              <p>No hunting around. We keep the next step close.</p>
            </article>

            <article className="ov-note-card">
              <p className="section-label">Good to know</p>
              <h3>Most modules land in about {averageMinutes} minutes.</h3>
              <p>Easy to pick up, easy to pause, and saved the whole way through.</p>
            </article>
          </section>

          <CoursePath
            sections={experience.sections}
            progress={progress}
            nextSection={nextSection}
            activeLesson={activeLesson}
            firstName={firstName}
          />
        </div>

        <aside className="ov-side-rail" aria-label="Tips and support">
          {/* Coach Tip card — replaces the old Next Up card */}
          <CoachTipCard context={tipContext} variant="rail" />

          <article className="ov-rail-card ov-rail-card-secondary">
            <p className="section-label">Progress</p>
            <h3>{completionPercent}% through the core path.</h3>
            <div className="ov-rail-progress-track" aria-hidden="true">
              <span className="ov-rail-progress-fill" style={{ width: `${completionPercent}%` }} />
            </div>
            <ul className="ov-rail-list">
              <li>{remainingCount} module{remainingCount === 1 ? "" : "s"} left.</li>
              <li>About {remainingMinutes} minutes to finish the essentials.</li>
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
