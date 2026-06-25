import Card from "../common/Card";
import Container from "../common/Container";

const features = [
  {
    title: "LeetCode Analytics",
    description:
      "Track solved problems, contest ratings, rankings and coding streaks.",
  },
  {
    title: "Codeforces Analytics",
    description:
      "Monitor ratings, ranks, contests and submission activity.",
  },
  {
    title: "Contest History",
    description:
      "View all past contests with detailed performance statistics.",
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