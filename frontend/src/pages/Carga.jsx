import { useState } from "react";
import { uploadArchivo } from "../services/api";

export default function Carga() {
  const [file, setFile] = useState(null);
  const [usuario, setUsuario] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: "", text: "" });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage({ type: "error", text: "Selecciona un archivo" });
      return;
    }
    setLoading(true);
    setMessage({ type: "", text: "" });
    try {
      const { data } = await uploadArchivo(file, usuario || null);
      setMessage({
        type: "success",
        text: `Archivo en cola (ID: ${data.archivo_id}). Estado: ${data.estado}. Puedes ver el estado en Archivos.`,
      });
      setFile(null);
      e.target.reset();
    } catch (err) {
      const detail = err.response?.data?.detail || err.message;
      setMessage({ type: "error", text: String(detail) });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <header className="page-header">
        <h1 className="page-title">Subir archivo de peajes</h1>
        <p className="page-subtitle">
          CSV con cabecera: cups_cliente, instalacion_gen, tipo_autoconsumo, fechas y arrays de 6 valores
        </p>
      </header>

      <div className="card">
        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label className="form-label">Archivo (CSV / TXT)</label>
            <input
              type="file"
              accept=".csv,.txt"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
              className="form-input form-input--file"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Usuario (opcional)</label>
            <input
              type="text"
              placeholder="Ej. admin"
              value={usuario}
              onChange={(e) => setUsuario(e.target.value)}
              className="form-input"
            />
          </div>
          <button type="submit" disabled={loading} className="btn btn-primary">
            {loading ? "Subiendo…" : "Subir archivo"}
          </button>
        </form>
        {message.text && (
          <p
            className={
              message.type === "error"
                ? "form-message form-message--error"
                : "form-message form-message--success"
            }
          >
            {message.text}
          </p>
        )}
      </div>
    </div>
  );
}
