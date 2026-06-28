import { SCREENS } from '../../utils/constants';

export default function NavBar({ activeScreen, onNavigate }) {
  return (
    <nav className="nav-tabs" aria-label="Navegação principal">
      {SCREENS.map((screen) => (
        <button
          key={screen.id}
          type="button"
          className={screen.id === activeScreen ? 'is-active' : ''}
          onClick={() => onNavigate(screen.id)}
        >
          <span>{screen.number}</span>
          {screen.label}
        </button>
      ))}
    </nav>
  );
}
