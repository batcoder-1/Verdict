import type { ReactNode } from "react";

interface SectionCardProps {
  title: string;
  children: ReactNode;
  action?: ReactNode;
}

const SectionCard = ({
  title,
  children,
  action,
}: SectionCardProps) => {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6 shadow-sm">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-xl font-semibold">{title}</h2>

        {action}
      </div>

      {children}
    </div>
  );
};

export default SectionCard;