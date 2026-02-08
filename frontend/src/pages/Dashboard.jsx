import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getStats, getArchivos } from "../services/api";

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

const estadoColor = (estado) => {
  switch (estado) {
    case "completado":
      return "var(--success)";
    case "error":
    case "pendiente":
      return "var(--warning)";
    case "procesando":
      return "var(--accent)";
    default:
      return "var(--text-secondary)";
  }
};

export default function Dashboard() {
  const [stats, setStats] = useState({
    total_archivos: 0,
    total_registros_energia: 0,
    total_errores: 0,
  });
  const [archivos, setArchivos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const [sRes, aRes] = await Promise.all([getStats(), getArchivos(10)]);
        if (!cancelled) {
          setStats(sRes.data);
          setArchivos(aRes.data || []);
        }
      } catch {
        if (!cancelled) {
          setStats({ total_archivos: 0, total_registros_energia: 0, total_errores: 0 });
          setArchivos([]);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    load();
    return () => { cancelled = true; };
  }, []);

  const cards = [
    {
      title: "Archivos procesados",
      value: stats.total_archivos,
      to: "/archivos",
      icon: "▤",
      color: "var(--accent)",
    },
    {
      title: "Registros de energía",
      value: stats.total_registros_energia,
      to: "/consulta",
      icon: "◇",
      color: "var(--success)",
    },
    {
      title: "Errores registrados",
      value: stats.total_errores,
      to: "/archivos",
      icon: "!",
      color: "var(--warning)",
    },
  ];

  return (
    <div className="page">
      <header className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">
          Resumen del sistema de procesamiento de peajes
        </p>
      </header>

      {loading ? (
        <div className="dashboard-loading">Cargando…</div>
      ) : (
        <>
          <section className="dashboard-cards">
            {cards.map((card) => (
              <Link
                key={card.title}
                to={card.to}
                className="dashboard-card"
                style={{ "--card-accent": card.color }}
              >
                <span className="dashboard-card-icon">{card.icon}</span>
                <div className="dashboard-card-body">
                  <span className="dashboard-card-value">{card.value}</span>
                  <span className="dashboard-card-title">{card.title}</span>
                </div>
              </Link>
            ))}
          </section>

          <section className="dashboard-section">
            <div className="dashboard-section-header">
              <h2 className="dashboard-section-title">Archivos recientes</h2>
              <Link to="/archivos" className="dashboard-section-link">
                Ver todos →
              </Link>
            </div>
            {archivos.length === 0 ? (
              <p className="dashboard-empty">
                Aún no hay archivos. <Link to="/carga">Sube el primero</Link>.
              </p>
            ) : (
              <div className="table-wrap">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Nombre</th>
                      <th>Estado</th>
                      <th>Registros</th>
                      <th>Errores</th>
                      <th>Fecha</th>
                    </tr>
                  </thead>
                  <tbody>
                    {archivos.map((a) => (
                      <tr key={a.id}>
                        <td>
                          <Link to={`/archivos/${a.id}`} className="table-link">
                            {a.nombre_archivo}
                          </Link>
                        </td>
                        <td>
                          <span
                            className="table-badge"
                            style={{ background: estadoColor(a.estado) }}
                          >
                            {a.estado}
                          </span>
                        </td>
                        <td>{a.registros_exitosos ?? 0}</td>
                        <td>{a.registros_con_error ?? 0}</td>
                        <td className="text-muted">{formatDate(a.fecha_carga)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>

          <section className="dashboard-actions">
            <h2 className="dashboard-section-title">Acciones rápidas</h2>
            <div className="dashboard-actions-grid">
              <Link to="/carga" className="action-card">
                <span className="action-card-icon">↑</span>
                <span>Subir archivo de peajes</span>
              </Link>
              <Link to="/consulta" className="action-card">
                <span className="action-card-icon">◇</span>
                <span>Consultar por CUPS</span>
              </Link>
            </div>
          </section>
        </>
      )}
    </div>
  );
}
