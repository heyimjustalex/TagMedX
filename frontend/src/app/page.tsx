import { Button } from "@nextui-org/button"

const Home = () => {
  return (
    <section className="w-full flex flex-center flex-col mt-20 items-center">
      <h1 className="head-text text-center">
        <span className="gradient-blue text-center">TagMedX</span>
      </h1>
      <p className="desc text-center mt-8 max-w-md">
        TagMedX is an open-source web app built with FastAPI,
        Next.js and MySQL, designed for medical image tagging.
      </p>
      <Button className="flex w-30 mt-4" color="primary" variant="ghost">Let's tag!</Button>
    </section>
  )
}

export default Home