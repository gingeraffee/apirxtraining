"use client";

import type { ReactNode } from "react";

type CheckpointCard = {
  title: string;
  description: string;
};

type ModuleKnowledgeCheckShellProps = {
  eyebrow?: string;
  title?: string;
  description: string;
  note?: string;
  checkpoints?: CheckpointCard[];
  children?: ReactNode;
  className?: string;
};

const DEFAULT_CHECKPOINTS: CheckpointCard[] = [
  {
    title: "Key idea recap",
    description: "Pause and restate the main takeaway from this module in your own words.",
  },
  {
    title: "Practical moment",
    description: "Think through one day-to-day moment where this guidance should shape your next step.",
  },
  {
    title: "Ready to continue",
    description: "Confirm what action you would take and where you would escalate if needed.",
  },
];

export function ModuleKnowledgeCheckShell({
  eyebrow = "Knowledge check",
  title = "Pause here for the module review",
  description,
  note = "This checkpoint space is built now so future module assessments can slot in without changing the launch layout.",
  checkpoints = DEFAULT_CHECKPOINTS,
  children,
  className = "",
}: ModuleKnowledgeCheckShellProps) {
  const shellClassName = ["knowledge-check-shell", className].filter(Boolean).join(" ");

  return (
    <section className={shellClassName} aria-labelledby="knowledge-check-title">
      <div className="knowledge-check-head">
        <div>
          <p className="section-label">{eyebrow}</p>
          <h3 id="knowledge-check-title">{title}</h3>
        </div>
        <span className="knowledge-check-state">Module checkpoint</span>
      </div>

      <p className="knowledge-check-description">{description}</p>

      <div className="knowledge-check-grid">
        {checkpoints.map((checkpoint) => (
          <article key={checkpoint.title} className="knowledge-check-card">
            <div className="knowledge-check-card-top">
              <span className="knowledge-check-chip">Review point</span>
              <strong>{checkpoint.title}</strong>
            </div>
            <p>{checkpoint.description}</p>
            <div className="knowledge-check-shell-lines" aria-hidden="true">
              <span />
              <span />
              <span />
            </div>
          </article>
        ))}
      </div>

      {children}

      <p className="knowledge-check-note">{note}</p>
    </section>
  );
}
