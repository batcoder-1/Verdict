import { Link } from "react-router-dom";
import Button from "../common/Button";
import Container from "../common/Container";

function Hero() {
  return (
    <Container>
      <section className="flex min-h-[75vh] flex-col items-center justify-center text-center">
        <h1 className="mb-6 text-6xl font-bold">
          Track Your
          <span className="text-blue-500"> Competitive Programming</span>
          <br />
          Journey
        </h1>

        <p className="mb-8 max-w-2xl text-lg text-zinc-400">
          Sync your LeetCode and Codeforces profiles, analyze your progress,
          monitor contests, and visualize your competitive programming journey.
        </p>

        <Link to="/login">
          <Button>Get Started</Button>
        </Link>
      </section>
    </Container>
  );
}

export default Hero;