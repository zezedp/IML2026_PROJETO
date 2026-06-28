import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

export default function ChartShell({ children, className = 'chart-box', label = 'grafico' }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [actionsHost, setActionsHost] = useState(null);
  const shellRef = useRef(null);

  useEffect(() => {
    const cardHeader = shellRef.current?.closest('.card')?.querySelector('.card__header');
    if (!cardHeader) return undefined;

    const host = document.createElement('div');
    host.className = 'card__chart-actions';
    cardHeader.appendChild(host);
    setActionsHost(host);

    return () => {
      host.remove();
      setActionsHost(null);
    };
  }, []);

  useEffect(() => {
    if (!isExpanded) return undefined;

    const handleKeyDown = (event) => {
      if (event.key === 'Escape') setIsExpanded(false);
    };

    document.body.classList.add('has-chart-modal');
    window.addEventListener('keydown', handleKeyDown);

    return () => {
      document.body.classList.remove('has-chart-modal');
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isExpanded]);

  const expandButton = (
    <button
      type="button"
      className="chart-expand"
      aria-label={`Expandir ${label}`}
      title={`Expandir ${label}`}
      onClick={() => setIsExpanded(true)}
    >
      <span aria-hidden="true" />
    </button>
  );

  return (
    <>
      <div ref={shellRef} className={`chart-shell ${className}`}>
        {!actionsHost && expandButton}
        {children}
      </div>
      {actionsHost && createPortal(expandButton, actionsHost)}
      {isExpanded &&
        createPortal(
          <div className="chart-modal" role="dialog" aria-modal="true" aria-label={`Visualizacao ampliada de ${label}`}>
            <button type="button" className="chart-modal__backdrop" aria-label="Fechar zoom" onClick={() => setIsExpanded(false)} />
            <div className="chart-modal__panel">
              <button type="button" className="chart-modal__close" aria-label="Fechar zoom" onClick={() => setIsExpanded(false)}>
                X
              </button>
              <div className={`chart-shell chart-shell--expanded ${className}`}>{children}</div>
            </div>
          </div>,
          document.body,
        )}
    </>
  );
}
