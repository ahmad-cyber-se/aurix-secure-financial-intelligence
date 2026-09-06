import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AURIX Secure Financial Intelligence Prototype",
  description: "24-hour technical evaluation prototype",
};

export default function RootLayout({children}: Readonly<{children: React.ReactNode}>) {
  return <html lang="en"><body>{children}</body></html>;
}
