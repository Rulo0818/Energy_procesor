import { useState, useEffect } from "react";
import { getClientes } from "../services/api";

const formatDate = (dateStr) => {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  return d.toLocaleDateString("es-ES", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
};

export default function Clientes() {
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filtroActivo, setFiltroActivo] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    loadClientes();
  }, [filtroActivo]);

  const loadClientes = async () => {
    try {
      setLoading(true);
      const params = {};
      if (filtroActivo !== null) {
        params.activo = filtroActivo;
      }
      const response = await getClientes(params);
      setClientes(response.data || []);
    } catch (error) {
      console.error("Error loading clientes:", error);
      setClientes([]);
    } finally {
      setLoading(false);
    }
  };

  const filteredClientes = clientes.filter((cliente) => {
    if (!searchTerm) return true;
    const search = searchTerm.toLowerCase();
    return (
      cliente.nombre_cliente.toLowerCase().includes(search) ||
      cliente.cups.toLowerCase().includes(search) ||
      (cliente.municipio && cliente.municipio.toLowerCase().includes(search)) ||
      (cliente.provincia && cliente.provincia.toLowerCase().includes(search))
    );
  });

  return (
    <div className="page">
      <header className="page-header">
        <h1 className="page-title">Clientes</h1>
        <p className="page-subtitle">
          Gestión de clientes y puntos de suministro (CUPS)
        </p>
      </header>

      <div className="filters-bar">
        <input
          type="text"
          placeholder="Buscar por nombre, CUPS, municipio o provincia..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
          style={{
            padding: "8px 12px",
            borderRadius: "6px",
            border: "1px solid var(--border)",
            background: "var(--bg-secondary)",
            color: "var(--text)",
            marginRight: "12px",
            minWidth: "300px",
          }}
        />
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
        <div className="dashboard-loading">Cargando clientes…</div>
      ) : filteredClientes.length === 0 ? (
        <p className="dashboard-empty">
          {searchTerm
            ? "No se encontraron clientes con ese criterio de búsqueda."
            : "No hay clientes registrados."}
        </p>
      ) : (
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>CUPS</th>
                <th>Nombre Cliente</th>
                <th>Email</th>
                <th>Teléfono</th>
                <th>Municipio</th>
                <th>Provincia</th>
                <th>CP</th>
                <th>Estado</th>
                <th>Fecha Registro</th>
              </tr>
            </thead>
            <tbody>
              {filteredClientes.map((cliente) => (
                <tr key={cliente.id}>
                  <td>{cliente.id}</td>
                  <td>
                    <code style={{ fontSize: "0.85em" }}>{cliente.cups}</code>
                  </td>
                  <td>
                    <strong>{cliente.nombre_cliente}</strong>
                  </td>
                  <td className="text-muted">{cliente.email || "—"}</td>
                  <td className="text-muted">{cliente.telefono || "—"}</td>
                  <td>{cliente.municipio || "—"}</td>
                  <td>{cliente.provincia || "—"}</td>
                  <td>{cliente.codigo_postal || "—"}</td>
                  <td>
                    <span
                      className="table-badge"
                      style={{
                        background: cliente.activo
                          ? "var(--success)"
                          : "var(--text-secondary)",
                      }}
                    >
                      {cliente.activo ? "Activo" : "Inactivo"}
                    </span>
                  </td>
                  <td className="text-muted">{formatDate(cliente.fecha_registro)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div style={{ marginTop: "20px", color: "var(--text-secondary)", fontSize: "0.9em" }}>
        Mostrando {filteredClientes.length} de {clientes.length} clientes
      </div>
    </div>
  );
}
