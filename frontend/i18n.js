/**
 * i18n.js
 * ----------------------------
 * Configuración de internacionalización para N.O.V.A
 * Carga los archivos de localización y selecciona el idioma
 * según la preferencia del usuario o el sistema.
 */

import i18n from "i18next";
import { initReactI18next } from "react-i18next";

// Importamos todos los idiomas
import es from "./localization/es.json";
import en from "./localization/en.json";
import fr from "./localization/fr.json";
import it from "./localization/it.json";
import pt from "./localization/pt.json";
import de from "./localization/de.json";
import zh from "./localization/zh.json";

i18n
  .use(initReactI18next)
  .init({
    resources: {
      es: { translation: es },
      en: { translation: en },
      fr: { translation: fr },
      it: { translation: it },
      pt: { translation: pt },
      de: { translation: de },
      zh: { translation: zh }
    },
    lng: "es", // Idioma por defecto
    fallbackLng: "en", // Si falta traducción, usa inglés
    interpolation: {
      escapeValue: false // react ya protege contra XSS
    }
  });

export default i18n;
