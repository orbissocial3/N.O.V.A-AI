/**
 * color.js
 * ----------------------------
 * Paleta de colores definitiva de N.O.V.A
 * Adaptada del sistema visual refinado:
 *  - Base oscura premium
 *  - Acentos luminosos futuristas
 *  - Color energético para alertas/marketing
 */

export const LightThemeColors = {
  // Base
  background: "#FFFFFF",
  text: "#0A0A0C",          // Nova Black para contraste en modo claro
  mutedText: "#555555",
  border: "#A7A9AC",        // Stellar Silver

  // Acentos
  primary: "#3A7BFF",       // Nova Blue
  secondary: "#7A3CFF",     // Quantum Purple
  accent: "#00E5FF",        // Origin Cyan

  // Estados
  success: "#34C759",
  error: "#FF3B30",
  warning: "#FF9500",
  info: "#5AC8FA",

  // Energía
  energetic: "#FF7A29",     // Solar Flare Orange
};

export const DarkThemeColors = {
  // Base
  background: "#0A0A0C",    // Nova Black
  card: "#1C1E22",          // Deep Space Gray
  text: "#FFFFFF",
  mutedText: "#A7A9AC",     // Stellar Silver
  border: "#3A3A3C",

  // Acentos
  primary: "#3A7BFF",       // Nova Blue
  secondary: "#7A3CFF",     // Quantum Purple
  accent: "#00E5FF",        // Origin Cyan

  // Estados
  success: "#32D74B",
  error: "#FF453A",
  warning: "#FFD60A",
  info: "#64D2FF",

  // Energía
  energetic: "#FF7A29",     // Solar Flare Orange
};

// Exportar objeto global
export const Colors = {
  light: LightThemeColors,
  dark: DarkThemeColors,
};
