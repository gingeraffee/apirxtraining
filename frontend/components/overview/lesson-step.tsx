import Link from "next/link";

import type { Section } from "@/lib/types";

export type LessonState = "completed" | "current" | "next" | "upcoming";

type LessonStepProps = {
  section: Section;
  index: number;
  state: LessonState;
  isLast: boolean;
};

export function LessonStep({ section, index, state, isLast }: LessonStepProps) {
  const stateLabel =
    state === "completed" ? "Completed"
    : state === "current" ? "Current"
    : state === "next" ? "Up next"
    : "Upcoming";

  const keyInsight = section.essentials[0]?.title ?? section.focuses[0] ?? "";

  return (
    <li className={`ov-step ${state}${isLast ? " last" : ""}`}>
      <div className="ov-step-rail">
        <div className="ov-step-marker" aria-hidden="true">
          {state === "completed" ? (
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path
                d="M2.5 7L5.5 10L11.5 4"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          ) : (
            <span>{index + 1}</span>
          )}
        </div>
        {!isLast && <div className="ov-step-line" />}
      </div>

      <div className="ov-step-body">
        <div className="ov-step-head">
          <strong className="ov-step-title">{section.title}</strong>
          <span className="ov-step-meta">
            {stateLabel} &middot; {section.estimatedMinutes} min
          </span>
        </div>
        <p className="ov-step-why">
          <span>Why it matters:</span> {section.purpose}
        </p>
        <p className="ov-step-covers">
          <span>Covers:</span> {section.summary}
        </p>
        {keyInsight && (
          <p className="ov-step-insight">
            <span>Key insight:</span> {keyInsight}
          </p>
        )}
        {state !== "completed" && (
          <Link
            className={state === "current" || state === "next" ? "primary-action compact-primary" : "inline-action"}
            href={`/modules/${section.slug}`}
          >
            {state === "current" ? "Continue lesson" : state === "next" ? "Start lesson" : "Preview lesson"}
          </Link>
        )}
      </div>
    </li>
  );
}
