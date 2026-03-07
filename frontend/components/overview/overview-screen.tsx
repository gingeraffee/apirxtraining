import type { ExperienceContent, ProgressRecord, Section } from "@/lib/types";

import { OverviewHero } from "./overview-hero";
import { CoursePath } from "./course-path";
import { SupportContact } from "./support-contact";

type OverviewScreenProps = {
  experience: ExperienceContent;
  progress: ProgressRecord;
  nextSection: Section | null;
};

export function OverviewScreen({ experience, progress, nextSection }: OverviewScreenProps) {
  const completedCount = progress.completed_sections.length;
  const totalCount = experience.sections.length;
  const currentSection = experience.sections.find(
    (s) => s.slug === progress.current_section,
  );
  const activeLesson =
    currentSection && !progress.completed_sections.includes(currentSection.slug)
      ? currentSection
      : nextSection;

  const supportContact = experience.track.support_contact;

  return (
    <div className="ov-page">
      <OverviewHero
        nextSection={nextSection}
        completedCount={completedCount}
        totalCount={totalCount}
      />
      <CoursePath
        sections={experience.sections}
        progress={progress}
        nextSection={nextSection}
        activeLesson={activeLesson}
      />
      <SupportContact contact={supportContact} />
    </div>
  );
}
