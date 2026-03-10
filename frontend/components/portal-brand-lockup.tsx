import Image from "next/image";

type PortalBrandLockupProps = {
  className?: string;
  priority?: boolean;
};

export function PortalBrandLockup({
  className = "",
  priority = false,
}: PortalBrandLockupProps) {
  const lockupClassName = ["portal-brand-lockup", className].filter(Boolean).join(" ");

  return (
    <div className={lockupClassName}>
      <Image
        src="/logo.png"
        alt="American Associated Pharmacies logo"
        width={900}
        height={286}
        priority={priority}
        className="brand-logo-img portal-lockup-logo"
      />
      <div className="portal-brand-caption">
        <span className="portal-brand-caption-label">Employee onboarding portal</span>
        <strong className="portal-brand-product-name">AAP Start</strong>
        <span className="portal-brand-caption-subline">American Associated Pharmacies</span>
      </div>
    </div>
  );
}

