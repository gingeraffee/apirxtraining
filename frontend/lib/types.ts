export type Stat = {
  label: string;
  value: string;
  detail: string;
};

export type Contact = {
  name: string;
  role: string;
  email: string;
  phone: string;
  note: string;
};

export type Section = {
  id: string;
  slug: string;
  eyebrow: string;
  title: string;
  summary: string;
  estimatedMinutes: number;
  punchline: string;
  quickFacts: { label: string; value: string }[];
  highlightCards: { title: string; body: string; tone: string }[];
  timeline: { label: string; title: string; body: string }[];
  takeaways: string[];
  reminders: string[];
  faq: { question: string; answer: string }[];
  resources: { title: string; body: string }[];
  acknowledgment: {
    title: string;
    statement: string;
    items: string[];
  };
};

export type Toolkit = {
  id: string;
  slug: string;
  eyebrow: string;
  title: string;
  summary: string;
  estimatedMinutes: number;
  punchline: string;
  hero: { title: string; body: string };
  overviewCards: { title: string; body: string }[];
  systems: { name: string; link: string; use: string }[];
  playbooks: { title: string; body: string; steps: string[]; escalateWhen: string[] }[];
  escalationContacts: { name: string; role: string; phone: string; email: string }[];
  quickLinks: string[];
  reminders: string[];
};

export type ExperienceContent = {
  organization: {
    name: string;
    headline: string;
    tagline: string;
    mission: string;
    vision: string;
    story: string;
    values: { name: string; body: string }[];
  };
  dashboardStats: Stat[];
  contacts: Contact[];
  sections: Section[];
  toolkits: Toolkit[];
};

export type ProgressRecord = {
  employee_id: string;
  display_name: string | null;
  current_section: string | null;
  completed_sections: string[];
  acknowledged_sections: string[];
  toolkit_completed: boolean;
  started_at: string | null;
  updated_at: string | null;
  core_total_sections: number;
  core_completion_ratio: number;
};

export type ProgressUpdate = {
  display_name?: string;
  current_section?: string | null;
  completed_sections: string[];
  acknowledged_sections: string[];
  toolkit_completed: boolean;
};
