import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Anton - AI Companion",
  description: "Your AI companion for Hytribe - 7 days of onboarding",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
