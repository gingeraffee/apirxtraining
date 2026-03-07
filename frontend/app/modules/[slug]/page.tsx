import { PortalExperience } from "@/components/portal-experience";

export default async function ModulePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  return <PortalExperience kind="section" slug={slug} />;
}
