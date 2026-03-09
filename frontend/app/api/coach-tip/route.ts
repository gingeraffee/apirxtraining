// app/api/coach-tip/route.ts
import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";
export const revalidate = 0;

const FALLBACK_TIPS = [
  { label: "Pro tip", tip: "Pause after each module and sum it up in your own words. It makes the useful stuff stick." },
  { label: "Did you know", tip: "Manual completion is a feature, not friction. It gives you a clean moment to decide whether the module actually landed." },
  { label: "Coach says", tip: "If something feels unclear, write the question down right then. Future you will forget the exact snag." },
  { label: "Quick heads up", tip: "Resource Hub is there for the stuff you want to revisit later, so you do not need to memorize everything on the first pass." },
  { label: "Fun fact", tip: "The fastest onboarding usually feels the clearest, not the densest." },
  { label: "Pro tip", tip: "Do not rush the policy modules. They are the ones that tend to matter in real situations first." },
  { label: "Coach says", tip: "Ask at least one real question this week. It makes the portal feel like support instead of homework." },
  { label: "Did you know", tip: "Most people remember more when they connect a policy to a real day-one scenario instead of trying to memorize the wording." },
];

const ANGLES = [
  "Give a counterintuitive angle most people would not expect.",
  "Share a real-world scenario where this knowledge would matter on day one.",
  "Give the kind of tip a veteran employee would quietly hand to a new hire.",
  "Mention something that sounds obvious but most people actually get wrong.",
  "Frame it as something that makes the first week noticeably easier.",
  "Share a fun or surprising fact that makes the topic more memorable.",
  "Give advice that stays useful beyond launch week.",
];

const NO_CACHE = {
  "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
  Pragma: "no-cache",
  Expires: "0",
};

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const context = searchParams.get("context") ?? "AAP Start launch onboarding";

  const apiKey = process.env.ANTHROPIC_API_KEY;

  if (!apiKey) {
    const fallback = FALLBACK_TIPS[Math.floor(Math.random() * FALLBACK_TIPS.length)];
    return NextResponse.json({ ...fallback, _debug: "no_api_key", _rand: Math.random() }, { headers: NO_CACHE });
  }

  const seed = Math.floor(Math.random() * 999999);
  const angle = ANGLES[Math.floor(Math.random() * ANGLES.length)];
  const prefix = ["Pro tip", "Did you know", "Quick heads up", "Coach says", "Fun fact"][Math.floor(Math.random() * 5)];

  try {
    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-haiku-4-5-20251001",
        max_tokens: 120,
        messages: [
          {
            role: "user",
            content: `You are a friendly, sharp onboarding coach for AAP Start, the launch onboarding portal for American Associated Pharmacies. Generate one short tip or fact for this module: "${context}"

Seed: ${seed}
Angle: ${angle}
Required prefix: "${prefix}:"

Rules:
- Start with exactly "${prefix}:" then your tip
- 1-2 sentences max
- Conversational, slightly witty, never corporate
- Plain text only, no markdown
- Keep it launch-safe: no invented policies, no fake legal specifics, no made-up system claims
- Avoid saying progress saves automatically
- Make it feel genuinely fresh, not generic`,
          },
        ],
      }),
      cache: "no-store",
    });

    const data = await response.json();
    const full: string = data.content?.[0]?.text?.trim() ?? "";

    const prefixMatch = full.match(/^(Pro tip|Did you know|Quick heads up|Coach says|Fun fact):\s*/i);
    const label = prefixMatch ? prefixMatch[1] : prefix;
    const tip = prefixMatch ? full.slice(prefixMatch[0].length) : full;

    return NextResponse.json({ label, tip, _debug: "api_ok", _seed: seed }, { headers: NO_CACHE });
  } catch (err) {
    const fallback = FALLBACK_TIPS[Math.floor(Math.random() * FALLBACK_TIPS.length)];
    return NextResponse.json({ ...fallback, _debug: "api_error", _err: String(err) }, { headers: NO_CACHE });
  }
}
