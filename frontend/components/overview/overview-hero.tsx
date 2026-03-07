import Link from "next/link";

import type { Section } from "@/lib/types";

type OverviewHeroProps = {
  nextSection: Section | null;
  completedCount: number;
  totalCount: number;
};

export function OverviewHero({ nextSection, completedCount, totalCount }: OverviewHeroProps) {
  const isStarting = completedCount === 0;
  const isComplete = !nextSection;

  const ctaLabel = isComplete
    ? "Onboarding complete ✓"
    : isStarting
      ? `Start: ${nextSection.title}`
      : `Continue: ${nextSection.title}`;

  const headlineLine1 = isComplete
    ? "You're all caught up."
    : isStarting
      ? "Day one starts here."
      : "Keep the momentum going.";

  const headlineLine2 = isComplete
    ? "Every section reviewed."
    : isStarting
      ? "Let's get you up to speed."
      : `${completedCount} of ${totalCount} done.`;

  const subCopy = isComplete
    ? "All core onboarding sections have been completed and saved. Check the role-specific toolkit if you haven't already."
    : isStarting
      ? "This is your onboarding path. Work through each lesson in order — every section builds on the last. No skipping, no surprises."
      : "You've already made real progress. Keep going, one lesson at a time, and you'll have the full picture before you know it.";

  return (
    <section className="ov-hero">
      <div className="ov-hero-texture" aria-hidden="true" />
      <div className="ov-hero-copy">
        <p className="section-label">Your onboarding course</p>
        <h1>
          {headlineLine1}
          <br />
          {headlineLine2}
        </h1>
        <p className="ov-hero-lead">{subCopy}</p>
        <div className="ov-hero-actions">
          {nextSection ? (
            <Link className="primary-action" href={`/modules/${nextSection.slug}`}>
              {ctaLabel}
            </Link>
          ) : (
            <span className="primary-action done-action">{ctaLabel}</span>
          )}
          <span className="ov-hero-progress">
            {completedCount} / {totalCount} lessons complete
          </span>
        </div>
      </div>

      <aside className="ov-hero-expect">
        <p className="section-label">What to expect</p>
        <h3>Structured. Practical. No fluff.</h3>
        <ul className="ov-expect-list">
          <li>Lessons run in order — orientation first, then policy, then review.</li>
          <li>Each lesson tells you why it matters before diving in.</li>
          <li>Your progress saves automatically every time you complete a section.</li>
          <li>One clear next step at all times — no guessing what's next.</li>
        </ul>
      </aside>
    </section>
  );
}
