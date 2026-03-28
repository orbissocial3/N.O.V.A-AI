/**
 * SettingsScreen.js
 * ----------------------------
 * Pantalla de configuración de N.O.V.A
 * - Diseño empresarial y premium
 * - Control total de idioma, tema y notificaciones
 * - Internacionalización con i18n
 * - Experiencia impecable y elegante
 */

import React from "react";
import { View, Text, TouchableOpacity, StyleSheet, Switch } from "react-native";
import { useTranslation } from "react-i18next";
import i18n from "../../i18n";
import { usePreferences } from "../hooks/usePreferences";

export default function SettingsScreen() {
  const { t } = useTranslation();
  const { language, theme, notifications, savePreferences } = usePreferences();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    savePreferences({ language: lng });
  };

  const toggleNotifications = () => {
    savePreferences({ notifications: !notifications });
  };

  const toggleTheme = () => {
    savePreferences({ theme: theme === "light" ? "dark" : "light" });
  };

  const LanguageButton = ({ label, lng }) => (
    <TouchableOpacity
      style={[
        styles.languageButton,
        { backgroundColor: language === lng ? "#007AFF" : "#EEE" }
      ]}
      onPress={() => changeLanguage(lng)}
    >
      <Text style={styles.languageText}>{label}</Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{t("settings.title")}</Text>

      {/* Idiomas */}
      <Text style={styles.sectionTitle}>{t("settings.language")}</Text>
      <View style={styles.languageContainer}>
        <LanguageButton label="Español" lng="es" />
        <LanguageButton label="English" lng="en" />
        <LanguageButton label="Français" lng="fr" />
        <LanguageButton label="Italiano" lng="it" />
        <LanguageButton label="Português" lng="pt" />
        <LanguageButton label="Deutsch" lng="de" />
        <LanguageButton label="中文" lng="zh" />
      </View>

      {/* Notificaciones */}
      <Text style={styles.sectionTitle}>{t("settings.notifications")}</Text>
      <Switch value={notifications} onValueChange={toggleNotifications} />

      {/* Tema */}
      <Text style={styles.sectionTitle}>{t("settings.theme")}</Text>
      <TouchableOpacity style={styles.themeButton} onPress={toggleTheme}>
        <Text style={styles.themeText}>
          {t("settings.currentTheme")}: {theme === "light" ? t("settings.light") : t("settings.dark")}
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: "#F9FAFB" },
  title: { fontSize: 26, fontWeight: "bold", marginBottom: 20, textAlign: "center", color: "#1A1A1A" },
  sectionTitle: { fontSize: 18, fontWeight: "600", marginTop: 20, marginBottom: 10, color: "#007AFF" },
  languageContainer: { flexDirection: "row", flexWrap: "wrap", gap: 10 },
  languageButton: {
    paddingVertical: 10,
    paddingHorizontal: 15,
    borderRadius: 8,
    marginBottom: 10,
    shadowColor: "#000",
    shadowOpacity: 0.05,
    shadowRadius: 3,
    elevation: 2
  },
  languageText: { fontSize: 14, fontWeight: "500", color: "#1A1A1A" },
  themeButton: {
    backgroundColor: "#007AFF",
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: "center",
    marginTop: 10,
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3
  },
  themeText: { color: "#FFF", fontSize: 16, fontWeight: "600" }
});
