import "./index.scss";

interface LoaderProps {
  size?: "small" | "medium" | "large";
}
const Loader = ({ size = "small" }: LoaderProps) => {
  return <div className={`loader ${size}`} />;
};

export default Loader;
