import Link from "next/link";

import type { Section } from "@/lib/types";

type OverviewHeroProps = {
  nextSection: Section | null;
  completedCount: number;
  totalCount: number;
};

export function OverviewHero({ nextSection, completedCount, totalCount }: OverviewHeroProps) {
  const ctaLabel = nextSection
    ? completedCount === 0
      ? `Begin ${nextSection.title}`
      : `Continue ${nextSection.title}`
    : "Onboarding complete";

  return (
    <section className="ov-hero">
      <div className="ov-hero-copy">
        <p className="section-label">Your onboarding course</p>
        <h1>A guided onboarding flow built around what new employees need first.</h1>
        <p className="ov-hero-lead">
          This is your main onboarding path. Each lesson is structured in a clear order,
          designed to help you build confidence and clarity from day one.
        </p>
        <p className="ov-hero-sub">
          Work lesson by lesson, complete each checkpoint, and keep moving forward
          with one clear next step.
        </p>
        <div className="ov-hero-actions">
          {nextSection ? (
            <Link className="primary-action" href={`/modules/${nextSection.slug}`}>
              {ctaLabel}
            </Link>
          ) : (
            <span className="primary-action done-action">Core path complete</span>
          )}
          <span className="ov-hero-progress">
            {completedCount} of {totalCount} lessons complete
          </span>
        </div>
      </div>

      <aside className="ov-hero-expect">
        <p className="section-label">What to expect</p>
        <h3>Clear lessons. Practical takeaways. Real momentum.</h3>
        <ul className="ov-expect-list">
          <li>Lessons are ordered from orientation basics to final review.</li>
          <li>Each lesson explains what it covers and why it matters.</li>
          <li>Your progress and time remaining are always visible.</li>
          <li>One clear next step keeps you moving forward.</li>
        </ul>
      </aside>
    </section>
  );
}
