import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Research Paper Reviewer",
  description: "Automated AI-powered academic paper analysis with peer review, literature review, and novelty detection",
  keywords: ["AI", "research", "paper review", "academic", "novelty detection"],
  icons: {
    icon: "/favicon.png",
    shortcut: "/favicon.png",
    apple: "/favicon.png",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
        <footer className="w-full py-8 glass-card rounded-none border-x-0 border-b-0 text-center text-gray-400 text-sm mt-auto">
          <p>
            Developed by <a href="https://hazratali1.github.io/Hazrat-Ali/" target="_blank" rel="noopener noreferrer" className="text-purple-400 hover:text-purple-300 font-semibold transition-colors">Hazrat Ali</a>
          </p>
        </footer>
      </body>
    </html>
  );
}
