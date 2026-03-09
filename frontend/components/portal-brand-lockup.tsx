import Image from "next/image";

type PortalBrandLockupProps = {
  className?: string;
  copyClassName?: string;
  priority?: boolean;
};

export function PortalBrandLockup({
  className = "",
  copyClassName = "",
  priority = false,
}: PortalBrandLockupProps) {
  const lockupClassName = ["portal-brand-lockup", className].filter(Boolean).join(" ");
  const brandCopyClassName = ["portal-brand", copyClassName].filter(Boolean).join(" ");

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
      <div className={brandCopyClassName}>
        <span className="portal-brand-overline">Launch onboarding</span>
        <strong>AAP Start</strong>
        <span className="portal-brand-subline">American Associated Pharmacies</span>
      </div>
    </div>
  );
}

