import Link from "next/link";

import type { Section } from "@/lib/types";

export type LessonState = "completed" | "current" | "next" | "upcoming";

type LessonStepProps = {
  section: Section;
  index: number;
  state: LessonState;
  isLast: boolean;
};

const CheckIcon = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <path d="M2.5 7L5.5 10L11.5 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export function LessonStep({ section, index, state, isLast }: LessonStepProps) {
  const stateLabel =
    state === "completed" ? "Done"
    : state === "current" ? "In progress"
    : state === "next" ? "Up next"
    : "Queued";

  const ctaLabel = state === "current" ? "Continue" : "Start";
  const showAction = state === "current" || state === "next";

  return (
    <li className={`ov-step ${state}${isLast ? " last" : ""}`}>
      <div className="ov-step-rail">
        <div className="ov-step-marker" aria-hidden="true">
          {state === "completed" ? <CheckIcon /> : <span>{index + 1}</span>}
        </div>
        {!isLast && <div className="ov-step-line" />}
      </div>

      <div className="ov-step-body">
        <div className="ov-step-head">
          <strong className="ov-step-title">{section.title}</strong>
          <span className={`ov-step-state ${state}`}>{stateLabel}</span>
        </div>

        <p className="ov-step-summary">{section.summary}</p>
        <p className="ov-step-meta">{section.focuses.join(" • ")}</p>
        <p className={`ov-step-purpose${showAction ? "" : " subtle"}`}>{section.purpose}</p>

        {showAction && (
          <Link className="primary-action compact-primary" href={`/modules/${section.slug}`}>
            {ctaLabel}
          </Link>
        )}
      </div>
    </li>
  );
}
