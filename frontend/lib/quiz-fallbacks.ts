import type { ExperienceContent, KnowledgeCheck, Section } from "@/lib/types";

const QUIZ_FALLBACKS: Record<string, KnowledgeCheck> = {
  "welcome-to-aap": {
    title: "Knowledge Check",
    intro: "Complete this required check before you move into the acknowledgment step.",
    passingPercent: 1,
    questions: [
      {
        id: "welcome-purpose",
        prompt: "Which description best matches what AAP Start is for?",
        options: [
          "A place to memorize every policy on day one.",
          "A guided launch path that orients you, shows where to look, and helps you know where questions go.",
          "A role-specific toolkit that replaces supervisor training.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "welcome-support",
        prompt: "Who is the primary onboarding and employee-support contact named in this module?",
        options: ["Nicole Thornton, HR Manager", "CBIZ Benefits", "LifeMatters"],
        correctOptionIndex: 0,
      },
    ],
  },
  "how-we-show-up": {
    title: "Knowledge Check",
    intro: "This required check confirms the practical culture habits from this chapter before you acknowledge it.",
    passingPercent: 1,
    questions: [
      {
        id: "culture-directness",
        prompt: "When you do not know the answer to a sensitive question, what is the best response?",
        options: [
          "Give your best guess so the conversation keeps moving.",
          "Say you need to check and follow up through the right channel.",
          "Share the question with anyone nearby until someone answers it.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "culture-privacy",
        prompt: "What should you do if you suspect a privacy breach or unauthorized access?",
        options: [
          "Wait to see if it becomes a larger problem.",
          "Report it to HR and IT right away.",
          "Mention it casually to a teammate and move on.",
        ],
        correctOptionIndex: 1,
      },
    ],
  },
  "tools-and-systems": {
    title: "Knowledge Check",
    intro: "Pass this required check before you acknowledge the systems basics for this module.",
    passingPercent: 1,
    questions: [
      {
        id: "systems-passwords",
        prompt: "Where should work passwords be stored?",
        options: [
          "In your personal notes app so you can reach them anywhere.",
          "Only in the approved company password manager.",
          "In a shared team spreadsheet so backup coverage is easy.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "systems-access",
        prompt: "What should you do if a key system is not working during your first week?",
        options: [
          "Build a workaround and ask about it later.",
          "Flag it early through the right support path.",
          "Share your credentials with a teammate who has access.",
        ],
        correctOptionIndex: 1,
      },
    ],
  },
  "how-work-works": {
    title: "Knowledge Check",
    intro: "Use this required check to confirm the work habits and support lanes from the chapter.",
    passingPercent: 1,
    questions: [
      {
        id: "work-follow-up",
        prompt: "If a deadline or follow-up you promised is going to change, what should you do?",
        options: [
          "Wait until the original deadline passes, then explain what happened.",
          "Communicate the change before the deadline passes.",
          "Assume people will understand if the work is important enough.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "work-hr-lane",
        prompt: "Which team owns people, policy, pay, and other sensitive employee issues?",
        options: ["HR", "IT", "Any experienced coworker"],
        correctOptionIndex: 0,
      },
    ],
  },
  "benefits-pay-and-time-away": {
    title: "Knowledge Check",
    intro: "This required check keeps the basics practical before you move into the acknowledgment.",
    passingPercent: 1,
    questions: [
      {
        id: "benefits-attendance",
        prompt: "What does two consecutive months of perfect attendance do under this module's attendance overview?",
        options: [
          "It removes one point early.",
          "It adds a floating holiday.",
          "It resets your entire attendance record.",
        ],
        correctOptionIndex: 0,
      },
      {
        id: "benefits-leave",
        prompt: "If a time-away question involves a medical situation or FMLA, what is the right move?",
        options: [
          "Wait for your next annual review to bring it up.",
          "Move it to HR directly.",
          "Ask a coworker what usually happens.",
        ],
        correctOptionIndex: 1,
      },
    ],
  },
  "support-leave-and-employee-resources": {
    title: "Knowledge Check",
    intro: "Pass this required check to confirm where support should go before you acknowledge the module.",
    passingPercent: 1,
    questions: [
      {
        id: "support-hr",
        prompt: "Where should medical, leave, and accommodation questions go?",
        options: ["To HR directly", "To the Resource Hub only", "To any teammate who has handled it before"],
        correctOptionIndex: 0,
      },
      {
        id: "support-eap",
        prompt: "How can employees use LifeMatters?",
        options: [
          "Only after HR approval",
          "Only after 90 days",
          "Confidentially from day one without a referral",
        ],
        correctOptionIndex: 2,
      },
    ],
  },
  "safety-at-aap": {
    title: "Knowledge Check",
    intro: "Finish this required check before you acknowledge the shared safety expectations.",
    passingPercent: 1,
    questions: [
      {
        id: "safety-urgent",
        prompt: "If something feels unsafe or threatening, what should you do?",
        options: [
          "Wait for a calmer time to mention it.",
          "Escalate it immediately.",
          "Keep working unless someone else stops.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "safety-reporting",
        prompt: "Which answer reflects the module's safety standard?",
        options: [
          "Near misses and hazards should be reported promptly.",
          "Only injuries that require medical treatment need to be reported.",
          "Minor hazards are fine if you can work around them.",
        ],
        correctOptionIndex: 0,
      },
    ],
  },
  "your-first-90-days": {
    title: "Knowledge Check",
    intro: "Use this required check to confirm the practical expectations for your first stretch at AAP.",
    passingPercent: 1,
    questions: [
      {
        id: "first-90-days-day-one",
        prompt: "What is day one mainly for according to this module?",
        options: [
          "Orientation and getting settled",
          "Independent mastery of your full role",
          "Completing every system training in one day",
        ],
        correctOptionIndex: 0,
      },
      {
        id: "first-90-days-questions",
        prompt: "What is the better move when something still feels unclear in your first 90 days?",
        options: [
          "Stay quiet until you have a perfect question.",
          "Ask early and use your support routes.",
          "Wait until onboarding is fully finished.",
        ],
        correctOptionIndex: 1,
      },
    ],
  },
  "final-review-and-acknowledgment": {
    title: "Knowledge Check",
    intro: "Complete this required final check before you finish the tracked launch path.",
    passingPercent: 1,
    questions: [
      {
        id: "final-review-reference",
        prompt: "What does successful launch completion mean in this module?",
        options: [
          "You memorized every policy detail.",
          "You know the essentials, where to look, and who to ask.",
          "You should not need support anymore.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "final-review-hub",
        prompt: "How should you use the Resource Hub after onboarding?",
        options: [
          "As a live reference shelf for files, contacts, and refreshers.",
          "Only if your manager gives written approval.",
          "Only after all future modules are released.",
        ],
        correctOptionIndex: 0,
      },
    ],
  },
};

function buildUnavailableFallback(section: Section): KnowledgeCheck {
  return {
    title: "Knowledge Check",
    intro: `The quiz content for ${section.title} is still loading. Refresh after the backend updates, then complete the required check before acknowledgment.`,
    passingPercent: 1,
    questions: [],
  };
}

export function normalizeExperienceContent(experience: ExperienceContent): ExperienceContent {
  return {
    ...experience,
    sections: experience.sections.map((section) => ({
      ...section,
      knowledgeCheck: section.knowledgeCheck ?? QUIZ_FALLBACKS[section.slug] ?? buildUnavailableFallback(section),
    })),
  };
}
