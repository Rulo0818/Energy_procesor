import { useState, useEffect } from "react";
import { getUsuarios } from "../services/api";

const formatDate = (dateStr) => {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  return d.toLocaleDateString("es-ES", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const rolColor = (rol) => {
  switch (rol) {
    case "admin":
      return "#ef4444";
    case "operador":
      return "#3b82f6";
    case "consultor":
      return "#10b981";
    default:
      return "var(--text-secondary)";
  }
};

export default function Usuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filtroActivo, setFiltroActivo] = useState(null);

  useEffect(() => {
    loadUsuarios();
  }, [filtroActivo]);

  const loadUsuarios = async () => {
    try {
      setLoading(true);
      const params = {};
      if (filtroActivo !== null) {
        params.activo = filtroActivo;
      }
      const response = await getUsuarios(params);
      setUsuarios(response.data || []);
    } catch (error) {
      console.error("Error loading usuarios:", error);
      setUsuarios([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <header className="page-header">
        <h1 className="page-title">Usuarios</h1>
        <p className="page-subtitle">
          Gestión de usuarios del sistema
        </p>
      </header>

      <div className="filters-bar">
        <button
          className={`filter-btn ${filtroActivo === null ? "active" : ""}`}
          onClick={() => setFiltroActivo(null)}
        >
          Todos
        </button>
        <button
          className={`filter-btn ${filtroActivo === true ? "active" : ""}`}
          onClick={() => setFiltroActivo(true)}
        >
          Activos
        </button>
        <button
          className={`filter-btn ${filtroActivo === false ? "active" : ""}`}
          onClick={() => setFiltroActivo(false)}
        >
          Inactivos
        </button>
      </div>

      {loading ? (
        <div className="dashboard-loading">Cargando usuarios…</div>
      ) : usuarios.length === 0 ? (
        <p className="dashboard-empty">No hay usuarios registrados.</p>
      ) : (
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Nombre Completo</th>
                <th>Email</th>
                <th>Rol</th>
                <th>Estado</th>
                <th>Fecha Registro</th>
                <th>Última Sesión</th>
              </tr>
            </thead>
            <tbody>
              {usuarios.map((usuario) => (
                <tr key={usuario.id}>
                  <td>{usuario.id}</td>
                  <td>
                    <strong>{usuario.username}</strong>
                  </td>
                  <td>{usuario.nombre_completo}</td>
                  <td className="text-muted">{usuario.email}</td>
                  <td>
                    <span
                      className="table-badge"
                      style={{ background: rolColor(usuario.rol) }}
                    >
                      {usuario.rol}
                    </span>
                  </td>
                  <td>
                    <span
                      className="table-badge"
                      style={{
                        background: usuario.activo
                          ? "var(--success)"
                          : "var(--text-secondary)",
                      }}
                    >
                      {usuario.activo ? "Activo" : "Inactivo"}
                    </span>
                  </td>
                  <td className="text-muted">{formatDate(usuario.fecha_registro)}</td>
                  <td className="text-muted">{formatDate(usuario.ultima_sesion)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
