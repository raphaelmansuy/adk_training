import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Customer Support Chat",
  description: "AI-powered customer support powered by Google ADK",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      {/* suppressHydrationWarning prevents React from logging mismatches for
          attributes injected by browser extensions or other client-only
          alterations (e.g. cz-shortcut-listen). This is safe because the
          body element content is entirely client-rendered wrapper content
          and we don't depend on those attributes for rendering logic. */}
      <body className={inter.className} suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
