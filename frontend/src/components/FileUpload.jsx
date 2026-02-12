import { useState } from "react";
import { uploadArchivo } from "../services/api";

export default function FileUpload({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [usuarioId, setUsuarioId] = useState(1);
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
      const { data } = await uploadArchivo(file, usuarioId);
      setMessage({
        type: "success",
        text: `Archivo en cola (ID: ${data.archivo_id}). Estado: ${data.estado}`,
      });
      setFile(null);
      if (onUploaded) onUploaded(data);
    } catch (err) {
      const detail = err.response?.data?.detail || err.message;
      setMessage({ type: "error", text: String(detail) });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section style={styles.section}>
      <h2 style={styles.h2}>Subir archivo de peajes</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="file"
          accept=".xml,.csv,.txt"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          style={styles.input}
        />
        <input
          type="number"
          placeholder="Usuario ID (por defecto: 1)"
          value={usuarioId}
          onChange={(e) => setUsuarioId(parseInt(e.target.value) || 1)}
          min="1"
          style={styles.input}
        />
        <button type="submit" disabled={loading} style={styles.button}>
          {loading ? "Subiendo…" : "Subir"}
        </button>
      </form>
      {message.text && (
        <p style={{ ...styles.message, color: message.type === "error" ? "#f87171" : "#4ade80" }}>
          {message.text}
        </p>
      )}
    </section>
  );
}

const styles = {
  section: { marginBottom: "2rem" },
  h2: { fontSize: "1.25rem", marginBottom: "0.75rem" },
  form: { display: "flex", flexDirection: "column", gap: "0.5rem", maxWidth: 400 },
  input: { padding: "0.5rem", borderRadius: 6, border: "1px solid #334155" },
  button: { padding: "0.5rem 1rem", background: "#3b82f6", color: "#fff", border: 0, borderRadius: 6, cursor: "pointer" },
  message: { marginTop: "0.5rem", fontSize: "0.9rem" },
};
