import React from "react";
import { View, Text, Button, StyleSheet, Switch } from "react-native";
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

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{t("settings.title")}</Text>

      <Text>{t("settings.language")}</Text>
      <Button title="Español" onPress={() => changeLanguage("es")} />
      <Button title="English" onPress={() => changeLanguage("en")} />
      <Button title="Français" onPress={() => changeLanguage("fr")} />
      <Button title="Italiano" onPress={() => changeLanguage("it")} />
      <Button title="Português" onPress={() => changeLanguage("pt")} />
      <Button title="Deutsch" onPress={() => changeLanguage("de")} />
      <Button title="中文" onPress={() => changeLanguage("zh")} />

      <Text style={{ marginTop: 20 }}>{t("settings.notifications")}</Text>
      <Switch value={notifications} onValueChange={toggleNotifications} />

      <Text style={{ marginTop: 20 }}>Tema actual: {theme}</Text>
      <Button title="Cambiar tema" onPress={toggleTheme} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 20, marginBottom: 20 }
});
