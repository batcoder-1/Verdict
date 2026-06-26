import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

import type { CodeforcesContest } from "../../types/codeforces";
import SectionCard from "../common/SectionCard";

interface Props {
  contests: CodeforcesContest[];
}

const CodeforcesRatingChart = ({ contests }: Props) => {
  const data = [...contests]
    .sort(
      (a, b) =>
        new Date(a.contest_date ?? "").getTime() -
        new Date(b.contest_date ?? "").getTime()
    )
    .map((contest) => ({
      contest: contest.contest_name,
      rating: contest.new_rating,
    }));

  return (
    <SectionCard title="Codeforces Rating Progress">
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis
              dataKey="contest"
              tick={false}
            />

            <YAxis />

           <Tooltip
  contentStyle={{
    backgroundColor: "#18181b",
    border: "1px solid #3f3f46",
    borderRadius: "12px",
  }}
/>

            <Line
              type="monotone"
              dataKey="rating"
              stroke="#f59e0b"
              strokeWidth={3}
              dot
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </SectionCard>
  );
};

export default CodeforcesRatingChart;