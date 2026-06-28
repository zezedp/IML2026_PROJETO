import Header from './Header';
import NavBar from './NavBar';

export default function MainLayout({ activeScreen, onNavigate, children }) {
  return (
    <>
      <div className="shell">
        <Header />
        <NavBar activeScreen={activeScreen} onNavigate={onNavigate} />
        <main>{children}</main>
      </div>
    </>
  );
}
