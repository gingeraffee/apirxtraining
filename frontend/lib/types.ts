export type Stat = {
  label: string;
  value: string;
  detail: string;
};

export type Contact = {
  id: string;
  name: string;
  role: string;
  email: string;
  phone: string;
  note: string;
};

export type Acknowledgment = {
  mode: "manual" | "checklist";
  title: string;
  statement: string;
  items: string[];
};

export type Section = {
  id: string;
  slug: string;
  eyebrow: string;
  title: string;
  summary: string;
  purpose: string;
  focuses: string[];
  essentials: { title: string; body: string }[];
  policyAreas: { title: string; items: { label: string; body: string }[] }[];
  actions: string[];
  escalation: string[];
  acknowledgment: Acknowledgment;
};

export type ResourceItem = {
  id: string;
  type: "file" | "link" | "contact";
  title: string;
  description: string;
  href?: string;
  contactId?: string;
  download?: boolean;
};

export type ResourceCategory = {
  id: string;
  title: string;
  description: string;
  items: ResourceItem[];
};

export type SupplementalPage = {
  id: string;
  slug: string;
  eyebrow: string;
  title: string;
  summary: string;
  state: "coming_soon" | "live";
  description: string;
  callout?: string;
  content?: { title: string; body: string }[];
  resourceCategories?: ResourceCategory[];
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
  supportContactId: string;
  section_overrides: Record<string, unknown>;
};

export type ExperienceContent = {
  brand: {
    portalName: string;
  };
  organization: {
    companyName: string;
    companyShortName: string;
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
  supplementalPages: SupplementalPage[];
  toolkits: [];
  track: TrackInfo;
};

export type ProgressRecord = {
  employee_id: string;
  display_name: string | null;
  current_section: string | null;
  completed_sections: string[];
  acknowledged_sections: string[];
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
};
