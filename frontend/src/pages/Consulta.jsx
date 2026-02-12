import { useState, useEffect } from "react";
import { getEnergia } from "../services/api";

export default function Consulta() {
  const [cups, setCups] = useState("");
  const [data, setData] = useState({ total: 0, registros: [] });
  const [loading, setLoading] = useState(false);

  const buscar = async () => {
    setLoading(true);
    try {
      const { data: res } = await getEnergia(cups ? { cups } : {});
      setData({ total: res.total, registros: res.registros || [] });
    } catch {
      setData({ total: 0, registros: [] });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    buscar();
  }, []);

  return (
    <div className="page">
      <header className="page-header">
        <h1 className="page-title">Consulta energía</h1>
        <p className="page-subtitle">
          Registros de energía excedentaria. Filtra por CUPS o revisa todos.
        </p>
      </header>

      <div className="card card--filter">
        <div className="form form--inline">
          <div className="form-group form-group--flex">
            <input
              type="text"
              placeholder="CUPS "
              value={cups}
              onChange={(e) => setCups(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && buscar()}
              className="form-input"
            />
            <button
              type="button"
              onClick={buscar}
              disabled={loading}
              className="btn btn-primary"
            >
              {loading ? "Cargando…" : "Buscar"}
            </button>
          </div>
        </div>
      </div>

      <div className="card">
        {data.registros.length === 0 ? (
          <p className="empty-state">
            No hay registros. Total: <strong>0</strong>.
          </p>
        ) : (
          <>
            <p className="card-count">Total: {data.total} registros</p>
            <div className="table-wrap">
              <table className="table">
                <thead>
                  <tr>
                    <th>CUPS</th>
                    <th>Instalación</th>
                    <th>Periodo</th>
                    <th>Tipo</th>
                    <th>Energía neta (P1–P6)</th>
                  </tr>
                </thead>
                <tbody>
                  {data.registros.map((r) => (
                    <tr key={r.id}>
                      <td>
                        <strong>{r.cups_cliente}</strong>
                      </td>
                      <td>{r.instalacion_gen}</td>
                      <td>
                        {r.fecha_desde} → {r.fecha_hasta}
                      </td>
                      <td>{r.tipo_autoconsumo}</td>
                      <td className="text-muted">
                        {Array.isArray(r.energia_neta_gen)
                          ? r.energia_neta_gen.join(", ")
                          : "—"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
