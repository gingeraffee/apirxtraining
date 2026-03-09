import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Manrope, Inter } from "next/font/google";

import "./globals.css";
import "./globals-refined.css";

const manrope = Manrope({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
  variable: "--font-display",
  display: "swap",
});

const inter = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-ui",
  display: "swap",
});

export const metadata: Metadata = {
  title: "AAP Start",
  description: "AAP Start is the launch onboarding portal for American Associated Pharmacies.",
};

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en" className={`${manrope.variable} ${inter.variable}`}>
      <body>{children}</body>
    </html>
  );
}
