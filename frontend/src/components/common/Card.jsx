export default function Card({ title, icon, children, className = '', actions = null }) {
  return (
    <section className={`card ${className}`}>
      {(title || actions) && (
        <div className="card__header">
          {title && (
            <h3 className="card__title">
              {icon && <span aria-hidden="true">{icon}</span>}
              {title}
            </h3>
          )}
          {actions}
        </div>
      )}
      {children}
    </section>
  );
}
