/**
 * SettingsScreen.js
 * ----------------------------
 * Pantalla de configuración de N.O.V.A
 * Premium, transparente y empresarial
 */

import React from "react";
import { View, Text, TouchableOpacity, StyleSheet, Switch, Image } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
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
        { backgroundColor: language === lng ? "#00CFFF" : "#222" }
      ]}
      onPress={() => changeLanguage(lng)}
    >
      <Text style={styles.languageText}>{label}</Text>
    </TouchableOpacity>
  );

  return (
    <LinearGradient
      colors={["#0A0F2C", "#3B0A45", "#0ACFFF"]}
      style={styles.container}
    >
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
      <Switch
        value={notifications}
        onValueChange={toggleNotifications}
        trackColor={{ false: "#444", true: "#00CFFF" }}
        thumbColor={notifications ? "#FFF" : "#888"}
      />

      {/* Tema */}
      <Text style={styles.sectionTitle}>{t("settings.theme")}</Text>
      <TouchableOpacity style={styles.themeButton} onPress={toggleTheme}>
        <Text style={styles.themeText}>
          {t("settings.currentTheme")}: {theme === "light" ? t("settings.light") : t("settings.dark")}
        </Text>
      </TouchableOpacity>

      {/* Footer corporativo */}
      <View style={styles.footer}>
        <Image
          source={require("../assets/logo.png")}
          style={styles.footerLogo}
          resizeMode="contain"
        />
        <Text style={styles.footerText}>
          From: Nova Artificial Intelligence Systems
        </Text>
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    marginBottom: 20,
    textAlign: "center",
    color: "#FFF",
    letterSpacing: 1.5
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "600",
    marginTop: 20,
    marginBottom: 10,
    color: "#00CFFF"
  },
  languageContainer: { flexDirection: "row", flexWrap: "wrap", gap: 10 },
  languageButton: {
    paddingVertical: 10,
    paddingHorizontal: 15,
    borderRadius: 8,
    marginBottom: 10,
    shadowColor: "#000",
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 3
  },
  languageText: { fontSize: 14, fontWeight: "500", color: "#FFF" },
  themeButton: {
    backgroundColor: "#00CFFF",
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: "center",
    marginTop: 10,
    shadowColor: "#00CFFF",
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 4
  },
  themeText: { color: "#0A0F2C", fontSize: 16, fontWeight: "700" },
  footer: {
    position: "absolute",
    bottom: 30,
    flexDirection: "row",
    alignItems: "center",
    alignSelf: "center"
  },
  footerLogo: { width: 22, height: 22, marginRight: 8 },
  footerText: { color: "#BBB", fontSize: 14 }
});
