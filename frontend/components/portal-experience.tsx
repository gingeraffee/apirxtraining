"use client";

import Link from "next/link";
import { useEffect, useState, useTransition } from "react";

import { acknowledgeSection, fetchExperience, fetchProgress, saveProgress, submitKnowledgeCheck } from "@/lib/api";
import type { Contact, KnowledgeCheck, ExperienceContent, ProgressRecord, Section, SupplementalPage, TrackInfo } from "@/lib/types";
import { OverviewScreen } from "@/components/overview/overview-screen";
import { LoginScreen } from "@/components/login-screen";
import { PortalBrandLockup } from "@/components/portal-brand-lockup";
import { ModuleKnowledgeCheck, type KnowledgeCheckFeedback } from "@/components/module-knowledge-check";
import { CoachTipCard } from "@/components/overview/coach-tip-card";
import { normalizeExperienceContent } from "@/lib/quiz-fallbacks";

type PortalKind = "overview" | "section" | "toolkit";

type PortalExperienceProps = {
  kind: PortalKind;
  slug?: string;
};

const EMPLOYEE_ID = "demo-employee";
const AUTH_NAME_KEY = "aap_portal_name";
const AUTH_EMPLOYEE_NUMBER_KEY = "aap_portal_employee_number";
const QUIZ_FALLBACK_KEY = "aap_portal_quiz_passed_sections";
const FALLBACK_DISPLAY_NAME = "";

