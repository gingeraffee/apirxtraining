import type { KnowledgeCheck } from "@/lib/types";

export type KnowledgeCheckFeedback = {
  state: "needs-answers" | "failed" | "passed";
  title: string;
  body: string;
  scoreLabel?: string;
};

type ModuleKnowledgeCheckProps = {
  knowledgeCheck: KnowledgeCheck;
  selections: Array<number | null>;
  isPassed: boolean;
  isPending: boolean;
  feedback: KnowledgeCheckFeedback | null;
  onSelect: (questionIndex: number, optionIndex: number) => void;
  onSubmit: () => void;
};

const OPTION_LABELS = ["A", "B", "C", "D", "E"];

export function ModuleKnowledgeCheck({ knowledgeCheck, selections, isPassed, isPending, feedback, onSelect, onSubmit }: ModuleKnowledgeCheckProps) {
  const questionCount = knowledgeCheck.questions.length;

  return (
    <section className="module-quiz" aria-labelledby="module-quiz-title">
      <div className="module-quiz-head">
        <div className="module-quiz-head-copy">
          <p className="section-label">Required checkpoint</p>
          <h2 id="module-quiz-title">{knowledgeCheck.title}</h2>
          <p className="module-quiz-intro">{knowledgeCheck.intro}</p>
        </div>
        <div className="module-quiz-meta">
          <span className={`module-quiz-status${isPassed ? " module-quiz-status--passed" : ""}`}>{isPassed ? "Passed" : "Required"}</span>
          <span className="module-quiz-count">{questionCount === 1 ? "1 question" : `${questionCount} questions`}</span>
        </div>
      </div>

      <p className="module-quiz-note">Confirm the key ideas here, then move into the acknowledgment step.</p>

      {questionCount > 0 ? (
        <>
          <div className="module-quiz-question-list">
            {knowledgeCheck.questions.map((question, questionIndex) => (
              <article key={question.id} className="module-quiz-question">
                <div className="module-quiz-question-head">
                  <span className="module-quiz-number">{questionIndex + 1}</span>
                  <div className="module-quiz-question-copy">
                    <p className="module-quiz-question-kicker">Choose one answer</p>
                    <h3>{question.prompt}</h3>
                  </div>
                </div>
                <div className="module-quiz-options" role="radiogroup" aria-label={question.prompt}>
                  {question.options.map((option, optionIndex) => {
                    const selected = selections[questionIndex] === optionIndex;
                    return (
                      <button
                        key={option}
                        className={selected ? "module-quiz-option active" : "module-quiz-option"}
                        onClick={() => onSelect(questionIndex, optionIndex)}
                        type="button"
                        disabled={isPassed || isPending}
                        aria-pressed={selected}
                      >
                        <span className="module-quiz-option-key">{OPTION_LABELS[optionIndex] ?? String(optionIndex + 1)}</span>
                        <span className="module-quiz-option-copy">{option}</span>
                        <span className="module-quiz-option-state" aria-hidden="true">{selected ? "Selected" : ""}</span>
                      </button>
                    );
                  })}
                </div>
              </article>
            ))}
          </div>

          {feedback && (
            <div className={`module-quiz-feedback module-quiz-feedback--${feedback.state}`} role="status" aria-live="polite">
              <span className="module-quiz-feedback-kicker">{feedback.state === "passed" ? "Ready for the next step" : feedback.state === "needs-answers" ? "Almost there" : "Try once more"}</span>
              <strong>{feedback.title}</strong>
              <p>{feedback.body}</p>
              {feedback.scoreLabel && <span className="module-quiz-feedback-score">{feedback.scoreLabel}</span>}
            </div>
          )}

          <div className="module-quiz-footer">
            <button className={`primary-action module-quiz-submit${isPassed ? " primary-action--done" : ""}`} onClick={onSubmit} disabled={isPassed || isPending} type="button">
              {isPassed ? "Knowledge check passed" : isPending ? "Checking answers..." : "Check answers"}
            </button>
            <p className="module-quiz-footer-note">The module stays locked until this checkpoint passes and the acknowledgment is saved.</p>
          </div>
        </>
      ) : (
        <div className="module-quiz-feedback module-quiz-feedback--needs-answers" role="status">
          <span className="module-quiz-feedback-kicker">Quiz unavailable</span>
          <strong>Knowledge check content is still syncing</strong>
          <p>Refresh after the backend updates, then complete this step before acknowledgment.</p>
        </div>
      )}
    </section>
  );
}
