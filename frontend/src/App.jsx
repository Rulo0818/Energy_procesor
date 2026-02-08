import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Carga from "./pages/Carga";
import Consulta from "./pages/Consulta";
import Archivos from "./pages/Archivos";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/carga" element={<Carga />} />
          <Route path="/consulta" element={<Consulta />} />
          <Route path="/archivos" element={<Archivos />} />
          <Route path="/archivos/:id" element={<Archivos />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
