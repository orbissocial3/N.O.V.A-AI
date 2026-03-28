/**
 * usePlan.js
 * ----------------------------
 * Hook personalizado para manejar el plan de suscripción del usuario.
 * Se conecta al UserContext y expone:
 *  - Plan actual
 *  - Función para actualizar el plan
 */

import { useContext } from "react";
import { UserContext } from "../context/UserContext";

export default function usePlan() {
  // Obtenemos valores y funciones desde el contexto global
  const { plan, updatePlan } = useContext(UserContext);

  return {
    plan,
    updatePlan,
  };
}
