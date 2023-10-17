import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";

import Providers from "./providers";
import Nav from "@/components/Nav/Nav";

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "TagMedX",
  description: "TagMedX is an open-source web app built with FastAPI, Next.js, and MySQL, designed for medical image tagging."
}

const RootLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <html lang="en" className="light">
      <body className={inter.className}>
        <Providers>
          <div className="background">
            <div className="gradient" />
          </div>
          <main className="main">
            <Nav />
            {children}
          </main>
        </Providers>
      </body>
    </html>
  )
}

export default RootLayout