import type { SupportContact as SupportContactData } from "@/lib/types";

type SupportContactProps = {
  contact: SupportContactData;
};

export function SupportContact({ contact }: SupportContactProps) {
  const vCard = [
    "BEGIN:VCARD",
    "VERSION:3.0",
    `FN:${contact.name}`,
    `N:${contact.name.split(" ").reverse().join(";")};;;`,
    `TITLE:${contact.role}`,
    `TEL;TYPE=WORK,VOICE:${contact.phone}`,
    `EMAIL;TYPE=INTERNET:${contact.email}`,
    "END:VCARD",
  ].join("\n");
  const vCardUrl = `data:text/vcard;charset=utf-8,${encodeURIComponent(vCard)}`;
  const firstName = contact.name.split(" ")[0];
  const phoneDigits = contact.phone.replace(/\D/g, "");

  return (
    <section className="ov-support">
      <div className="ov-support-copy">
        <p className="section-label">Need help?</p>
        <h3>Your assigned support contact</h3>
        <p>
          Reach out anytime a lesson feels unclear or a policy scenario
          needs direct guidance.
        </p>
      </div>

      <div className="ov-support-card">
        <div className="ov-support-identity">
          <strong>{contact.name}</strong>
          <span>{contact.role}</span>
        </div>
        <div className="ov-support-details">
          <p>
            <a href={`tel:${phoneDigits}`}>{contact.phone}</a>
          </p>
          <p>
            <a href={`mailto:${contact.email}`}>{contact.email}</a>
          </p>
        </div>
        <div className="ov-support-actions">
          <a className="inline-action" href={`tel:${phoneDigits}`}>
            Call {firstName}
          </a>
          <a className="inline-action" href={`mailto:${contact.email}`}>
            Email {firstName}
          </a>
          <a
            className="inline-action"
            href={vCardUrl}
            download={`${contact.name.toLowerCase().replace(/\s/g, "-")}.vcf`}
          >
            Save contact
          </a>
        </div>
        <div className="ov-support-future" aria-hidden="true">
          {/* Virtual business card / QR code area — prepared for future rollout */}
        </div>
      </div>
    </section>
  );
}
