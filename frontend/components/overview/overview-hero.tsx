import Link from "next/link";

import type { Section } from "@/lib/types";

type OverviewHeroProps = {
  firstName: string;
  nextSection: Section | null;
  completedCount: number;
  totalCount: number;
  completionPercent: number;
  remainingCount: number;
  remainingMinutes: number;
};

function pick<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

// ── COPY POOLS ────────────────────────────────────────────────

const startingHeadlines = (n: string) => [
  `Welcome aboard, ${n}.`,
  `Let's get you started, ${n}.`,
  `Good to have you here, ${n}.`,
  `Ready when you are, ${n}.`,
  `Your journey starts here, ${n}.`,
  `Everything's set, ${n}.`,
];

const startingSubCopy = [
  "Everything's laid out and ready. Your next step is always one click away — no hunting required.",
  "The path is clear and the order is set. Just focus on one module at a time.",
  "We've done the organizing — you just have to show up. Let's get the first one out of the way.",
  "No guesswork, no clutter. Each step unlocks as you go.",
  "Your full onboarding path is mapped out below. The first module is the hardest to start — so let's start it.",
  "Short modules, clear sequence, automatic saves. This is as low-friction as onboarding gets.",
];

const startingStatus = ["Ready to go", "Let's do this", "First up", "Just getting started"];

const inProgressHeadlines = (n: string) => [
  `You're getting settled in, ${n}.`,
  `Making moves, ${n}.`,
  `Good progress, ${n}.`,
  `You're in the groove, ${n}.`,
  `Keep going, ${n}.`,
  `Looking solid, ${n}.`,
];

const inProgressSubCopy = [
  "A few key modules down, a few left to go. We keep the path clear so you can keep moving.",
  "You've got the rhythm now. The rest of the path follows the same pattern.",
  "Each module you finish is one less thing to worry about later. You're doing great.",
  "Still in the thick of it, but the finish line is coming into view.",
  "Most of the heavy lifting is behind you now. The next few are quick.",
  "Consistent progress beats rushing. You're exactly where you should be.",
];

const inProgressStatusEarly = ["Good start", "Off and running", "Building momentum", "First steps done"];
const inProgressStatusMid   = ["In stride", "Getting there", "Halfway there", "Momentum building"];
const inProgressStatusLate  = ["Home stretch", "Almost done", "Nearly there", "Final stretch"];

const completeHeadlines = (n: string) => [
  `You nailed it, ${n}.`,
  `All done, ${n}.`,
  `That's a wrap, ${n}.`,
  `You crushed it, ${n}.`,
  `Onboarding complete, ${n}.`,
  `You made it, ${n}.`,
];

const completeSubCopy = [
  "The essentials are locked in. Revisit anything you need, or dip into the toolkit when you have a minute.",
  "Every module is checked off. You're fully equipped for what comes next.",
  "Core onboarding is behind you. Everything you covered is always a click away if you need a refresher.",
  "That's everything in the core path. Well done — go make your mark.",
  "You've covered the basics, the policies, and everything in between. You're officially in.",
  "All of it's saved and ready whenever you need it. Nothing to do but get to work.",
];

const completeStatus = ["All set", "Done and dusted", "Complete", "Locked in"];

// ── COMPONENT ─────────────────────────────────────────────────

export function OverviewHero({
  firstName,
  nextSection,
  completedCount,
  totalCount,
  completionPercent,
  remainingCount,
  remainingMinutes,
}: OverviewHeroProps) {
  const isStarting = completedCount === 0;
  const isComplete = !nextSection;

  let headline: string;
  let subCopy: string;
  let statusLabel: string;

  if (isComplete) {
    headline    = pick(completeHeadlines(firstName));
    subCopy     = pick(completeSubCopy);
    statusLabel = pick(completeStatus);
  } else if (isStarting) {
    headline    = pick(startingHeadlines(firstName));
    subCopy     = pick(startingSubCopy);
    statusLabel = pick(startingStatus);
  } else {
    headline    = pick(inProgressHeadlines(firstName));
    subCopy     = pick(inProgressSubCopy);
    statusLabel =
      completionPercent < 40
        ? pick(inProgressStatusEarly)
        : completionPercent < 75
          ? pick(inProgressStatusMid)
          : pick(inProgressStatusLate);
  }

  const ctaLabel = isComplete
    ? "Core onboarding complete"
    : isStarting
      ? "Start next module"
      : "Continue next module";

  return (
    <section className="ov-hero" aria-label="Onboarding overview">
      <div className="ov-hero-texture" aria-hidden="true" />

      <div className="ov-hero-copy">
        <div className="ov-hero-head">
          <p className="section-label">Onboarding overview</p>
          <span className={`ov-hero-status${isComplete ? " done" : ""}`}>{statusLabel}</span>
        </div>

        <h1>{headline}</h1>
        <p className="ov-hero-lead">{subCopy}</p>

        <div className="ov-hero-actions">
          {nextSection ? (
            <div className="ov-hero-next">
              <p className="ov-hero-next-label">
                <span className="ov-hero-next-tag">Next up</span>
                <span className="ov-hero-next-title">{nextSection.title}</span>
              </p>
              <p className="ov-hero-next-meta">
                {remainingCount} module{remainingCount === 1 ? "" : "s"} remaining
                {remainingMinutes > 0 ? ` · ~${remainingMinutes} min left` : ""}
              </p>
              <Link className="primary-action" href={`/modules/${nextSection.slug}`}>
                {ctaLabel}
              </Link>
            </div>
          ) : (
            <div className="ov-hero-next">
              <span className="primary-action done-action">{ctaLabel}</span>
              <p className="ov-hero-next-meta">Nice work, {firstName}. Everything is saved.</p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
