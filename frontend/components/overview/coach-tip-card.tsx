"use client";

import { useEffect, useState } from "react";

type TipData = { label: string; tip: string };

type CoachTipCardProps = {
  context: string;
  variant?: "rail" | "hero";
};

const FOOTER_LINES = [
  "you've got this. seriously.",
  "one module at a time. that's all.",
  "the good stuff sticks. keep going.",
  "built for you. not a textbook.",
  "your future self is already proud.",
  "knowledge unlocked. keep stacking.",
];

function pickFooter() {
  return FOOTER_LINES[Math.floor(Math.random() * FOOTER_LINES.length)];
}

function SparkIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 15 15" fill="none" aria-hidden="true">
      <path
        d="M7.5 1.5L8.5 5.5L12.5 6.5L8.5 7.5L7.5 11.5L6.5 7.5L2.5 6.5L6.5 5.5L7.5 1.5Z"
        fill="currentColor"
      />
    </svg>
  );
}

export function CoachTipCard({ context, variant = "rail" }: CoachTipCardProps) {
  const [data, setData] = useState<TipData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    async function fetchTip() {
      setLoading(true);

      try {
        const params = new URLSearchParams({
          context,
          t: Date.now().toString(),
          r: Math.random().toString(36).slice(2),
        });
        const res = await fetch(`/api/coach-tip?${params}`, {
          method: "GET",
          cache: "no-store",
        });
        const json = await res.json();

        if (active) {
          setData(json);
        }
      } catch {
        if (active) {
          setData({ label: "Pro tip", tip: "Take notes as you go - your future self will thank you." });
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void fetchTip();

    return () => {
      active = false;
    };
  }, [context]);

  if (variant === "hero") {
    return (
      <div className="hero-tip-strip" role="note" aria-label="Onboarding tip">
        <span className="hero-tip-icon">
          <SparkIcon />
        </span>
        <div className="hero-tip-body">
          {loading || !data ? (
            <>
              <span className="hero-tip-skeleton wide" />
              <span className="hero-tip-skeleton narrow" />
            </>
          ) : (
            <span className="hero-tip-text">
              <strong>{data.label}:</strong> {data.tip}
            </span>
          )}
        </div>
      </div>
    );
  }

  return (
    <article className="ov-rail-card ov-rail-card-tip" aria-label="Coach tip">
      <div className="tip-card-header">
        <div className="tip-card-label-row">
          <span className="tip-spark-icon">
            <SparkIcon />
          </span>
          <p className="section-label">Coach tip</p>
        </div>
      </div>

      {loading || !data ? (
        <div className="tip-skeleton-block">
          <span className="tip-skeleton-line" />
          <span className="tip-skeleton-line med" />
          <span className="tip-skeleton-line short" />
        </div>
      ) : (
        <p className="tip-body-text">
          <span className="tip-prefix">{data.label}:</span> {data.tip}
        </p>
      )}

      <div className="tip-card-footer">
        <span className="tip-footer-label">{pickFooter()}</span>
      </div>
    </article>
  );
}
