import Card from "../common/Card";
import Container from "../common/Container";

const features = [
  {
    title: "LeetCode Analytics",
    description: "Track solved problems, rankings, streaks and contest ratings.",
  },
  {
    title: "Codeforces Analytics",
    description: "Monitor rating progression and contest performance.",
  },
  {
    title: "Contest History",
    description: "Browse your complete contest history with detailed statistics.",
  },
  {
    title: "Rating Charts",
    description: "Visualize your rating progression over time.",
  },
  {
    title: "One-click Sync",
    description: "Refresh your profiles instantly from both platforms.",
  },
  {
    title: "Secure Authentication",
    description: "JWT-based authentication with protected routes.",
  },
];

function Features() {
  return (
    <Container>
      <section className="grid gap-6 py-16 md:grid-cols-3">
        {features.map((feature) => (
          <Card key={feature.title}>
            <h3 className="mb-3 text-xl font-semibold">
              {feature.title}
            </h3>

            <p className="text-zinc-400">
              {feature.description}
            </p>
          </Card>
        ))}
      </section>
    </Container>
  );
}

export default Features;