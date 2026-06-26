import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import type { LeetCodeContest } from "../../types/leetcode";
import SectionCard from "../common/SectionCard";

interface Props {
  contests: LeetCodeContest[];
}

const LeetCodeRatingChart = ({ contests }: Props) => {
  const data = contests.map((contest, index) => ({
  contest: index + 1,
  rating: contest.rating,
}));

  return (
    <SectionCard title="LeetCode Rating Progress">
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
              stroke="#3b82f6"
              strokeWidth={3}
              dot
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </SectionCard>
  );
};

export default LeetCodeRatingChart;