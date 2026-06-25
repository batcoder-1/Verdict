import { Link } from "react-router-dom";

function Logo() {
  return (
    <Link
      to="/"
      className="text-2xl font-bold tracking-tight text-white"
    >
      Verdict
    </Link>
  );
}

export default Logo;