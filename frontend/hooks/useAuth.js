/**
 * useAuth.js
 * ----------------------------
 * Hook personalizado para manejar la autenticación del usuario.
 * Se conecta al UserContext y expone:
 *  - Datos del usuario
 *  - Estado de autenticación
 *  - Funciones de login y logout
 *  - Estado de carga
 */

import { useContext } from "react";
import { UserContext } from "../context/UserContext";

export default function useAuth() {
  // Obtenemos valores y funciones desde el contexto global
  const {
    user,
    isAuthenticated,
    loading,
    login,
    logout,
  } = useContext(UserContext);

  return {
    user,
    isAuthenticated,
    loading,
    login,
    logout,
  };
}
