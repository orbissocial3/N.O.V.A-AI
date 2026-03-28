/**
 * api.js
 * ----------------------------
 * Cliente HTTP para N.O.V.A.
 * - Usa axios para conectar con el backend FastAPI
 * - Añade token en cada request
 * - Maneja errores globales y desconexión
 */

import axios from "axios";
import auth from "./auth";

// URL base del backend (usa variable de entorno si existe, si no tu IP local)
const API_BASE_URL =
  process.env.EXPO_PUBLIC_API_URL || "http://192.168.56.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: process.env.EXPO_PUBLIC_API_TIMEOUT || 10000, // configurable
});

// Interceptor para añadir token
api.interceptors.request.use(
  async (config) => {
    const token = await auth.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para manejar errores globales
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const { status, data } = error.response;
      console.log(`[API Error] ${status}:`, data);

      if (status === 401) {
        // Token inválido → cerrar sesión
        auth.logout();
      }
    } else {
      console.log("[Network Error]:", error.message);
    }
    return Promise.reject(error);
  }
);

export default api;
