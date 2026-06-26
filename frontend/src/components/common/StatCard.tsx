import type { ReactNode } from "react";

interface StatCardProps {
  title: string;
  value: string | number;
  icon?: ReactNode;
  subtitle?: string;
}

const StatCard = ({
  title,
  value,
  icon,
  subtitle,
}: StatCardProps) => {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4 transition hover:border-zinc-700">
      <div className="mb-2 flex items-center gap-2 text-zinc-400">
        {icon}
        <span className="text-sm">{title}</span>
      </div>

      <div className="text-3xl font-bold">
        {value}
      </div>

      {subtitle && (
        <p className="mt-1 text-sm text-zinc-500">
          {subtitle}
        </p>
      )}
    </div>
  );
};

export default StatCard;