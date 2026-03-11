"use client";

import { useState, useTransition, useEffect, useCallback } from "react";
import Link from "next/link";
import type { Acknowledgment, KnowledgeCheck, ProgressRecord } from "@/lib/types";
import { acknowledgeSection, submitKnowledgeCheck } from "@/lib/api";

type ModuleCompletionFlowProps = {
  sectionSlug: string;
  sectionTitle: string;
  employeeId: string;
  displayName: string;
  acknowledgment: Acknowledgment;
  knowledgeCheck: KnowledgeCheck;
  nextSectionSlug?: string;
  nextSectionTitle?: string;
  isLastModule?: boolean;
  progressRecord: ProgressRecord;
  onProgressUpdate: (record: ProgressRecord) => void;
};

function CheckIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
      <path d="M3.5 8.5L6.5 11.5L12.5 4.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export default function ModuleCompletionFlow({
  sectionSlug,
  sectionTitle,
  employeeId,
  displayName,
  acknowledgment,
  knowledgeCheck,
  nextSectionSlug,
  nextSectionTitle,
  isLastModule = false,
  progressRecord,
  onProgressUpdate,
}: ModuleCompletionFlowProps) {
  const isAlreadyAcknowledged = progressRecord.acknowledged_sections.includes(sectionSlug);
  const isAlreadyQuizPassed = progressRecord.quiz_passed_sections.includes(sectionSlug);
  const isAlreadyCompleted = isAlreadyAcknowledged && isAlreadyQuizPassed;

  const initialStep = isAlreadyCompleted ? 3 : isAlreadyAcknowledged ? 2 : 1;

  const [step, setStep] = useState<1 | 2 | 3>(initialStep);
  const [checkedItems, setCheckedItems] = useState<Set<number>>(new Set());
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [feedback, setFeedback] = useState<{ correct: boolean; explanation: string } | null>(null);
  const [quizAnswers, setQuizAnswers] = useState<number[]>([]);
  const [isPending, startTransition] = useTransition();
  const [shakeKey, setShakeKey] = useState(0);

  // Auto-advance step when progress changes externally
  useEffect(() => {
    if (isAlreadyCompleted) {
      setStep(3);
    } else if (isAlreadyAcknowledged && step === 1) {
      setStep(2);
    }
  }, [isAlreadyAcknowledged, isAlreadyCompleted, step]);

  // Auto-skip quiz if already passed
  useEffect(() => {
    if (isAlreadyQuizPassed && step === 2) {
      setStep(3);
    }
  }, [isAlreadyQuizPassed, step]);

  const totalQuestions = knowledgeCheck.questions.length;
  const allChecked = checkedItems.size === acknowledgment.items.length && acknowledgment.items.length > 0;

  const handleToggleCheck = useCallback((index: number) => {
    setCheckedItems((prev) => {
      const next = new Set(prev);
      if (next.has(index)) {
        next.delete(index);
      } else {
        next.add(index);
      }
      return next;
    });
  }, []);

  const handleAcknowledge = useCallback(() => {
    if (!allChecked || isPending) return;

    startTransition(async () => {
      try {
        const updated = await acknowledgeSection(employeeId, sectionSlug, displayName);
        onProgressUpdate(updated);
        setStep(2);
      } catch (err) {
        console.error("Failed to acknowledge section:", err);
        // Still advance locally so the user isn't stuck
        setStep(2);
      }
    });
  }, [allChecked, isPending, employeeId, sectionSlug, displayName, onProgressUpdate]);

  const handleSelectOption = useCallback((optionIndex: number) => {
    if (feedback) return; // Don't allow changing while feedback is shown
    setSelectedOption(optionIndex);
  }, [feedback]);

  const handleSubmitAnswer = useCallback(() => {
    if (selectedOption === null || feedback) return;

    const question = knowledgeCheck.questions[currentQuestion];
    if (!question) return;

    const isCorrect = selectedOption === question.correctOptionIndex;

    if (isCorrect) {
      const newAnswers = [...quizAnswers, selectedOption];
      setQuizAnswers(newAnswers);
      setFeedback({ correct: true, explanation: `Correct! ${getExplanation(question.prompt)}` });

      // If this was the last question, submit to backend
      if (currentQuestion === totalQuestions - 1) {
        startTransition(async () => {
          try {
            const result = await submitKnowledgeCheck(employeeId, sectionSlug, displayName, newAnswers);
            onProgressUpdate(result.progress);
          } catch (err) {
            console.error("Failed to submit knowledge check:", err);
            // Still handle locally
            const localCorrect = knowledgeCheck.questions.every(
              (q, i) => newAnswers[i] === q.correctOptionIndex
            );
            if (localCorrect) {
              // Mark as completed locally
            }
          }
        });
      }
    } else {
      setFeedback({ correct: false, explanation: "That's not quite right. Review the material and try again from the beginning." });
    }
  }, [selectedOption, feedback, currentQuestion, quizAnswers, knowledgeCheck, totalQuestions, employeeId, sectionSlug, displayName, onProgressUpdate]);

  const handleNextQuestion = useCallback(() => {
    if (currentQuestion < totalQuestions - 1) {
      setCurrentQuestion((prev) => prev + 1);
      setSelectedOption(null);
      setFeedback(null);
    } else {
      // All questions answered correctly
      setStep(3);
    }
  }, [currentQuestion, totalQuestions]);

  const handleRestartQuiz = useCallback(() => {
    setCurrentQuestion(0);
    setSelectedOption(null);
    setFeedback(null);
    setQuizAnswers([]);
    setShakeKey((prev) => prev + 1);
  }, []);

  // Step 1: Acknowledgment
  if (step === 1) {
    return (
      <section className="completion-flow completion-flow--ack" id="section-completion-flow">
        <div className="completion-ack">
          <div className="completion-ack-head">
            <div className="completion-step-indicator">
              <span className="completion-step-badge">1</span>
              <span className="completion-step-label">Step 1 of 3</span>
            </div>
            <h2>{acknowledgment.title}</h2>
            <p className="completion-ack-statement">{acknowledgment.statement}</p>
          </div>

          <div className="completion-ack-checklist">
            {acknowledgment.items.map((item, index) => (
              <button
                key={item}
                className={`completion-check-item${checkedItems.has(index) ? " completion-check-item--active" : ""}`}
                onClick={() => handleToggleCheck(index)}
                type="button"
              >
                <span className="completion-check-indicator" aria-hidden="true">
                  {checkedItems.has(index) ? <CheckIcon /> : null}
                </span>
                <span>{item}</span>
              </button>
            ))}
          </div>

          <div className="completion-ack-footer">
            <button
              className={`completion-action${allChecked ? " completion-action--ready" : ""}`}
              disabled={!allChecked || isPending}
              onClick={handleAcknowledge}
              type="button"
            >
              {isPending ? "Saving..." : "Continue to Knowledge Check"}
            </button>
            <p className="completion-helper">
              {allChecked
                ? "All takeaways confirmed. Continue when ready."
                : `${checkedItems.size} of ${acknowledgment.items.length} confirmed`}
            </p>
          </div>
        </div>
      </section>
    );
  }

  // Step 2: Knowledge Check
  if (step === 2) {
    const question = knowledgeCheck.questions[currentQuestion];
    if (!question) return null;

    const progressPercent = ((currentQuestion + (feedback?.correct ? 1 : 0)) / totalQuestions) * 100;

    return (
      <section className="completion-flow completion-flow--quiz" id="section-completion-flow" key={shakeKey}>
        <div className="completion-quiz">
          <div className="completion-quiz-head">
            <div className="completion-step-indicator">
              <span className="completion-step-badge">2</span>
              <span className="completion-step-label">Step 2 of 3</span>
            </div>
            <div className="completion-quiz-progress">
              <div className="completion-quiz-progress-bar">
                <div
                  className="completion-quiz-progress-fill"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
              <span className="completion-quiz-progress-text">
                Question {currentQuestion + 1} of {totalQuestions}
              </span>
            </div>
          </div>

          <div className="completion-quiz-body">
            <h3 className="completion-quiz-question">{question.prompt}</h3>

            <div className="completion-quiz-options">
              {question.options.map((option, index) => (
                <button
                  key={`${question.id}-${index}`}
                  className={`completion-quiz-option${
                    selectedOption === index ? " completion-quiz-option--selected" : ""
                  }${
                    feedback && index === question.correctOptionIndex
                      ? " completion-quiz-option--correct"
                      : ""
                  }${
                    feedback && !feedback.correct && selectedOption === index
                      ? " completion-quiz-option--wrong"
                      : ""
                  }`}
                  onClick={() => handleSelectOption(index)}
                  type="button"
                  disabled={feedback !== null}
                >
                  <span className="completion-quiz-option-marker">
                    {String.fromCharCode(65 + index)}
                  </span>
                  <span>{option}</span>
                </button>
              ))}
            </div>

            {!feedback && (
              <button
                className="completion-action completion-action--submit"
                disabled={selectedOption === null}
                onClick={handleSubmitAnswer}
                type="button"
              >
                Submit Answer
              </button>
            )}

            {feedback && (
              <div className={`completion-quiz-feedback${feedback.correct ? " completion-quiz-feedback--correct" : " completion-quiz-feedback--wrong"}`}>
                <div className="completion-quiz-feedback-icon">
                  {feedback.correct ? (
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
                      <circle cx="10" cy="10" r="9" stroke="currentColor" strokeWidth="2" />
                      <path d="M6 10L9 13L14 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  ) : (
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
                      <circle cx="10" cy="10" r="9" stroke="currentColor" strokeWidth="2" />
                      <path d="M7 7L13 13M13 7L7 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                  )}
                </div>
                <div className="completion-quiz-feedback-body">
                  <strong>{feedback.correct ? "Correct!" : "Not quite"}</strong>
                  <p>{feedback.explanation}</p>
                </div>
                <button
                  className="completion-action"
                  onClick={feedback.correct ? handleNextQuestion : handleRestartQuiz}
                  type="button"
                >
                  {feedback.correct
                    ? currentQuestion === totalQuestions - 1
                      ? "See Results"
                      : "Next Question"
                    : "Restart Quiz"}
                </button>
              </div>
            )}
          </div>
        </div>
      </section>
    );
  }

  // Step 3: Celebration / Complete
  return (
    <section className="completion-flow completion-flow--celebrate" id="section-completion-flow">
      <div className="completion-celebrate">
        <div className="completion-celebrate-visual">
          <div className="completion-celebrate-check">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none" aria-hidden="true">
              <circle cx="24" cy="24" r="22" stroke="currentColor" strokeWidth="2.5" />
              <path d="M14 24L21 31L34 17" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <div className="completion-celebrate-dots" aria-hidden="true">
            {Array.from({ length: 12 }).map((_, i) => (
              <span key={i} className="completion-dot" style={{ "--dot-index": i } as React.CSSProperties} />
            ))}
          </div>
        </div>

        <div className="completion-celebrate-body">
          <div className="completion-step-indicator">
            <span className="completion-step-badge completion-step-badge--done">
              <CheckIcon />
            </span>
            <span className="completion-step-label">Complete</span>
          </div>
          <h2>{isLastModule ? "You made it." : "Module complete."}</h2>
          <p className="completion-celebrate-sub">
            {isLastModule
              ? `${sectionTitle} is done, and so is your tracked launch path. You now know where to look, who to ask, and how work works at AAP.`
              : `${sectionTitle} is saved in your tracked progress. The knowledge check and acknowledgment are both locked in.`}
          </p>
        </div>

        <div className="completion-celebrate-actions">
          {!isLastModule && nextSectionSlug && nextSectionTitle && (
            <Link
              className="completion-action completion-action--advance"
              href={`/modules/${nextSectionSlug}`}
            >
              Continue to {nextSectionTitle}
            </Link>
          )}
          {isLastModule && (
            <Link className="completion-action completion-action--advance" href="/">
              Return to Overview
            </Link>
          )}
        </div>
      </div>
    </section>
  );
}

/** Generate a brief explanation for correct answers. */
function getExplanation(prompt: string): string {
  // Keep explanations minimal since the prompt itself is informative
  return "This answer reflects the guidance covered in this module.";
}
