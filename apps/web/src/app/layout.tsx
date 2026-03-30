import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HexStrike — AI Pentesting Platform",
  description: "AI-powered autonomous penetration testing",
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