const CheckIcon = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
    <path d="M2.5 7L5.5 10L11.5 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const LaunchLinkIcon = () => (
  <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
    <path d="M3 9L9 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    <path d="M4.5 3H9V7.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export function PortalExperience({ kind, slug }: PortalExperienceProps) {
  const [experience, setExperience] = useState<ExperienceContent | null>(null);
  const [progress, setProgress] = useState<ProgressRecord | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [profileName, setProfileName] = useState<string | null>(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem(AUTH_NAME_KEY) ?? null;
    }
    return null;
  });
  const [profileEmployeeNumber, setProfileEmployeeNumber] = useState<string | null>(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem(AUTH_EMPLOYEE_NUMBER_KEY) ?? null;
    }
    return null;
  });
  const [checkedItems, setCheckedItems] = useState<Record<string, boolean[]>>({});
  const [quizSelections, setQuizSelections] = useState<Record<string, Array<number | null>>>({});
  const [quizFeedback, setQuizFeedback] = useState<Record<string, KnowledgeCheckFeedback | null>>({});
  const [fallbackQuizPassedSections, setFallbackQuizPassedSections] = useState<string[]>(() => {
    if (typeof window === "undefined") {
      return [];
    }

    try {
      const stored = localStorage.getItem(QUIZ_FALLBACK_KEY);
      return stored ? JSON.parse(stored) as string[] : [];
    } catch {
      return [];
    }
  });
  const [pendingAction, setPendingAction] = useState<"quiz" | "acknowledgment" | null>(null);
  const [isPending, startTransition] = useTransition();
  const [isSigningIn, setIsSigningIn] = useState(false);

  useEffect(() => {
    let isCancelled = false;

    async function load() {
      setLoading(true);
      setError(null);

      try {
        const [nextExperience, nextProgress] = await Promise.all([
          fetchExperience(),
          fetchProgress(EMPLOYEE_ID),
        ]);

        if (isCancelled) {
          return;
        }

        setExperience(normalizeExperienceContent(nextExperience));
        setProgress(nextProgress);
      } catch {
        if (!isCancelled) {
          setError("The onboarding API is unavailable. Start the FastAPI backend and reload this page.");
        }
      } finally {
        if (!isCancelled) {
          setLoading(false);
        }
      }
    }

    void load();

    return () => {
      isCancelled = true;
    };
  }, []);

  const displayName = profileName ?? progress?.display_name ?? FALLBACK_DISPLAY_NAME;
  const firstName = displayName.split(" ")[0] ?? displayName;
  const sections = experience?.sections ?? [];
  const supplementalPages = experience?.supplementalPages ?? [];
  const activeSection = sections.find((section) => section.slug === slug) ?? null;
  const activeSupplemental = supplementalPages.find((page) => page.slug === slug) ?? null;
  const roleSpecificPages = supplementalPages.filter((page) => page.slug === "where-you-make-an-impact");
  const referencePages = supplementalPages.filter((page) => page.slug !== "where-you-make-an-impact");
  const acknowledgedSections = new Set(progress?.acknowledged_sections ?? []);
  const quizPassedSections = new Set([...(progress?.quiz_passed_sections ?? progress?.completed_sections ?? []), ...fallbackQuizPassedSections]);
  const completedSections = new Set(Array.from(acknowledgedSections).filter((sectionSlug) => quizPassedSections.has(sectionSlug)));
  const overviewNextSection = sections.find((section) => !completedSections.has(section.slug)) ?? null;
  const sectionSequenceNext = activeSection
    ? sections[sections.findIndex((section) => section.slug === activeSection.slug) + 1] ?? null
    : null;
  const contextNextSection = activeSection ? sectionSequenceNext : overviewNextSection;
  const completionPercent = sections.length
    ? Math.round((completedSections.size / sections.length) * 100)
    : 0;

  useEffect(() => {
    if (!activeSection) {
      return;
    }

    setCheckedItems((current) => {
      if (current[activeSection.slug]) {
        return current;
      }
      return {
        ...current,
        [activeSection.slug]: activeSection.acknowledgment.items.map(() => false),
      };
    });
    setQuizSelections((current) => {
      if (current[activeSection.slug]) {
        return current;
      }
      return {
        ...current,
        [activeSection.slug]: activeSection.knowledgeCheck.questions.map(() => null),
      };
    });
  }, [activeSection]);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }

    localStorage.setItem(QUIZ_FALLBACK_KEY, JSON.stringify(fallbackQuizPassedSections));
  }, [fallbackQuizPassedSections]);

  async function syncCurrentSection(currentSlug: string) {
    if (!progress || progress.current_section === currentSlug) {
      return;
    }

    try {
      const updated = await saveProgress(EMPLOYEE_ID, {
        display_name: displayName,
        current_section: currentSlug,
        completed_sections: Array.from(completedSections),
        acknowledged_sections: Array.from(acknowledgedSections),
        quiz_passed_sections: Array.from(quizPassedSections),
      });
      setProgress(updated);
    } catch {
      // Ignore background sync failures.
    }
  }

  useEffect(() => {
    if (!profileName || !progress || !slug) {
      return;
    }

    void syncCurrentSection(slug);
  }, [slug, progress, profileName]);

  function toggleItem(sectionSlug: string, itemIndex: number) {
    setCheckedItems((current) => {
      const existing = current[sectionSlug] ?? [];
      const next = [...existing];
      next[itemIndex] = !next[itemIndex];
      return {
        ...current,
        [sectionSlug]: next,
      };
    });
  }

  function selectQuizAnswer(sectionSlug: string, questionIndex: number, optionIndex: number) {
    setQuizSelections((current) => {
      const existing = current[sectionSlug] ?? [];
      const next = [...existing];
      next[questionIndex] = optionIndex;
      return {
        ...current,
        [sectionSlug]: next,
      };
    });
    setQuizFeedback((current) => ({
      ...current,
      [sectionSlug]: current[sectionSlug]?.state === "passed" ? current[sectionSlug] : null,
    }));
  }

  function handleAcknowledge(section: Section) {
    const items = section.acknowledgment.items;
    const selected = checkedItems[section.slug] ?? [];
    const complete = section.acknowledgment.mode === "manual"
      || items.length === 0
      || (selected.length === items.length && selected.every(Boolean));

    if (!complete) {
      return;
    }

    setPendingAction("acknowledgment");
    startTransition(async () => {
      try {
        const updated = await acknowledgeSection(EMPLOYEE_ID, section.slug, displayName);
        setProgress(updated);
      } catch (err) {
        console.error("Failed to acknowledge section:", err);
      } finally {
        setPendingAction(null);
      }
    });
  }

  function handleSubmitKnowledge(section: Section) {
    const selectedAnswers = quizSelections[section.slug] ?? [];
    const questions = section.knowledgeCheck.questions;
    const needsAllAnswers = selectedAnswers.length !== questions.length || selectedAnswers.some((value) => value === null);

    if (needsAllAnswers) {
      setQuizFeedback((current) => ({
        ...current,
        [section.slug]: {
          state: "needs-answers",
          title: "Finish each question first",
          body: "Choose one answer for every question before checking your answers.",
        },
      }));
      return;
    }

    setPendingAction("quiz");
    startTransition(async () => {
      try {
        const result = await submitKnowledgeCheck(EMPLOYEE_ID, section.slug, displayName, selectedAnswers.filter((value): value is number => value !== null));
        setProgress(result.progress);
        setFallbackQuizPassedSections((current) => current.filter((item) => item !== section.slug));
        setQuizFeedback((current) => ({
          ...current,
          [section.slug]: result.passed
            ? {
                state: "passed",
                title: "Knowledge check passed",
                body: "You cleared the required quiz. Finish the acknowledgment step to complete the module.",
                scoreLabel: `${result.correct_count}/${result.total_questions} correct`,
              }
            : {
                state: "failed",
                title: "Take another pass",
                body: "Review the section and try again. The module only completes after this quiz is passed.",
                scoreLabel: `${result.correct_count}/${result.total_questions} correct`,
              },
        }));
      } catch (err) {
        const isNotFound = err instanceof Error && err.message.includes("404");

        if (isNotFound) {
          const correctCount = questions.reduce((count, question, index) => {
            return count + (selectedAnswers[index] === question.correctOptionIndex ? 1 : 0);
          }, 0);
          const totalQuestions = questions.length;
          const passingPercent = section.knowledgeCheck.passingPercent;
          const score = totalQuestions > 0 ? correctCount / totalQuestions : 0;
          const passed = totalQuestions > 0 && score >= passingPercent;

          if (passed) {
            setFallbackQuizPassedSections((current) => Array.from(new Set([...current, section.slug])));
          }

          setQuizFeedback((current) => ({
            ...current,
            [section.slug]: passed
              ? {
                  state: "passed",
                  title: "Knowledge check passed",
                  body: "The checkpoint was scored locally because the backend route is not live yet. Finish the acknowledgment step to complete the module.",
                  scoreLabel: `${correctCount}/${totalQuestions} correct`,
                }
              : {
                  state: "failed",
                  title: "Take another pass",
                  body: "Review the section and try again. The module only completes after this quiz is passed.",
                  scoreLabel: `${correctCount}/${totalQuestions} correct`,
                },
          }));
        } else {
          console.error("Failed to submit knowledge check:", err);
          setQuizFeedback((current) => ({
            ...current,
            [section.slug]: {
              state: "failed",
              title: "Quiz unavailable right now",
              body: "The knowledge check could not be submitted. Try again in a moment.",
            },
          }));
        }
      } finally {
        setPendingAction(null);
      }
    });
  }

  async function handleLogin(nextName: string, nextEmployeeNumber: string) {
    if (!progress) {
      return;
    }

    setIsSigningIn(true);
    setProfileName(nextName);
    setProfileEmployeeNumber(nextEmployeeNumber);
    localStorage.setItem(AUTH_NAME_KEY, nextName);
    localStorage.setItem(AUTH_EMPLOYEE_NUMBER_KEY, nextEmployeeNumber);

    try {
      const updated = await saveProgress(EMPLOYEE_ID, {
        display_name: nextName,
        current_section: progress.current_section,
        completed_sections: Array.from(completedSections),
        acknowledged_sections: Array.from(acknowledgedSections),
        quiz_passed_sections: Array.from(quizPassedSections),
      });
      setProgress(updated);
    } catch {
      // Let the user continue even if the profile sync misses once.
    } finally {
      setIsSigningIn(false);
    }
  }

  function handleLogout() {
    setProfileName(null);
    setProfileEmployeeNumber(null);
    localStorage.removeItem(AUTH_NAME_KEY);
    localStorage.removeItem(AUTH_EMPLOYEE_NUMBER_KEY);
  }

  if (loading) {
    return (
      <div className="status-screen">
        <div className="status-card">
          <p className="section-label">AAP Start</p>
          <h1>Loading your launch experience...</h1>
          <p>Connecting to the onboarding API.</p>
        </div>
      </div>
    );
  }

  if (error || !experience || !progress) {
    return (
      <div className="status-screen">
        <div className="status-card">
          <p className="section-label">Setup needed</p>
          <h1>Backend not running.</h1>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!profileName) {
    return <LoginScreen defaultName="" defaultEmployeeNumber={profileEmployeeNumber ?? ""} isPending={isSigningIn} onSubmit={handleLogin} />;
  }

  const contextTitle = kind === "overview"
    ? "Overview"
    : activeSection?.title ?? activeSupplemental?.title ?? "Page not found";
  const contextEyebrow = activeSection?.eyebrow ?? activeSupplemental?.eyebrow ?? null;

  return (
    <div className={`app-shell portal-shell${kind === "overview" ? "" : " portal-shell--detail"}`}>
      <aside className="side-rail portal-rail">
        <div className="brand-block portal-brand-block portal-rail-brand">
          <PortalBrandLockup priority />
        </div>

        <div className="rail-panel progress-panel">
          <p className="section-label">Tracked progress</p>
          <strong>{completionPercent}%</strong>
          <p>{progress.completed_sections.length} of {sections.length} live modules complete</p>
          <div className="rail-progress" aria-hidden="true">
            <div className="rail-progress-track">
              <span className="rail-progress-fill" style={{ width: `${completionPercent}%` }} />
            </div>
          </div>
        </div>

        <div className="rail-nav-group">
          <p className="rail-group-label">Launch path</p>
          <nav className="nav-stack">
            <Link className={kind === "overview" ? "nav-link active" : "nav-link"} href="/">
              <span className="nav-link-num">0</span>
              <span className="nav-link-title">Overview</span>
            </Link>
            {sections.map((section, index) => (
              <Link
                key={section.slug}
                className={slug === section.slug ? "nav-link active" : completedSections.has(section.slug) ? "nav-link is-complete" : "nav-link"}
                href={`/modules/${section.slug}`}
              >
                <span className="nav-link-num">{completedSections.has(section.slug) ? <CheckIcon /> : index + 1}</span>
                <span className="nav-link-title">{section.title}</span>
              </Link>
            ))}
          </nav>
        </div>

        {referencePages.length > 0 && (
          <div className="rail-nav-group">
            <p className="rail-group-label">Reference shelf</p>
            <nav className="nav-stack">
              {referencePages.map((page) => (
                <Link
                  key={page.slug}
                  className={slug === page.slug ? "nav-link nav-link--supplemental active" : "nav-link nav-link--supplemental"}
                  href={`/modules/${page.slug}`}
                >
                  <span className="nav-link-num"><LaunchLinkIcon /></span>
                  <span className="nav-link-title">{page.title}</span>
                  <span className={`nav-link-badge ${page.state}`}>{page.state === "coming_soon" ? "Soon" : "Live"}</span>
                </Link>
              ))}
            </nav>
          </div>
        )}

        {roleSpecificPages.length > 0 && (
          <div className="rail-nav-group">
            <p className="rail-group-label">Role-specific</p>
            <nav className="nav-stack">
              {roleSpecificPages.map((page) => (
                <Link
                  key={page.slug}
                  className={slug === page.slug ? "nav-link nav-link--supplemental active" : "nav-link nav-link--supplemental"}
                  href={`/modules/${page.slug}`}
                >
                  <span className="nav-link-num">...</span>
                  <span className="nav-link-title">{page.title}</span>
                  <span className={`nav-link-badge ${page.state}`}>Soon</span>
                </Link>
              ))}
            </nav>
          </div>
        )}

        <button className="rail-user-chip" type="button" onClick={handleLogout}>
          <div className="rail-user-avatar" aria-hidden="true">{firstName.charAt(0).toUpperCase()}</div>
          <div className="rail-user-info">
            <strong>{firstName}</strong>
            <span>Sign out</span>
          </div>
        </button>
      </aside>

      <main className={`main-stage portal-stage${kind === "overview" ? "" : " portal-stage--detail"}`}>
        {kind !== "overview" && activeSection?.slug !== "welcome-to-aap" && activeSection?.slug !== "how-we-show-up" && (
          <header className="topbar portal-topbar">
            <div>
              {contextEyebrow && contextEyebrow !== "Start Here" && <p className="section-label">{contextEyebrow}</p>}
              <h1 className="topbar-title">{contextTitle}</h1>
            </div>
          </header>
        )}

        {kind === "overview" && (
          <OverviewScreen experience={experience} progress={progress} nextSection={overviewNextSection} firstName={firstName} />
        )}

        {kind !== "overview" && activeSection && (
          <SectionScreen
            section={activeSection}
            nextSection={contextNextSection}
            isAcknowledged={acknowledgedSections.has(activeSection.slug)}
            isQuizPassed={quizPassedSections.has(activeSection.slug)}
            isCompleted={completedSections.has(activeSection.slug)}
            selections={checkedItems[activeSection.slug] ?? []}
            quizSelections={quizSelections[activeSection.slug] ?? []}
            quizFeedback={quizFeedback[activeSection.slug] ?? null}
            onToggle={toggleItem}
            onQuizSelect={selectQuizAnswer}
            onSubmitKnowledgeCheck={handleSubmitKnowledge}
            onAcknowledge={handleAcknowledge}
            isPending={isPending}
            pendingAction={pendingAction}
            contacts={experience.contacts}
            track={experience.track}
          />
        )}

        {kind !== "overview" && !activeSection && activeSupplemental && (
          <SupplementalPageScreen page={activeSupplemental} contacts={experience.contacts} />
        )}

        {kind !== "overview" && !activeSection && !activeSupplemental && (
          <div className="status-screen inline-status-screen">
            <div className="status-card">
              <p className="section-label">AAP Start</p>
              <h1>Page not found.</h1>
              <p>This launch page is not part of the current experience payload.</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

type SectionProps = {
  section: Section;
  nextSection: Section | null;
  isAcknowledged: boolean;
  isQuizPassed: boolean;
  isCompleted: boolean;
  selections: boolean[];
  quizSelections: Array<number | null>;
  quizFeedback: KnowledgeCheckFeedback | null;
  onToggle: (sectionSlug: string, itemIndex: number) => void;
  onQuizSelect: (sectionSlug: string, questionIndex: number, optionIndex: number) => void;
  onSubmitKnowledgeCheck: (section: Section) => void;
  onAcknowledge: (section: Section) => void;
  isPending: boolean;
  pendingAction: "quiz" | "acknowledgment" | null;
  contacts: Contact[];
  track: TrackInfo;
};

function SectionScreen({ section, nextSection, isAcknowledged, isQuizPassed, isCompleted, selections, quizSelections, quizFeedback, onToggle, onQuizSelect, onSubmitKnowledgeCheck, onAcknowledge, isPending, pendingAction, contacts, track }: SectionProps) {
  const knowledgeCheck: KnowledgeCheck = section.knowledgeCheck ?? { title: "Knowledge Check", intro: "Quiz content is unavailable right now.", passingPercent: 1, questions: [] };
  const showChecklist = section.acknowledgment.mode !== "manual" && section.acknowledgment.items.length > 0;
  const allChecked = !showChecklist || (selections.length === section.acknowledgment.items.length && selections.every(Boolean));
  const checkedCount = selections.filter(Boolean).length;
  const answeredQuizCount = quizSelections.filter((value) => value !== null).length;
  const totalQuizQuestions = knowledgeCheck.questions.length;
  const isWelcomeModule = section.slug === "welcome-to-aap";
  const isCultureModule = section.slug === "how-we-show-up";
  const completionStatus = isCompleted
    ? "Completed"
    : isQuizPassed && isAcknowledged
      ? "Saving"
      : isQuizPassed
        ? "Acknowledgment left"
        : isAcknowledged
          ? "Quiz left"
          : "2 steps left";
  const completionStatusNote = isCompleted
    ? "Quiz and acknowledgment are both saved. You can revisit this chapter anytime."
    : isQuizPassed && !isAcknowledged
      ? "Knowledge check passed. Finish the acknowledgment to complete the module."
      : isAcknowledged && !isQuizPassed
        ? "Acknowledgment saved. Pass the knowledge check to complete the module."
        : "Pass the knowledge check and finish the acknowledgment to complete this module.";
  const checkpointDescription = isWelcomeModule
    ? "Before you finish Welcome to AAP, pass the required knowledge check and complete the acknowledgment."
    : `Before ${section.title} can be complete, pass the required knowledge check and finish the acknowledgment.`;
  const checkpointNote = isCompleted
    ? "This module is complete and saved in your tracked progress."
    : "Both required steps stay visible here until the module is complete.";
  const completionSectionHref = "#section-completion";
  const progressionItems = isWelcomeModule
    ? [
      { href: "#section-big-picture", title: "Big picture" },
      { href: "#section-context", title: "AAP and API" },
      { href: "#section-practical-guidance", title: "Using AAP Start" },
      { href: "#section-knowledge-check", title: "Knowledge check" },
      { href: "#section-acknowledgment", title: "Acknowledgment" },
      { href: "#section-completion", title: "Completion" },
    ]
    : [
      { href: "#section-framing", title: "Framing" },
      { href: "#section-story", title: "Main idea" },
      { href: "#section-example", title: "At AAP" },
      { href: "#section-action", title: "Take action" },
      { href: "#section-knowledge-check", title: "Knowledge check" },
      { href: "#section-acknowledgment", title: "Acknowledgment" },
      { href: "#section-completion", title: "Completion" },
    ];
  const progressionLabel = isWelcomeModule ? "Welcome module map" : "Progress tracker";
  const progressionMeta = isWelcomeModule
    ? `${progressionItems.length} stops through the welcome path`
    : `${progressionItems.length} beats through this module`;
  const welcomeSupportItems = section.policyAreas[0]?.items ?? [];
  const welcomeContextItems = section.policyAreas[1]?.items ?? [];

  const supportContact = contacts.find((c) => c.id === track.supportContactId) ?? null;

  const tipContext = nextSection
    ? `${nextSection.title}: ${nextSection.summary}`
    : `${section.title}: ${section.summary}`;
  const narrativeBeats = section.essentials.slice(0, 3);
  const examplePrimary = section.policyAreas[0] ?? null;
  const exampleSecondary = section.policyAreas[1] ?? null;
  const framingCopy = section.chapterIntros?.[0] ?? section.purpose;
  const exampleIntro = section.chapterIntros?.[1] ?? "This is what the guidance looks like once it becomes real work at AAP.";
  const actionIntro = section.chapterIntros?.[2] ?? "Leave this chapter with a clear next move, not just a list of reminders.";
  const reflectionPrompts = (section.focuses.length > 0 ? section.focuses : narrativeBeats.map((item) => item.title)).slice(0, 3);
  const cultureScenarios = isCultureModule
    ? [
      {
        eyebrow: "When clarity matters",
        title: "Say the thing directly and respectfully",
        body: section.policyAreas[0]?.items[0]?.body ?? "Be direct, respectful, and professional when something needs to be addressed.",
      },
      {
        eyebrow: "When a line gets crossed",
        title: "Treat unsafe conduct like a real escalation",
        body: section.policyAreas[0]?.items[1]?.body ?? "Unsafe or disrespectful conduct should be raised immediately, not normalized.",
      },
      {
        eyebrow: "When information is sensitive",
        title: "Protect trust before anything gets shared",
        body: section.policyAreas[1]?.items[0]?.body ?? "Confirm the reason, the audience, and the system before sharing sensitive information.",
      },
    ]
    : [];
  const cultureEscalationNote = isCultureModule
    ? section.policyAreas[1]?.items[3]?.body ?? section.escalation[1] ?? null
    : null;
  const supportPhoneHref = supportContact ? supportContact.phone.replace(/\D/g, "") : "";
  const quizFeedbackToShow = quizFeedback ?? (isQuizPassed
    ? {
        state: "passed" as const,
        title: "Knowledge check passed",
        body: "This required quiz is already complete.",
      }
    : null);
  const completionRequirements = [
    {
      label: "Knowledge check",
      complete: isQuizPassed,
      body: isQuizPassed ? "Passed and saved." : `Required before completion. ${answeredQuizCount}/${totalQuizQuestions} answered.`,
    },
    {
      label: "Acknowledgment",
      complete: isAcknowledged,
      body: isAcknowledged ? "Acknowledgment saved." : showChecklist ? `${checkedCount}/${section.acknowledgment.items.length} checks ready.` : "Required before completion.",
    },
  ];
  const completionCtaLabel = isCompleted
    ? "Module complete"
    : !isQuizPassed
      ? "Pass knowledge check to finish"
      : !isAcknowledged
        ? "Complete acknowledgment to finish"
        : "Saving completion...";
  const completionHelperNote = isCompleted
    ? "Both required steps are saved. This module now counts toward tracked progress."
    : !isQuizPassed
      ? "Start with the knowledge check above. Once it passes, the acknowledgment becomes your final confirmation step."
      : !isAcknowledged
        ? "The checkpoint is cleared. Save the acknowledgment to finish the module."
        : "Everything required is saved for this module.";
  const renderWelcomeEssentialBody = (item: { title: string; body: string }) => item.body
    .split("\n\n")
    .map((paragraph, index) => {
      const labeledParagraph = paragraph.match(/^(Mission|Vision):\s*(.*)$/);

      if (labeledParagraph) {
        return (
          <p key={`${item.title}-${index}`}>
            <strong>{labeledParagraph[1]}:</strong> {labeledParagraph[2]}
          </p>
        );
      }

      return <p key={`${item.title}-${index}`}>{paragraph}</p>;
    });

  return (
    <div className={`section-page portal-page portal-page--detail portal-page--section${isWelcomeModule ? " portal-page--welcome" : ""}${isCultureModule ? " portal-page--culture" : ""}`}>
      <section className="page-hero single-focus-hero section-hero section-hero--focused section-hero--cinematic">
        <div className="section-hero-copy">
          <div className="section-hero-head">
            <p className="section-label">{section.eyebrow}</p>
            <span className={`section-hero-status${isCompleted ? " done" : ""}`}>
              {isCompleted ? "Module complete" : "In progress"}
            </span>
          </div>
          <h1>{section.title}</h1>
          <p className="lead">{section.summary}</p>
          <p className="purpose-line">{section.purpose}</p>
          <div className="section-chip-row">
            <span className="section-chip">{progressionItems.length} sections</span>
            <span className="section-chip">Knowledge check</span>
            <span className="section-chip">Acknowledgment required</span>
          </div>
        </div>
      </section>

      <div className="section-layout-grid">
        <div className="section-main-column">
          <nav className="lesson-flow-nav" aria-label="Lesson progression">
            <div className="lesson-flow-head">
              <p className="lesson-flow-label">{progressionLabel}</p>
              <p className="lesson-flow-meta">{progressionMeta}</p>
            </div>
            <div className="lesson-flow-track">
              {progressionItems.map((item, index) => (
                <a
                  key={item.href}
                  className={index === 0 ? "lesson-flow-link lesson-flow-link--active" : item.href === completionSectionHref ? "lesson-flow-link lesson-flow-link--completion" : "lesson-flow-link"}
                  href={item.href}
                >
                  <span className="lesson-flow-step">{index + 1}</span>
                  <span className="lesson-flow-title">{item.title}</span>
                </a>
              ))}
            </div>
          </nav>

          {isWelcomeModule ? (
            <>
              <section className="lesson-chapter lesson-chapter--orientation lesson-chapter-surface welcome-body-section welcome-big-picture-section" id="section-big-picture">
                <div className="welcome-foundation-layout">
                  <div className="lesson-chapter-head welcome-foundation-head">
                    <h2>Start with the big picture</h2>
                    <p className="lesson-chapter-intro">{section.chapterIntros?.[0]}</p>
                  </div>
                  <div className="welcome-foundation-panel">
                    <div className="welcome-big-picture-grid">
                      {section.essentials.map((item) => (
                        <article key={item.title} className="welcome-big-picture-card">
                          <h3>{item.title}</h3>
                          <div className="welcome-big-picture-copy">
                            {renderWelcomeEssentialBody(item)}
                          </div>
                        </article>
                      ))}
                    </div>
                  </div>
                </div>
              </section>

              <section className="lesson-chapter lesson-chapter--reference lesson-chapter-surface welcome-body-section" id="section-context">
                <div className="lesson-chapter-head">
                  <h2>AAP and API in this launch experience</h2>
                  <p className="lesson-chapter-intro">{section.chapterIntros?.[1]}</p>
                </div>
                <div className="welcome-context-layout">
                  <article className="welcome-context-block">
                    <h3>{section.policyAreas[0]?.title ?? "Company context"}</h3>
                    <dl className="policy-list">
                      {welcomeSupportItems.map((item) => (
                        <div key={item.label} className="policy-row">
                          <dt>{item.label}</dt>
                          <dd>{item.body}</dd>
                        </div>
                      ))}
                    </dl>
                  </article>
                  {section.contextSidebar && (
                    <article className="welcome-context-block welcome-context-block--api">
                      <h3>{section.contextSidebar.title}</h3>
                      {section.contextSidebar.body.map((para, i) => (
                        <p key={i}>{para}</p>
                      ))}
                    </article>
                  )}
                </div>
              </section>

              <section className="lesson-chapter lesson-chapter--application lesson-chapter-surface welcome-body-section" id="section-practical-guidance">
                <div className="lesson-chapter-head">
                  <h2>Using AAP Start</h2>
                  <p className="lesson-chapter-intro">{section.chapterIntros?.[2]}</p>
                </div>
                <div className="welcome-practical-grid">
                  <article className="welcome-practical-block">
                    <h3>What this path should give you</h3>
                    <ul className="plain-list">
                      {section.actions.map((item) => <li key={item}>{item}</li>)}
                    </ul>
                  </article>
                  <article className="welcome-practical-block">
                    <h3>Where questions should go</h3>
                    <ul className="plain-list">
                      {section.escalation.map((item) => <li key={item}>{item}</li>)}
                    </ul>
                  </article>
                </div>
                {welcomeContextItems.length > 0 && (
                  <article className="welcome-practical-block welcome-practical-block--portal">
                    <h3>{welcomeContextItems[0]?.label ?? "Day-one orientation"}</h3>
                    <ul className="plain-list">
                      {welcomeContextItems.map((item) => (
                        <li key={item.label}>{item.body}</li>
                      ))}
                    </ul>
                  </article>
                )}
              </section>

              <section className="lesson-chapter lesson-chapter--checkpoint welcome-checkpoint-section welcome-knowledge-section" id="section-knowledge-check">
                <ModuleKnowledgeCheck
                  knowledgeCheck={knowledgeCheck}
                  selections={quizSelections}
                  isPassed={isQuizPassed}
                  isPending={isPending && pendingAction === "quiz"}
                  feedback={quizFeedbackToShow}
                  onSelect={(questionIndex, optionIndex) => onQuizSelect(section.slug, questionIndex, optionIndex)}
                  onSubmit={() => onSubmitKnowledgeCheck(section)}
                />
              </section>

              <section className="lesson-chapter lesson-chapter--acknowledgment lesson-chapter-surface welcome-acknowledgment-section" id="section-acknowledgment">
                <div className="lesson-chapter-head lesson-chapter-head--completion acknowledgment-section-head">
                  <p className="section-label">Acknowledgment</p>
                  <h2>{section.acknowledgment.title}</h2>
                  <p className="lesson-chapter-intro">This is the final required confirmation after the checkpoint passes.</p>
                </div>
                <p className="acknowledgment-statement">{section.acknowledgment.statement}</p>

                {showChecklist && (
                  <div className="checklist-list">
                    {section.acknowledgment.items.map((item, index) => (
                      <button
                        key={item}
                        className={selections[index] ? "check-item active" : "check-item"}
                        onClick={() => onToggle(section.slug, index)}
                        type="button"
                        disabled={isAcknowledged}
                      >
                        <span className="check-item-indicator" aria-hidden="true">{selections[index] ? <CheckIcon /> : ""}</span>
                        <strong>{item}</strong>
                      </button>
                    ))}
                  </div>
                )}

                <button
                  className={`primary-action${isAcknowledged ? " primary-action--done" : ""}`}
                  disabled={isAcknowledged || !allChecked || isPending}
                  onClick={() => !isAcknowledged && onAcknowledge(section)}
                  aria-disabled={isAcknowledged}
                  type="button"
                >
                  {isAcknowledged ? "Acknowledgment saved" : isPending && pendingAction === "acknowledgment" ? "Saving acknowledgment..." : "Complete acknowledgment"}
                </button>
              </section>

              <section className="lesson-chapter lesson-chapter--completion welcome-completion-section" id="section-completion">
                <div className="lesson-chapter-head lesson-chapter-head--completion">
                  <p className="section-label">Completion</p>
                  <h2>Finish the module with both required steps</h2>
                </div>
                <p>{checkpointDescription}</p>
                <p className="module-flow-bridge">Checkpoint first, acknowledgment second, completion last.</p>
                <div className="module-completion-summary">
                  {completionRequirements.map((item) => (
                    <article key={item.label} className={item.complete ? "module-completion-card module-completion-card--done" : "module-completion-card"}>
                      <p className="section-label">{item.label}</p>
                      <strong>{item.complete ? "Complete" : "Required"}</strong>
                      <p>{item.body}</p>
                    </article>
                  ))}
                </div>

                <p className="module-completion-helper">{completionHelperNote}</p>
                <button className={`primary-action${isCompleted ? " primary-action--done" : ""}`} disabled type="button">
                  {completionCtaLabel}
                </button>

                {nextSection && (
                  <p className="finish-next-note">
                    Next after this: <Link className="module-next-link" href={`/modules/${nextSection.slug}`}>{nextSection.title}</Link>
                  </p>
                )}
              </section>
            </>
          ) : isCultureModule ? (
            <>
              <section className="lesson-chapter lesson-chapter--orientation lesson-chapter-surface culture-chapter-shell culture-day-shell" id="section-day-to-day">
                <div className="lesson-chapter-head culture-chapter-head">
                  <p className="section-label">What this means day to day</p>
                  <h2>Show the standard in ordinary moments</h2>
                  <p className="lesson-chapter-intro">{framingCopy}</p>
                </div>
                <div className="culture-prose-stack">
                  {narrativeBeats.map((item, index) => (
                    <article key={item.title} className={index === 0 ? "culture-prose-point culture-prose-point--lead" : "culture-prose-point"}>
                      <h3>{item.title}</h3>
                      <p>{item.body}</p>
                    </article>
                  ))}
                </div>
              </section>

              <section className="lesson-chapter lesson-chapter--reference lesson-chapter-surface culture-chapter-shell culture-example-shell" id="section-example">
                <div className="lesson-chapter-head culture-chapter-head">
                  <p className="section-label">What this looks like at AAP</p>
                  <h2>Use the standard when the moment is real</h2>
                  <p className="lesson-chapter-intro">{exampleIntro}</p>
                </div>
                <div className="culture-scenario-list">
                  {cultureScenarios.map((scenario) => (
                    <article key={scenario.title} className="culture-scenario">
                      <p className="section-label">{scenario.eyebrow}</p>
                      <h3>{scenario.title}</h3>
                      <p>{scenario.body}</p>
                    </article>
                  ))}
                </div>
              </section>

              <section className="lesson-chapter lesson-chapter--application lesson-chapter-surface culture-chapter-shell culture-action-shell" id="section-action">
                <div className="lesson-chapter-head culture-chapter-head">
                  <p className="section-label">What to do in practice</p>
                  <h2>Keep the next move simple</h2>
                  <p className="lesson-chapter-intro">{actionIntro}</p>
                </div>
                <div className="culture-action-layout">
                  <div className="culture-action-main">
                    <ul className="plain-list culture-action-list">
                      {section.actions.map((item) => <li key={item}>{item}</li>)}
                    </ul>
                  </div>
                  <aside className="culture-inline-support">
                    <p className="section-label">Escalate quickly</p>
                    <ul className="plain-list culture-escalation-list">
                      {section.escalation.map((item) => <li key={item}>{item}</li>)}
                    </ul>
                    {cultureEscalationNote && <p className="culture-inline-note">{cultureEscalationNote}</p>}
                  </aside>
                </div>
              </section>

              <section className="lesson-chapter lesson-chapter--checkpoint lesson-chapter-surface culture-chapter-shell culture-knowledge-shell" id="section-knowledge-check">
                <ModuleKnowledgeCheck
                  knowledgeCheck={knowledgeCheck}
                  selections={quizSelections}
                  isPassed={isQuizPassed}
                  isPending={isPending && pendingAction === "quiz"}
                  feedback={quizFeedbackToShow}
                  onSelect={(questionIndex, optionIndex) => onQuizSelect(section.slug, questionIndex, optionIndex)}
                  onSubmit={() => onSubmitKnowledgeCheck(section)}
                />
              </section>

              <section className="lesson-chapter lesson-chapter--acknowledgment lesson-chapter-surface culture-chapter-shell culture-acknowledgment-shell" id="section-acknowledgment">
                <div className="lesson-chapter-head lesson-chapter-head--completion culture-chapter-head acknowledgment-section-head">
                  <p className="section-label">Acknowledgment</p>
                  <h2>{section.acknowledgment.title}</h2>
                  <p className="lesson-chapter-intro">This is the final required confirmation after the checkpoint passes.</p>
                </div>
                <p className="acknowledgment-statement">{section.acknowledgment.statement}</p>

                {showChecklist && (
                  <div className="checklist-list">
                    {section.acknowledgment.items.map((item, index) => (
                      <button
                        key={item}
                        className={selections[index] ? "check-item active" : "check-item"}
                        onClick={() => onToggle(section.slug, index)}
                        type="button"
                        disabled={isAcknowledged}
                      >
                        <span className="check-item-indicator" aria-hidden="true">{selections[index] ? <CheckIcon /> : ""}</span>
                        <strong>{item}</strong>
                      </button>
                    ))}
                  </div>
                )}

                <button
                  className={`primary-action${isAcknowledged ? " primary-action--done" : ""}`}
                  disabled={isAcknowledged || !allChecked || isPending}
                  onClick={() => !isAcknowledged && onAcknowledge(section)}
                  aria-disabled={isAcknowledged}
                  type="button"
                >
                  {isAcknowledged ? "Acknowledgment saved" : isPending && pendingAction === "acknowledgment" ? "Saving acknowledgment..." : "Complete acknowledgment"}
                </button>
              </section>

              <section className="content-panel acknowledgment-panel lesson-chapter lesson-chapter--completion lesson-chapter-surface culture-chapter-shell culture-ending-shell" id="section-completion">
                <div className="lesson-chapter-head lesson-chapter-head--completion culture-chapter-head">
                  <p className="section-label">Completion</p>
                  <h2>Finish the module with both required steps</h2>
                  <p className="lesson-chapter-intro">{checkpointDescription}</p>
                </div>
                <div className="culture-ending-layout">
                  <div className="culture-reflection-panel">
                    <p className="section-label">Completion status</p>
                    <div className="module-completion-summary module-completion-summary--stacked">
                      {completionRequirements.map((item) => (
                        <article key={item.label} className={item.complete ? "module-completion-card module-completion-card--done" : "module-completion-card"}>
                          <p className="section-label">{item.label}</p>
                          <strong>{item.complete ? "Complete" : "Required"}</strong>
                          <p>{item.body}</p>
                        </article>
                      ))}
                    </div>
                    <p className="culture-reflection-note">{checkpointNote}</p>
                    <p className="module-completion-helper">{completionHelperNote}</p>
                    <button className={`primary-action${isCompleted ? " primary-action--done" : ""}`} disabled type="button">
                      {completionCtaLabel}
                    </button>
                  </div>
                  <div className="culture-bottom-support">
                    {nextSection && (
                      <article className="culture-bottom-card">
                        <p className="section-label">Next module</p>
                        <strong>{nextSection.title}</strong>
                        <p>{nextSection.summary}</p>
                        <Link className="inline-action" href={`/modules/${nextSection.slug}`}>Preview next</Link>
                      </article>
                    )}
                    {supportContact && (
                      <article className="culture-bottom-card">
                        <p className="section-label">Questions</p>
                        <strong>{supportContact.name}</strong>
                        <span className="culture-contact-role">{supportContact.role}</span>
                        <p>{supportContact.note}</p>
                        <div className="rail-contact-actions">
                          <a className="inline-action" href={`mailto:${supportContact.email}`}>Email</a>
                          <a className="inline-action" href={`tel:${supportPhoneHref}`}>Call</a>
                        </div>
                      </article>
                    )}
                  </div>
                </div>
              </section>
            </>
           ) : (
            <>
              <section className="lesson-chapter lesson-chapter--orientation lesson-chapter-surface chapter-framing-shell" id="section-framing">
                <div className="chapter-framing-layout">
                  <div className="chapter-framing-main">
                    <p className="section-label">Opening</p>
                    <h2>Start with the throughline</h2>
                    <p className="lesson-chapter-intro chapter-framing-copy">{framingCopy}</p>
                  </div>
                  <div className="chapter-support-column">
                    <article className="chapter-support-card chapter-support-card--focus">
                      <p className="section-label">Focus areas</p>
                      <div className="chapter-focus-list">
                        {section.focuses.map((focus) => <span key={focus} className="chapter-focus-chip">{focus}</span>)}
                      </div>
                    </article>
                    <article className="chapter-support-card chapter-support-card--status">
                      <p className="section-label">This chapter</p>
                      <strong>{completionStatus}</strong>
                      <p>{completionStatusNote}</p>
                    </article>
                    {nextSection && (
                      <article className="chapter-support-card chapter-support-card--next">
                        <p className="section-label">Next after this</p>
                        <strong>{nextSection.title}</strong>
                        <p>{nextSection.summary}</p>
                      </article>
                    )}
                  </div>
                </div>
              </section>

              <section className="lesson-chapter lesson-chapter--takeaways lesson-chapter-surface chapter-story-shell" id="section-story">
                <div className="lesson-chapter-head chapter-story-head">
                  <p className="section-label">Main idea</p>
                  <h2>The part to carry with you</h2>
                  <p className="lesson-chapter-intro">Keep the core idea clear enough that it changes how you work, communicate, or make decisions at AAP.</p>
                </div>
                <div className="chapter-story-prose">
                  {narrativeBeats.map((item, index) => (
                    <article key={item.title} className={index === 0 ? "chapter-story-beat chapter-story-beat--lead" : "chapter-story-beat"}>
                      <h3>{item.title}</h3>
                      <p>{item.body}</p>
                    </article>
                  ))}
                </div>
              </section>

              <section className="lesson-chapter lesson-chapter--reference lesson-chapter-surface chapter-example-shell" id="section-example">
                <div className="lesson-chapter-head">
                  <p className="section-label">At AAP</p>
                  <h2>What this looks like at AAP</h2>
                  <p className="lesson-chapter-intro">{exampleIntro}</p>
                </div>
                <div className="chapter-example-layout">
                  {examplePrimary && (
                    <article className="chapter-example-panel">
                      <h3>{examplePrimary.title}</h3>
                      <dl className="policy-list chapter-example-list">
                        {examplePrimary.items.map((item) => (
                          <div key={item.label} className="policy-row">
                            <dt>{item.label}</dt>
                            <dd>{item.body}</dd>
                          </div>
                        ))}
                      </dl>
                    </article>
                  )}
                  {exampleSecondary && (
                    <aside className="chapter-example-side">
                      <article className="chapter-support-card chapter-support-card--example">
                        <p className="section-label">Keep in view</p>
                        <strong>{exampleSecondary.title}</strong>
                        <dl className="policy-list chapter-example-support-list">
                          {exampleSecondary.items.map((item) => (
                            <div key={item.label} className="policy-row">
                              <dt>{item.label}</dt>
                              <dd>{item.body}</dd>
                            </div>
                          ))}
                        </dl>
                      </article>
                    </aside>
                  )}
                </div>
              </section>

              <section className="lesson-chapter lesson-chapter--application lesson-chapter-surface chapter-action-shell" id="section-action">
                <div className="lesson-chapter-head">
                  <p className="section-label">Take action</p>
                  <h2>Use it in the way you work</h2>
                  <p className="lesson-chapter-intro">{actionIntro}</p>
                </div>
                <div className="chapter-action-layout">
                  <article className="chapter-action-main">
                    <p className="section-label">What to do</p>
                    <ul className="plain-list chapter-action-list">
                      {section.actions.map((item) => <li key={item}>{item}</li>)}
                    </ul>
                  </article>
                  <aside className="chapter-action-side">
                    <article className="chapter-support-card chapter-support-card--escalate">
                      <p className="section-label">Escalate when</p>
                      <ul className="plain-list chapter-escalation-list">
                        {section.escalation.map((item) => <li key={item}>{item}</li>)}
                      </ul>
                    </article>
                  </aside>
                </div>
              </section>

              <section className="lesson-chapter lesson-chapter--checkpoint lesson-chapter-surface chapter-knowledge-shell" id="section-knowledge-check">
                <ModuleKnowledgeCheck
                  knowledgeCheck={knowledgeCheck}
                  selections={quizSelections}
                  isPassed={isQuizPassed}
                  isPending={isPending && pendingAction === "quiz"}
                  feedback={quizFeedbackToShow}
                  onSelect={(questionIndex, optionIndex) => onQuizSelect(section.slug, questionIndex, optionIndex)}
                  onSubmit={() => onSubmitKnowledgeCheck(section)}
                />
              </section>

              <section className="lesson-chapter lesson-chapter--acknowledgment lesson-chapter-surface chapter-acknowledgment-shell" id="section-acknowledgment">
                <div className="lesson-chapter-head lesson-chapter-head--completion acknowledgment-section-head">
                  <p className="section-label">Acknowledgment</p>
                  <h2>{section.acknowledgment.title}</h2>
                  <p className="lesson-chapter-intro">This is the final required confirmation after the checkpoint passes.</p>
                </div>
                <p className="acknowledgment-statement">{section.acknowledgment.statement}</p>

                {showChecklist && (
                  <div className="checklist-list">
                    {section.acknowledgment.items.map((item, index) => (
                      <button
                        key={item}
                        className={selections[index] ? "check-item active" : "check-item"}
                        onClick={() => onToggle(section.slug, index)}
                        type="button"
                        disabled={isAcknowledged}
                      >
                        <span className="check-item-indicator" aria-hidden="true">{selections[index] ? <CheckIcon /> : ""}</span>
                        <strong>{item}</strong>
                      </button>
                    ))}
                  </div>
                )}

                <button
                  className={`primary-action${isAcknowledged ? " primary-action--done" : ""}`}
                  disabled={isAcknowledged || !allChecked || isPending}
                  onClick={() => !isAcknowledged && onAcknowledge(section)}
                  aria-disabled={isAcknowledged}
                  type="button"
                >
                  {isAcknowledged ? "Acknowledgment saved" : isPending && pendingAction === "acknowledgment" ? "Saving acknowledgment..." : "Complete acknowledgment"}
                </button>
              </section>

              <section className="content-panel acknowledgment-panel lesson-chapter lesson-chapter--completion lesson-chapter-surface chapter-ending-shell" id="section-completion">
                <div className="lesson-chapter-head lesson-chapter-head--completion">
                  <p className="section-label">Completion</p>
                  <h2>Finish the module with both required steps</h2>
                </div>
                <p className="chapter-ending-copy">{checkpointDescription}</p>
                <p className="module-flow-bridge">Checkpoint first, acknowledgment second, completion last.</p>
                <div className="module-completion-summary">
                  {completionRequirements.map((item) => (
                    <article key={item.label} className={item.complete ? "module-completion-card module-completion-card--done" : "module-completion-card"}>
                      <p className="section-label">{item.label}</p>
                      <strong>{item.complete ? "Complete" : "Required"}</strong>
                      <p>{item.body}</p>
                    </article>
                  ))}
                </div>
                <div className="chapter-reflection-panel">
                  <p className="section-label">Make sure these are clear</p>
                  <ul className="plain-list chapter-reflection-list">
                    {reflectionPrompts.map((prompt) => (
                      <li key={prompt}>
                        <strong>{prompt}</strong>
                      </li>
                    ))}
                  </ul>
                  <p className="chapter-reflection-note">{checkpointNote}</p>
                </div>

                <p className="module-completion-helper">{completionHelperNote}</p>
                <button className={`primary-action${isCompleted ? " primary-action--done" : ""}`} disabled type="button">
                  {completionCtaLabel}
                </button>

                {nextSection && (
                  <p className="finish-next-note">
                    Next after this: <Link className="module-next-link" href={`/modules/${nextSection.slug}`}>{nextSection.title}</Link>
                  </p>
                )}
              </section>
            </>

          )}
        </div>

        <aside className="section-context-rail" aria-label="Module context">
          <CoachTipCard context={tipContext} variant="rail" />
          {nextSection && (
            <article className="rail-context-card rail-context-card--next">
              <p className="section-label">Next module</p>
              <strong>{nextSection.title}</strong>
              <p>{nextSection.summary}</p>
              <Link className="inline-action" href={`/modules/${nextSection.slug}`}>Preview next</Link>
            </article>
          )}
          <article className="rail-context-card rail-context-card--compact">
            <div className="compact-card-section compact-card-section--status">
              <p className="section-label">This module</p>
              <strong>{completionStatus}</strong>
              <p>{completionStatusNote}</p>
            </div>
            {supportContact && (
              <div className="compact-card-section compact-card-section--support">
                <p className="section-label">Your People Person</p>
                <strong>{supportContact.name}</strong>
                <span className="compact-support-role">{supportContact.role}</span>
                <a className="compact-support-detail" href={`mailto:${supportContact.email}`}>{supportContact.email}</a>
                <a className="compact-support-detail" href={`tel:${supportContact.phone.replace(/\D/g, "")}`}>{supportContact.phone}</a>
              </div>
            )}
          </article>
        </aside>
      </div>
    </div>
  );
}
type SupplementalPageScreenProps = {
  page: SupplementalPage;
  contacts: Contact[];
};

function SupplementalPageScreen({ page, contacts }: SupplementalPageScreenProps) {
  const contactMap = new Map(contacts.map((contact) => [contact.id, contact]));

  return (
    <div className="page-stack section-page supplemental-page portal-page portal-page--detail portal-page--supplemental">
      <section className="page-hero single-focus-hero section-hero supplemental-hero">
        <div className="section-hero-copy">
          <p className="section-label">{page.eyebrow}</p>
          <h1>{page.title}</h1>
          <p className="lead">{page.summary}</p>
          <p className="purpose-line">{page.description}</p>
        </div>
        <aside className="summary-panel hero-support-panel supplemental-status-panel">
          <p className="section-label">Launch status</p>
          <strong>{page.state === "coming_soon" ? page.callout ?? "Coming Soon" : "Live"}</strong>
          <p>{page.state === "coming_soon" ? "Visible in nav, excluded from progress." : "Reference page, excluded from progress."}</p>
        </aside>
      </section>

      {page.state === "coming_soon" && (
        <section className="content-panel quiet-content-panel supplemental-callout-panel">
          <p className="section-label">Preview</p>
          <h3>Visible on purpose, not live yet.</h3>
          <div className="essential-grid compact-takeaways">
            {(page.content ?? []).map((item) => (
              <article key={item.title} className="essential-card">
                <strong>{item.title}</strong>
                <p>{item.body}</p>
              </article>
            ))}
          </div>
        </section>
      )}

      {page.state === "live" && (
        <section className="resource-hub-shell">
          {(page.resourceCategories ?? []).map((category) => (
            <article key={category.id} className="content-panel quiet-content-panel resource-category-panel">
              <p className="section-label">Resource category</p>
              <h3>{category.title}</h3>
              <p>{category.description}</p>
              <div className="resource-item-list">
                {category.items.map((item) => {
                  const contact = item.contactId ? contactMap.get(item.contactId) : null;
                  return (
                    <article key={item.id} className="resource-item-card">
                      <p className="section-label">{item.type === "contact" ? "Contact" : item.type === "file" ? "File" : "Link"}</p>
                      <h4>{item.title}</h4>
                      <p>{item.description}</p>
                      {contact ? (
                        <div className="resource-contact-stack">
                          <strong>{contact.name}</strong>
                          <span>{contact.role}</span>
                          {contact.email && <a className="inline-action" href={`mailto:${contact.email}`}>Email</a>}
                          {contact.phone && <a className="inline-action" href={`tel:${contact.phone.replace(/\D/g, "")}`}>Call</a>}
                        </div>
                      ) : item.href ? (
                        <a className="inline-action" href={item.href} download={item.download}>
                          {item.type === "file" ? "Open file" : "Open link"}
                        </a>
                      ) : null}
                    </article>
                  );
                })}
              </div>
            </article>
          ))}
        </section>
      )}
    </div>
  );
}





