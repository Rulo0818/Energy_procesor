import { Link } from "react-router-dom";
import FileUpload from "../components/FileUpload";

export default function Home() {
  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <h1 style={styles.title}>Energy Process — Peajes</h1>
        <nav style={styles.nav}>
          <Link to="/" style={styles.link}>Inicio</Link>
          <Link to="/consulta" style={styles.link}>Consulta energía</Link>
        </nav>
      </header>
      <main style={styles.main}>
        <FileUpload />
      </main>
    </div>
  );
}

const styles = {
  page: { padding: "1.5rem", maxWidth: 800, margin: "0 auto" },
  header: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "2rem", flexWrap: "wrap", gap: "1rem" },
  title: { fontSize: "1.5rem", margin: 0 },
  nav: { display: "flex", gap: "1rem" },
  link: { color: "#60a5fa", textDecoration: "none" },
  main: {},
};
