import { Link, NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Layout.css";

const navItems = [
  { to: "/", label: "Dashboard", icon: "◉" },
  { to: "/carga", label: "Subir archivo", icon: "↑" },
  { to: "/consulta", label: "Consulta energía", icon: "◇" },
  { to: "/archivos", label: "Archivos y errores", icon: "▤" },
  { to: "/usuarios", label: "Usuarios", icon: "" },
  { to: "/clientes", label: "Clientes", icon: "" },
];

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="layout">
      <aside className="sidebar">
        <Link to="/" className="sidebar-brand">
          <span className="sidebar-brand-icon">⚡</span>
          <span className="sidebar-brand-text">Energy Process</span>
        </Link>
        <nav className="sidebar-nav">
          {navItems.map(({ to, label, icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                "sidebar-link" + (isActive ? " sidebar-link--active" : "")
              }
              end={to === "/"}
            >
              <span className="sidebar-link-icon">{icon}</span>
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          <a
            href={`${import.meta.env.VITE_API_URL || "http://localhost:8000"}/docs`}
            target="_blank"
            rel="noopener noreferrer"
            className="sidebar-link"
          >
            <span className="sidebar-link-icon">⎘</span>
            <span>Docs</span>
          </a>
          {user && (
            <div className="sidebar-user">
              <div className="user-info">
                <div className="user-name">{user.nombre}</div>
                <div className="user-email">{user.email}</div>
              </div>
              <button onClick={handleLogout} className="btn-logout" title="Cerrar sesión">
                logout
              </button>
            </div>
          )}
        </div>
      </aside>
      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}
