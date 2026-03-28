import { useState, useEffect } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";

export function usePreferences() {
  const [language, setLanguage] = useState("es");
  const [theme, setTheme] = useState("light");
  const [notifications, setNotifications] = useState(true);

  // Cargar preferencias al iniciar
  useEffect(() => {
    const loadPreferences = async () => {
      try {
        const storedLang = await AsyncStorage.getItem("language");
        const storedTheme = await AsyncStorage.getItem("theme");
        const storedNotif = await AsyncStorage.getItem("notifications");

        if (storedLang) setLanguage(storedLang);
        if (storedTheme) setTheme(storedTheme);
        if (storedNotif !== null) setNotifications(storedNotif === "true");
      } catch (error) {
        console.log("Error cargando preferencias:", error);
      }
    };
    loadPreferences();
  }, []);

  // Guardar preferencias
  const savePreferences = async (prefs) => {
    try {
      if (prefs.language) {
        setLanguage(prefs.language);
        await AsyncStorage.setItem("language", prefs.language);
      }
      if (prefs.theme) {
        setTheme(prefs.theme);
        await AsyncStorage.setItem("theme", prefs.theme);
      }
      if (prefs.notifications !== undefined) {
        setNotifications(prefs.notifications);
        await AsyncStorage.setItem("notifications", prefs.notifications.toString());
      }
    } catch (error) {
      console.log("Error guardando preferencias:", error);
    }
  };

  return { language, theme, notifications, savePreferences };
}
