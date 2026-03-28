/**
 * i18n.js
 * ----------------------------
 * Configuración de internacionalización para N.O.V.A
 * Carga los archivos de localización y selecciona el idioma
 * según la preferencia del usuario o el sistema.
 */

import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import * as Localization from "expo-localization";
import AsyncStorage from "@react-native-async-storage/async-storage";
import logger from "./services/logger";

// Importamos todos los idiomas
import es from "./localization/es.json";
import en from "./localization/en.json";
import fr from "./localization/fr.json";
import it from "./localization/it.json";
import pt from "./localization/pt.json";
import de from "./localization/de.json";
import zh from "./localization/zh.json";

// Recursos de traducción
const resources = {
  es: { translation: es },
  en: { translation: en },
  fr: { translation: fr },
  it: { translation: it },
  pt: { translation: pt },
  de: { translation: de },
  zh: { translation: zh },
};

// Función para obtener idioma preferido
const getPreferredLanguage = async () => {
  try {
    const storedLang = await AsyncStorage.getItem("preferredLanguage");
    if (storedLang) {
      logger.info(`[i18n] Idioma preferido cargado: ${storedLang}`);
      return storedLang;
    }
  } catch (error) {
    logger.error("[i18n] Error obteniendo idioma preferido", error);
  }
  // Si no hay preferencia, usar idioma del sistema
  const systemLang = Localization.locale.split("-")[0];
  logger.info(`[i18n] Idioma del sistema detectado: ${systemLang}`);
  return resources[systemLang] ? systemLang : "en";
};

// Inicialización
(async () => {
  const preferredLang = await getPreferredLanguage();

  i18n
    .use(initReactI18next)
    .init({
      resources,
      lng: preferredLang,
      fallbackLng: "en", // fallback inteligente
      interpolation: {
        escapeValue: false, // react ya protege contra XSS
      },
      react: {
        useSuspense: false,
      },
    });

  logger.info(`[i18n] Inicializado con idioma: ${preferredLang}`);
})();

export default i18n;
