import Link from "next/link";

import type { SupplementalPage } from "@/lib/types";

type OverviewHeroProps = {
  firstName: string;
  nextSectionSlug: string | null;
  nextSectionTitle: string | null;
  completedCount: number;
  totalCount: number;
  completionPercent: number;
  remainingCount: number;
  supplementalPages: SupplementalPage[];
};

export function OverviewHero({
  firstName,
  nextSectionSlug,
  nextSectionTitle,
  completedCount,
  totalCount,
  completionPercent,
  remainingCount,
  supplementalPages,
}: OverviewHeroProps) {
  const isComplete = completedCount >= totalCount && totalCount > 0;
  const comingSoonCount = supplementalPages.filter((page) => page.state === "coming_soon").length;

  return (
    <section className="ov-hero" aria-label="Onboarding overview">
      <div className="ov-hero-texture" aria-hidden="true" />

      <div className="ov-hero-copy">
        <div className="ov-hero-head">
          <p className="section-label">AAP Start</p>
          <span className={`ov-hero-status${isComplete ? " done" : ""}`}>
            {isComplete ? "Launch path complete" : `${completedCount} of ${totalCount} complete`}
          </span>
        </div>

        <h1>{isComplete ? `You're all set, ${firstName}.` : `Welcome in, ${firstName}.`}</h1>
        <p className="ov-hero-lead">
          {isComplete
            ? "You finished the tracked launch path. The Resource Hub stays here whenever you need a quick reset or a live reference."
            : "AAP Start keeps the essentials in one clean path so you can focus on one module at a time and still know where to find support."}
        </p>

        <div className="ov-hero-actions">
          {nextSectionSlug && nextSectionTitle ? (
            <div className="ov-hero-next">
              <p className="ov-hero-next-label">
                <span className="ov-hero-next-tag">Next up</span>
                <span className="ov-hero-next-title">{nextSectionTitle}</span>
              </p>
              <p className="ov-hero-next-meta">
                {remainingCount} module{remainingCount === 1 ? "" : "s"} left in the tracked path.
              </p>
              <Link className="primary-action" href={`/modules/${nextSectionSlug}`}>
                Open next module
              </Link>
            </div>
          ) : (
            <div className="ov-hero-next">
              <span className="primary-action done-action">Tracked path complete</span>
              <p className="ov-hero-next-meta">Keep Resource Hub close for live files and support contacts.</p>
            </div>
          )}
        </div>

        <div className="overview-chip-row" aria-label="Overview highlights">
          <span className="overview-chip">9 live modules</span>
          <span className="overview-chip">Manual completion only</span>
          <span className="overview-chip">{comingSoonCount} coming soon page{comingSoonCount === 1 ? "" : "s"}</span>
          <span className="overview-chip">{completionPercent}% complete</span>
        </div>
      </div>
    </section>
  );
}
