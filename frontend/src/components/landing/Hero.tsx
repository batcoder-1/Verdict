import Button from "../common/Button";
import Container from "../common/Container";

function Hero() {
  return (
    <section className="py-32">
      <Container>
        <div className="mx-auto max-w-4xl text-center">

          <span className="rounded-full border border-zinc-800 px-4 py-2 text-sm text-zinc-400">
            Now tracking LeetCode + Codeforces
          </span>

          <h1 className="mt-8 text-6xl font-bold tracking-tight">
            Analyze Your Competitive Programming Journey
          </h1>

          <p className="mx-auto mt-6 max-w-2xl text-xl text-zinc-400">
            Track LeetCode and Codeforces performance in one unified dashboard.
          </p>

          <div className="mt-10 flex justify-center gap-4">
            <Button>Get Started</Button>
            <Button variant="secondary">
              GitHub Repository
            </Button>
          </div>

        </div>
      </Container>
    </section>
  );
}

export default Hero;