import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { getArchivos, getArchivoStatus, getErroresArchivo } from "../services/api";

const formatDate = (dateStr) => {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleDateString("es-ES", {
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

export default function Archivos() {
  const { id } = useParams();
  const [archivos, setArchivos] = useState([]);
  const [detalle, setDetalle] = useState(null);
  const [errores, setErrores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadingDetalle, setLoadingDetalle] = useState(false);

  useEffect(() => {
    let cancelled = false;
    getArchivos(50)
      .then((res) => {
        if (!cancelled) setArchivos(res.data || []);
      })
      .catch(() => {
        if (!cancelled) setArchivos([]);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, []);

  useEffect(() => {
    if (!id) {
      setDetalle(null);
      setErrores([]);
      return;
    }
    setLoadingDetalle(true);
    Promise.all([
      getArchivoStatus(id),
      getErroresArchivo(id),
    ])
      .then(([aRes, eRes]) => {
        setDetalle(aRes.data);
        setErrores(eRes.data || []);
      })
      .catch(() => {
        setDetalle(null);
        setErrores([]);
      })
      .finally(() => setLoadingDetalle(false));
  }, [id]);

  if (id) {
    return (
      <div className="page">
        <header className="page-header">
          <Link to="/archivos" className="back-link">← Volver a archivos</Link>
          <h1 className="page-title">
            {loadingDetalle ? "Cargando…" : detalle?.nombre_archivo || `Archivo #${id}`}
          </h1>
          {detalle && (
            <p className="page-subtitle">
              Estado: <span style={{ color: estadoColor(detalle.estado) }}>{detalle.estado}</span>
              {" · "}
              {detalle.registros_exitosos ?? 0} registros · {detalle.registros_con_error ?? 0} errores
              {" · "}
              {formatDate(detalle.fecha_carga)}
            </p>
          )}
        </header>

        <div className="card">
          <h2 className="card-title">Errores en este archivo</h2>
          {loadingDetalle ? (
            <p className="text-muted">Cargando…</p>
          ) : errores.length === 0 ? (
            <p className="empty-state">Sin errores para este archivo.</p>
          ) : (
            <div className="table-wrap">
              <table className="table">
                <thead>
                  <tr>
                    <th>Línea</th>
                    <th>Tipo</th>
                    <th>Descripción</th>
                  </tr>
                </thead>
                <tbody>
                  {errores.map((e) => (
                    <tr key={e.id}>
                      <td>{e.linea_archivo}</td>
                      <td>
                        <span className="table-badge" style={{ background: "var(--warning)" }}>
                          {e.tipo_error}
                        </span>
                      </td>
                      <td>{e.descripcion}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <header className="page-header">
        <h1 className="page-title">Archivos y errores</h1>
        <p className="page-subtitle">
          Listado de archivos procesados. Haz clic en uno para ver sus errores.
        </p>
      </header>

      <div className="card">
        {loading ? (
          <p className="text-muted">Cargando…</p>
        ) : archivos.length === 0 ? (
          <p className="empty-state">
            Aún no hay archivos. <Link to="/carga">Sube uno</Link>.
          </p>
        ) : (
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>Estado</th>
                  <th>Registros OK</th>
                  <th>Errores</th>
                  <th>Fecha</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {archivos.map((a) => (
                  <tr key={a.id}>
                    <td>{a.nombre_archivo}</td>
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
                    <td>
                      <Link to={`/archivos/${a.id}`} className="btn btn-sm">
                        Ver errores
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
