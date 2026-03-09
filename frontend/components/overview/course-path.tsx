import Link from "next/link";

import type { ProgressRecord, Section } from "@/lib/types";

import { LessonStep } from "./lesson-step";
import type { LessonState } from "./lesson-step";

type CoursePathProps = {
  sections: Section[];
  progress: ProgressRecord;
  nextSection: Section | null;
  activeLesson: Section | null;
  firstName: string;
};

export function CoursePath({ sections, progress, nextSection, activeLesson, firstName }: CoursePathProps) {
  const completedCount = progress.completed_sections.length;
  const totalCount = sections.length;
  const completionPercent = totalCount ? Math.round((completedCount / totalCount) * 100) : 0;
  const remainingMinutes = sections
    .filter((section) => !progress.completed_sections.includes(section.slug))
    .reduce((sum, section) => sum + section.estimatedMinutes, 0);
  const completedSet = new Set(progress.completed_sections);

  return (
    <section className="ov-path" aria-label="Core onboarding path">
      <div className="ov-path-header">
        <div>
          <p className="section-label">Core path</p>
          <h2>{firstName}'s onboarding path</h2>
        </div>
        <div className="ov-path-stats">
          <strong>{completedCount}/{totalCount} done</strong>
          <span>{remainingMinutes} min left</span>
        </div>
      </div>

      <div className="ov-path-progress">
        <div className="ov-progress-bar" aria-hidden="true">
          <div className="ov-progress-fill" style={{ width: `${completionPercent}%` }} />
        </div>
        {nextSection ? (
          <Link className="inline-action" href={`/modules/${nextSection.slug}`}>
            Open next module
          </Link>
        ) : (
          <p className="ov-complete-note">Core path complete.</p>
        )}
      </div>

      <ol className="ov-journey">
        {sections.map((section, index) => {
          const complete = completedSet.has(section.slug);
          const current = !complete && activeLesson?.slug === section.slug;
          const isNext = !complete && nextSection?.slug === section.slug && !current;
          const state: LessonState = complete ? "completed" : current ? "current" : isNext ? "next" : "upcoming";

          return (
            <LessonStep
              key={section.slug}
              section={section}
              index={index}
              state={state}
              isLast={index === sections.length - 1}
            />
          );
        })}
      </ol>
    </section>
  );
}
