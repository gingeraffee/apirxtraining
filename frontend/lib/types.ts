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
  purpose: string;
  focuses: string[];
  essentials: { title: string; body: string }[];
  policyAreas: { title: string; items: { label: string; body: string }[] }[];
  actions: string[];
  escalation: string[];
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
  purpose: string;
  whenToUse: string[];
  systems: { name: string; link: string; use: string }[];
  playbooks: { title: string; summary: string; doThis: string[]; escalateWhen: string[] }[];
  quickAnswers: { question: string; answer: string; reference: string }[];
  escalateImmediately: string[];
  contacts: { name: string; role: string; phone: string; email: string }[];
  acknowledgment: {
    title: string;
    statement: string;
    items: string[];
  };
};

export type SupportContact = {
  name: string;
  role: string;
  phone: string;
  email: string;
};

export type TrackInfo = {
  id: string;
  name: string;
  support_contact: SupportContact;
  toolkit_slugs: string[];
  section_overrides: Record<string, unknown>;
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
  track: TrackInfo;
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
