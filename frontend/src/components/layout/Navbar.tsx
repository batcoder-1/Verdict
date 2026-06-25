import Logo from "../common/Logo";
import Button from "../common/Button";
import Container from "../common/Container";

function Navbar() {
  return (
    <nav className="border-b border-zinc-800 bg-zinc-950">
      <Container>
        <div className="flex h-16 items-center justify-between">
          <Logo />

          <div className="flex gap-3">
            <Button variant="secondary">
              GitHub
            </Button>

            <Button>
              Get Started
            </Button>
          </div>
        </div>
      </Container>
    </nav>
  );
}

export default Navbar;