type ButtonProps = {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: "primary" | "secondary";
  type?: "button" | "submit";
};

function Button({
  children,
  onClick,
  variant = "primary",
  type = "button",
}: ButtonProps) {
  const base =
    "px-5 py-2 rounded-lg font-medium transition duration-200";

  const styles =
    variant === "primary"
      ? "bg-blue-600 hover:bg-blue-700 text-white"
      : "border border-zinc-700 text-zinc-200 hover:bg-zinc-800";

  return (
    <button
      type={type}
      onClick={onClick}
      className={`${base} ${styles}`}
    >
      {children}
    </button>
  );
}

export default Button;