"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

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

type HeroMessage = {
  welcome: (firstName: string) => string;
  story: string;
};

const IN_PROGRESS_MESSAGES: HeroMessage[] = [
  {
    welcome: (firstName) => `Welcome in, ${firstName}.`,
    story: "AAP Start keeps the essentials in one clean path so you can focus on one module at a time and still know where to find support.",
  },
  {
    welcome: (firstName) => `You're in the right place, ${firstName}.`,
    story: "This launch path is designed to keep your first stretch focused, useful, and easier to move through without handbook overload.",
  },
  {
    welcome: (firstName) => `Good to see you, ${firstName}.`,
    story: "AAP Start turns the early onboarding stretch into a guided system so you can build confidence, keep momentum, and know what comes next.",
  },
  {
    welcome: (firstName) => `Let's make this easy, ${firstName}.`,
    story: "The portal is here to keep the launch path clear: one live module at a time, with support and references still close when you need them.",
  },
];

const COMPLETE_MESSAGES: HeroMessage[] = [
  {
    welcome: (firstName) => `You're all set, ${firstName}.`,
    story: "You finished the tracked launch path. Resource Hub stays close whenever you want a quick reset, a live file, or the right support contact.",
  },
  {
    welcome: (firstName) => `Nice work, ${firstName}.`,
    story: "The live path is complete, but the portal still works like a good home base for support details, handbook access, and quick refreshers.",
  },
  {
    welcome: (firstName) => `Launch path complete, ${firstName}.`,
    story: "You made it through the tracked onboarding experience. What stays now is the useful part: fast references, contacts, and a clean place to revisit key info.",
  },
];

function pickRandomMessage(messages: HeroMessage[]) {
  return messages[Math.floor(Math.random() * messages.length)];
}

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
  const messageSet = isComplete ? COMPLETE_MESSAGES : IN_PROGRESS_MESSAGES;
  const [heroMessage, setHeroMessage] = useState<HeroMessage>(messageSet[0]);

  useEffect(() => {
    setHeroMessage(pickRandomMessage(messageSet));
  }, [messageSet]);

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

        <h1>{heroMessage.welcome(firstName)}</h1>
        <p className="ov-hero-lead">{heroMessage.story}</p>

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
