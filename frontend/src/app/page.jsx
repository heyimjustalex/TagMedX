"use client"

import { Button } from "@nextui-org/button"
import { useContext } from "react";
import NotificationContext from "../contexts/NotificationContext";
import NextColor from "../consts/NextColor"

export default function HomePage() {
  const notification = useContext(NotificationContext);
  return (
    <section className="page flex-col">
      <h1 className="head-text text-center">
        <span className="gradient-blue text-center">TagMedX</span>
      </h1>
      <p className="desc text-center mt-6 max-w-md">
        TagMedX is an open-source web app built with FastAPI,
        Next.js and MySQL, designed for medical image tagging.
      </p>
      <Button className="flex w-30 mt-4" color="primary" variant="ghost" onClick={() => notification.make(NextColor.Primary, "Information", "Textjsndi asndi uasdi ansdi nasiud ")}>Let's tag!</Button>
    </section>
  )
}