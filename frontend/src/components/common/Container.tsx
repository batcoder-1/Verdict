type ContainerProps = {
  children: React.ReactNode;
};

function Container({ children }: ContainerProps) {
  return (
    <div className="mx-auto max-w-7xl px-6">
      {children}
    </div>
  );
}

export default Container;