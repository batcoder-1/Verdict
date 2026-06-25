import Card from "../common/Card";
import Container from "../common/Container";

const features = [
  {
    title: "Unified Analytics",
    description:
      "Track LeetCode and Codeforces statistics from a single dashboard.",
  },
  {
    title: "Contest History",
    description:
      "Browse contest performance, rating changes, and rankings over time.",
  },
  {
    title: "One-Click Sync",
    description:
      "Synchronize your latest profile and contest data whenever you want.",
  },
  {
    title: "Daily Streaks",
    description:
      "Monitor current and longest coding streaks across supported platforms.",
  },
  {
    title: "Performance Insights",
    description:
      "Visualize solved problems, ratings, and progress with intuitive charts.",
  },
  {
    title: "Secure Authentication",
    description:
      "JWT-based authentication keeps your account secure while accessing your analytics.",
  },
];

function Features() {
  return (
    <section className="py-24">
      <Container>
        <div className="text-center">

          <p className="text-blue-500 text-sm font-semibold uppercase tracking-wider">
            Features
          </p>

          <h2 className="mt-4 text-4xl font-bold">
            Everything you need to track your progress
          </h2>

          <p className="mt-4 text-zinc-400">
            Designed for competitive programmers who want all their statistics
            in one place.
          </p>
        </div>

        <div className="mt-14 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {features.map((feature) => (
            <Card key={feature.title}>
              <h3 className="text-xl font-semibold">
                {feature.title}
              </h3>

              <p className="mt-3 text-zinc-400">
                {feature.description}
              </p>
            </Card>
          ))}
        </div>
      </Container>
    </section>
  );
}

export default Features;