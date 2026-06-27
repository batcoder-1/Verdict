import { Link } from "react-router-dom";
import { ArrowRight, LineChart, Trophy, Flame } from "lucide-react";
import { FaGithub } from "react-icons/fa";

import Button from "../common/Button";
import Card from "../common/Card";
import Container from "../common/Container";
import StatCard from "../common/StatCard";

function Hero() {
  return (
    <Container>
      <section className="py-20">
        <div className="mx-auto max-w-4xl text-center">
          <div className="mb-6 inline-flex rounded-full border border-zinc-700 px-4 py-2 text-sm text-zinc-400">
            Open Source • FastAPI • React
          </div>

          <h1 className="text-6xl font-bold leading-tight">
            Track Your
            <span className="text-blue-500"> Competitive Programming</span>
            <br />
            Journey
          </h1>

          <p className="mx-auto mt-6 max-w-2xl text-lg text-zinc-400">
            Connect your LeetCode and Codeforces accounts to analyze ratings,
            contest history, coding streaks and visualize your progress through
            one unified dashboard.
          </p>

          <div className="mt-10 flex justify-center gap-4">
            <Link to="/login">
              <Button>
                Get Started
                <ArrowRight size={18} />
              </Button>
            </Link>

            <a
              href="https://github.com/batcoder-1/Verdict"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Button variant="outline">
                <FaGithub size={18} />
                GitHub
              </Button>
            </a>
          </div>
        </div>

        <Card className="mx-auto mt-20 max-w-6xl">
          {/* Product Highlights */}
          <div className="grid gap-4 md:grid-cols-4">
            <StatCard
              title="Platforms Supported"
              value="2"
            />

            <StatCard
              title="Contest Tracking"
              value="✓"
            />

            <StatCard
              title="Rating Charts"
              value="Live"
            />

            <StatCard
              title="One-click Sync"
              value="Instant"
            />
          </div>

          {/* Dashboard Preview */}
          <div className="mt-8 rounded-xl border border-zinc-800 bg-zinc-950 p-6">
            <div className="mb-6 flex items-center justify-between">
              <h3 className="text-lg font-semibold">
                Dashboard Preview
              </h3>

              <span className="rounded-full bg-green-500/10 px-3 py-1 text-sm text-green-400">
                Live Analytics
              </span>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <Card>
                <div className="mb-4 flex items-center gap-2">
                  <Trophy className="text-yellow-400" size={20} />
                  <h4 className="font-semibold">LeetCode</h4>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <StatCard title="Solved" value="395" />
                  <StatCard title="Rating" value="1721" />
                  <StatCard title="Contests" value="8" />
                  <StatCard title="Streak" value="15" />
                </div>
              </Card>

              <Card>
                <div className="mb-4 flex items-center gap-2">
                  <LineChart className="text-blue-400" size={20} />
                  <h4 className="font-semibold">Codeforces</h4>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <StatCard title="Rating" value="1176" />
                  <StatCard title="Max" value="1218" />
                  <StatCard title="Rank" value="Pupil" />
                  <StatCard title="Streak" value="1" />
                </div>
              </Card>
            </div>

            <div className="mt-6 flex items-center justify-center rounded-lg border border-dashed border-zinc-700 py-8 text-zinc-500">
              <Flame className="mr-2" size={18} />
              Interactive rating charts & contest history
            </div>
          </div>
        </Card>
      </section>
    </Container>
  );
}

export default Hero;