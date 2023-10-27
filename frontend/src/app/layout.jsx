import "./globals.css";
import { Inter } from "next/font/google";

import Providers from "./providers";
import Nav from "../components/Nav/Nav";

const inter = Inter({ subsets: ["latin"] })

export const metadata = {
  title: "TagMedX",
  description: "TagMedX is an open-source web app built with FastAPI, Next.js, and MySQL, designed for medical image tagging."
}

export default function RootLayout({ children }) {
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