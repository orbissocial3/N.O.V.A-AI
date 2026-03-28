    /**
 * UserContext.js
 * ----------------------------
 * Contexto global para manejar el estado del usuario en la aplicación N.O.V.A.
 * Aquí definimos:
 *  - Información del usuario (id, nombre, email)
 *  - Estado de autenticación (logueado o no)
 *  - Plan de suscripción activo
 *  - Idioma preferido
 *  - Funciones para login, logout y actualización de datos
 */

import React, { createContext, useState, useEffect } from "react";
import auth from "../services/auth";   // Servicio de autenticación
import api from "../services/api";     // Conexión al backend

// Creamos el contexto
export const UserContext = createContext();

// Proveedor del contexto
export const UserProvider = ({ children }) => {
  // Estado global del usuario
  const [user, setUser] = useState(null); // { id, name, email }
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [plan, setPlan] = useState(null); // { id, name, price, benefits }
  const [language, setLanguage] = useState("es"); // Idioma por defecto español
  const [loading, setLoading] = useState(true);

  // Inicialización: verificar si hay sesión activa
  useEffect(() => {
    const initializeUser = async () => {
      try {
        const token = await auth.getToken();
        if (token) {
          // Validamos token con backend
          const response = await api.get("/auth/validate", {
            headers: { Authorization: `Bearer ${token}` },
          });
          if (response.status === 200) {
            setUser(response.data.user);
            setPlan(response.data.plan);
            setIsAuthenticated(true);
          }
        }
      } catch (error) {
        console.log("Error inicializando usuario:", error.message);
      } finally {
        setLoading(false);
      }
    };

    initializeUser();
  }, []);

  // Función de login
  const login = async (credentials) => {
    try {
      const response = await auth.login(credentials);
      if (response.token) {
        await auth.saveToken(response.token);
        setUser(response.user);
        setPlan(response.plan);
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.log("Error en login:", error.message);
    }
  };

  // Función de logout
  const logout = async () => {
    try {
      await auth.clearToken();
      setUser(null);
      setPlan(null);
      setIsAuthenticated(false);
    } catch (error) {
      console.log("Error en logout:", error.message);
    }
  };

  // Función para actualizar plan
  const updatePlan = (newPlan) => {
    setPlan(newPlan);
  };

  // Función para cambiar idioma
  const changeLanguage = (lang) => {
    setLanguage(lang);
  };

  return (
    <UserContext.Provider
      value={{
        user,
        isAuthenticated,
        plan,
        language,
        loading,
        login,
        logout,
        updatePlan,
        changeLanguage,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};
