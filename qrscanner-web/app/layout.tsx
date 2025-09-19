"use client";
import "./globals.css";
import { useEffect } from "react";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      const { innerWidth, innerHeight } = window;
      const x = (e.clientX / innerWidth - 0.5) * 40; // -20px..+20px
      const y = (e.clientY / innerHeight - 0.5) * 40;
      document.querySelectorAll<HTMLElement>(".sphere").forEach((el, i) => {
        el.style.transform = `translate(${x * (i + 1)}px, ${y * (i + 1)}px)`;
      });
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <html lang="en">
      <body className="relative min-h-screen bg-gray-900 text-white overflow-hidden">
        <div className="absolute inset-0 -z-10 overflow-hidden">
          <div className="sphere sphere-1" />
          <div className="sphere sphere-2" />
          <div className="sphere sphere-3" />
        </div>
        {children}
      </body>
    </html>
  );
}
