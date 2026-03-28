/**
 * auth.js
 * ----------------------------
 * Servicio de autenticación para N.O.V.A.
 * - Maneja login/logout
 * - Persiste token en AsyncStorage
 * - Expone utilidades para obtener token y estado de sesión
 */

import AsyncStorage from "@react-native-async-storage/async-storage";
import api from "./api";

const TOKEN_KEY = "nova_token";

const auth = {
  // Login con email/contraseña
  login: async (email, password) => {
    try {
      const response = await api.post("/auth/login", { email, password });
      if (response.data?.token) {
        await AsyncStorage.setItem(TOKEN_KEY, response.data.token);
        return true;
      }
      return false;
    } catch (error) {
      console.log("Error en login:", error.message);
      return false;
    }
  },

  // Logout → elimina token
  logout: async () => {
    try {
      await AsyncStorage.removeItem(TOKEN_KEY);
    } catch (error) {
      console.log("Error en logout:", error.message);
    }
  },

  // Obtener token actual
  getToken: async () => {
    try {
      return await AsyncStorage.getItem(TOKEN_KEY);
    } catch (error) {
      console.log("Error obteniendo token:", error.message);
      return null;
    }
  },

  // Verificar si hay sesión activa
  isAuthenticated: async () => {
    const token = await auth.getToken();
    return !!token;
  },
};

export default auth;
