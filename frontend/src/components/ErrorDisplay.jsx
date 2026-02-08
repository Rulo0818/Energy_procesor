export default function ErrorDisplay({ errores }) {
  if (!errores?.length) {
    return <p style={{ color: "#94a3b8" }}>Sin errores para este archivo.</p>;
  }
  return (
    <ul style={styles.list}>
      {errores.map((e) => (
        <li key={e.id} style={styles.item}>
          <span style={styles.badge}>{e.tipo_error}</span> Línea {e.linea_archivo}: {e.descripcion}
        </li>
      ))}
    </ul>
  );
}

const styles = {
  list: { listStyle: "none", padding: 0, margin: 0 },
  item: { padding: "0.5rem 0", borderBottom: "1px solid #334155", fontSize: "0.9rem" },
  badge: { background: "#7f1d1d", color: "#fecaca", padding: "0.15rem 0.4rem", borderRadius: 4, marginRight: "0.5rem", fontSize: "0.75rem" },
};
