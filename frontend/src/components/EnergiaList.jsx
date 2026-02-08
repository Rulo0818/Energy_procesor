export default function EnergiaList({ registros, total }) {
  if (!registros?.length) {
    return (
      <p style={{ color: "#94a3b8" }}>No hay registros. Total: 0.</p>
    );
  }
  return (
    <div style={styles.wrapper}>
      <p style={styles.total}>Total: {total}</p>
      <ul style={styles.list}>
        {registros.map((r) => (
          <li key={r.id} style={styles.item}>
            <strong>{r.cups_cliente}</strong> — {r.instalacion_gen} | {r.fecha_desde} → {r.fecha_hasta} | tipo {r.tipo_autoconsumo}
          </li>
        ))}
      </ul>
    </div>
  );
}

const styles = {
  wrapper: { marginTop: "1rem" },
  total: { marginBottom: "0.5rem", color: "#94a3b8" },
  list: { listStyle: "none", padding: 0, margin: 0 },
  item: { padding: "0.5rem 0", borderBottom: "1px solid #334155", fontSize: "0.9rem" },
};
