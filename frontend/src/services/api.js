import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL,
  headers: { "Content-Type": "application/json" },
});

export const uploadArchivo = (file, usuarioCarga = null) => {
  const form = new FormData();
  form.append("file", file);
  if (usuarioCarga) form.append("usuario_carga", usuarioCarga);
  return api.post("/api/v1/archivos/upload", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const getArchivoStatus = (archivoId) =>
  api.get(`/api/v1/archivos/${archivoId}`);

export const getEnergia = (params = {}) =>
  api.get("/api/v1/energia", { params });

export const getErroresArchivo = (archivoId) =>
  api.get(`/api/v1/errores/${archivoId}`);

export const getArchivos = (limit = 20) =>
  api.get("/api/v1/archivos", { params: { limit } });

export const getStats = () => api.get("/api/v1/stats");
