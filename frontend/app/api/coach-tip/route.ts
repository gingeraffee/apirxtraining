// app/api/coach-tip/route.ts
import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";
export const revalidate = 0;

const FALLBACK_TIPS = [
  { label: "Pro tip",        tip: "Take notes as you go — your future self will genuinely thank you." },
  { label: "Did you know",   tip: "Most people retain more when they pause and summarize what they just read in their own words." },
  { label: "Coach says",     tip: "If something feels unclear, write down the question now. It's easy to forget what confused you once you move on." },
  { label: "Quick heads up", tip: "Your progress saves automatically — you can close the tab and pick up exactly where you left off." },
  { label: "Fun fact",       tip: "Employees who complete structured training in their first week ramp up significantly faster than those who don't." },
  { label: "Pro tip",        tip: "Don't rush the policy modules — they're the ones that actually come up in real situations on the floor." },
  { label: "Coach says",     tip: "Ask your support contact at least one question this week. It breaks the ice and makes everything easier going forward." },
  { label: "Did you know",   tip: "The most common onboarding mistake is skimming compliance sections. They're short for a reason — they matter." },
];

const ANGLES = [
  "Give a counterintuitive angle most people wouldn't expect.",
  "Share a real-world scenario where this knowledge would matter on day one.",
  "Give the kind of tip a veteran employee would whisper to a new hire.",
  "Mention something that sounds obvious but most people actually get wrong.",
  "Frame it as something that separates good employees from great ones.",
  "Give a tip that would make someone's first week noticeably easier.",
  "Share a fun or surprising fact that makes the topic more memorable.",
  "Give advice that applies beyond day one — something that stays useful for months.",
];

const NO_CACHE = {
  "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
  "Pragma": "no-cache",
  "Expires": "0",
};

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const context = searchParams.get("context") ?? "General AAP onboarding";

  const apiKey = process.env.ANTHROPIC_API_KEY;

  // No API key — return a random fallback with a debug flag so we can see it in the response
  if (!apiKey) {
    const fallback = FALLBACK_TIPS[Math.floor(Math.random() * FALLBACK_TIPS.length)];
    return NextResponse.json(
      { ...fallback, _debug: "no_api_key", _rand: Math.random() },
      { headers: NO_CACHE }
    );
  }

  const seed   = Math.floor(Math.random() * 999999);
  const angle  = ANGLES[Math.floor(Math.random() * ANGLES.length)];
  const prefix = ["Pro tip", "Did you know", "Quick heads up", "Coach says", "Fun fact"][
    Math.floor(Math.random() * 5)
  ];

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
            content: `You are a friendly, sharp onboarding coach for AAP (also known as API Rx), a company that operates pharmacies and warehouses. Generate one short tip or fact for this module: "${context}"

Seed: ${seed}
Angle: ${angle}
Required prefix: "${prefix}:"

Rules:
- Start with exactly "${prefix}:" then your tip
- 1–2 sentences max — tight and punchy
- Conversational, slightly witty — never corporate or stiff
- Plain text only, no markdown
- Genuinely fresh — no generic advice`,
          },
        ],
      }),
      cache: "no-store",
    });

    const data = await response.json();
    const full: string = data.content?.[0]?.text?.trim() ?? "";

    const prefixMatch = full.match(/^(Pro tip|Did you know|Quick heads up|Coach says|Fun fact):\s*/i);
    const label = prefixMatch ? prefixMatch[1] : prefix;
    const tip   = prefixMatch ? full.slice(prefixMatch[0].length) : full;

    return NextResponse.json(
      { label, tip, _debug: "api_ok", _seed: seed },
      { headers: NO_CACHE }
    );
  } catch (err) {
    const fallback = FALLBACK_TIPS[Math.floor(Math.random() * FALLBACK_TIPS.length)];
    return NextResponse.json(
      { ...fallback, _debug: "api_error", _err: String(err) },
      { headers: NO_CACHE }
    );
  }
}
