export default function Badge({ variant = 'type', children }) {
  return <span className={`badge badge--${variant}`}>{children}</span>;
}
