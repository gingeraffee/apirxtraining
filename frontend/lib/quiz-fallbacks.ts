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
      {
        id: "welcome-cooperative",
        prompt: "What type of organization is AAP?",
        options: [
          "A publicly traded corporation.",
          "A member-owned cooperative supporting independent pharmacies.",
          "A government agency overseeing pharmacy regulations.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "welcome-day-one",
        prompt: "What is the right goal for day one according to this module?",
        options: [
          "Memorize every policy and procedure.",
          "Get oriented, know the basics, and know where to look.",
          "Complete all system training before end of shift.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "welcome-api",
        prompt: "What is API's relationship to AAP?",
        options: [
          "API is a competitor to AAP.",
          "API continues to operate as AAP's warehouse and distribution arm.",
          "API is the parent company that acquired AAP.",
        ],
        correctOptionIndex: 1,
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
      {
        id: "culture-escalation",
        prompt: "Which of these should be escalated immediately?",
        options: [
          "A coworker arriving five minutes late.",
          "Harassment, retaliation, or threatening conduct.",
          "A preference disagreement about lunch schedules.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "culture-documents",
        prompt: "What should happen to printed materials with sensitive information?",
        options: [
          "Leave them at the shared printer for convenience.",
          "Retrieve them immediately, never leave them unattended, and shred when done.",
          "Store them in your desk drawer indefinitely.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "culture-email",
        prompt: "What is the rule about forwarding work materials to personal email?",
        options: [
          "It is fine as long as you delete them later.",
          "Do not forward work materials to personal email addresses.",
          "Only do it if your manager is copied.",
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
      {
        id: "systems-approved",
        prompt: "What is the policy on using personal tools for company work?",
        options: [
          "Use whatever is fastest.",
          "Store work only in approved company systems.",
          "Personal tools are fine if they are cloud-based.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "systems-support",
        prompt: "Where should IT-related problems and access issues be directed?",
        options: [
          "To any coworker who seems tech-savvy.",
          "To your site's IT team, who generally prefers Teams for requests.",
          "To the company's public website help form.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "systems-day-one",
        prompt: "What is expected regarding system training on your first day?",
        options: [
          "Master every tool before leaving.",
          "Get familiar with key systems; your supervisor and trainer will guide you.",
          "Skip systems training until your second week.",
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
      {
        id: "work-open-door",
        prompt: "What does AAP's open door culture mean?",
        options: [
          "Only speak up during scheduled meetings.",
          "You are encouraged to raise questions, concerns, or ideas with your supervisor or HR at any time.",
          "Wait for a formal review to share feedback.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "work-records",
        prompt: "When personal details change, what should you do?",
        options: [
          "Wait until annual enrollment.",
          "Update HR promptly so your records stay accurate.",
          "Let payroll figure it out on their own.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "work-documentation",
        prompt: "Why is it important to document key interactions?",
        options: [
          "To create a paper trail for legal disputes.",
          "To protect everyone by capturing decisions, commitments, and next steps.",
          "Documentation is optional at AAP.",
        ],
        correctOptionIndex: 1,
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
      {
        id: "benefits-pto",
        prompt: "When does PTO eligibility begin for full-time employees?",
        options: [
          "Immediately on day one.",
          "After 60 days.",
          "After one full year of employment.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "benefits-pay",
        prompt: "Where should pay discrepancies or unexpected deductions be directed?",
        options: [
          "Handle it informally with your manager.",
          "Bring it to HR through the proper channel.",
          "Ignore it and assume it will correct itself.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "benefits-two-day",
        prompt: "What happens after two consecutive workdays of absence without any call-in notification?",
        options: [
          "A verbal warning is issued.",
          "It is treated as a voluntary resignation.",
          "A point is added but nothing else changes.",
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
      {
        id: "support-urgency",
        prompt: "Which of these requires immediate attention rather than waiting until the next business day?",
        options: [
          "A routine PTO request.",
          "A pay discrepancy or safety concern.",
          "A question about the dress code.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "support-language",
        prompt: "When someone raises a sensitive topic, what is the right approach?",
        options: [
          "Speculate about outcomes and reassure them.",
          "Listen, acknowledge, and avoid promising outcomes.",
          "Tell them to handle it on their own.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "support-it",
        prompt: "How does IT generally prefer to receive support requests?",
        options: [
          "Through personal phone calls.",
          "Through Teams.",
          "By walking to the IT department in person.",
        ],
        correctOptionIndex: 1,
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
      {
        id: "safety-responsibility",
        prompt: "Who is responsible for safety at AAP?",
        options: [
          "Only the safety department.",
          "Everyone shares responsibility for safety.",
          "Only managers and supervisors.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "safety-unclear",
        prompt: "What should you do when the safe path for a task is not obvious?",
        options: [
          "Use your best guess and move quickly.",
          "Stop and get direction instead of guessing.",
          "Ask a coworker to do it for you.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "safety-process",
        prompt: "What is the right approach to safety training and local guidance?",
        options: [
          "Skip it if you have prior experience.",
          "Follow the training and guidance that applies to your workspace.",
          "Only review it after an incident occurs.",
        ],
        correctOptionIndex: 1,
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
      {
        id: "first-90-days-intro-period",
        prompt: "What defines the first 60 days at AAP?",
        options: [
          "The probationary review period with mandatory testing.",
          "The introductory period with important attendance expectations and some benefits not yet started.",
          "A self-directed phase with no expectations.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "first-90-days-confidence",
        prompt: "How does confidence develop according to this module?",
        options: [
          "Through memorizing the handbook cover to cover.",
          "Through repetition, practice, and returning to resources when needed.",
          "Through avoiding mistakes at all costs.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "first-90-days-plan",
        prompt: "Who guides the specific milestones for your 30/60/90-day development plan?",
        options: [
          "AAP Start provides the detailed plan.",
          "Your supervisor or trainer based on your role.",
          "You create the plan independently.",
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
      {
        id: "final-review-finish",
        prompt: "Why is the finish line manual on purpose?",
        options: [
          "To slow employees down.",
          "So completion happens when you intentionally mark it, not by reaching the bottom of a page.",
          "To give HR time to review your progress.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "final-review-support",
        prompt: "What should you expect after finishing the launch path?",
        options: [
          "You should no longer need any support.",
          "You should feel oriented and know where to ask questions.",
          "You should memorize all policies before asking anything.",
        ],
        correctOptionIndex: 1,
      },
      {
        id: "final-review-next",
        prompt: "What is the recommended approach for topics that still feel fuzzy?",
        options: [
          "Skip them and move on.",
          "Take one last pass through anything unclear and use your support routes.",
          "Wait until someone brings them up.",
        ],
        correctOptionIndex: 1,
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
