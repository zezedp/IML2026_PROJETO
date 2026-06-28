export default function SectionHeader({ title, description }) {
  return (
    <header className="section-header">
      <h1>{title}</h1>
      <p>{description}</p>
    </header>
  );
}
