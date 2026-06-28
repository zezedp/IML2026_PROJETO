export default function InsightBox({ variant = 'primary', children }) {
  return <div className={`insight insight--${variant}`}>{children}</div>;
}
