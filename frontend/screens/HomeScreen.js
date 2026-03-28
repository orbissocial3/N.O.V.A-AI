/**
 * HomeScreen.js
 * ----------------------------
 * Pantalla principal de N.O.V.A
 * - Bienvenida premium con logo
 * - Accesos rápidos estilizados
 * - Experiencia visual limpia y empresarial
 */

import React from "react";
import { View, Text, TouchableOpacity, StyleSheet, Image } from "react-native";
import { useTranslation } from "react-i18next";

export default function HomeScreen({ navigation }) {
  const { t } = useTranslation();

  const QuickButton = ({ title, screen }) => (
    <TouchableOpacity
      style={styles.button}
      onPress={() => navigation.navigate(screen)}
    >
      <Text style={styles.buttonText}>{title}</Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      {/* Logo y bienvenida */}
      <Image
        source={require("../assets/logo.png")}
        style={styles.logo}
        resizeMode="contain"
      />
      <Text style={styles.title}>{t("app.welcome")}</Text>
      <Text style={styles.subtitle}>{t("app.tagline")}</Text>

      {/* Accesos rápidos */}
      <View style={styles.buttons}>
        <QuickButton title={t("chat.title")} screen="Chat" />
        <QuickButton title={t("plans.title")} screen="Plans" />
        <QuickButton title={t("payment.title")} screen="Payment" />
        <QuickButton title={t("settings.title")} screen="Settings" />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    justifyContent: "center", 
    alignItems: "center", 
    backgroundColor: "#F9FAFB", 
    padding: 20 
  },
  logo: { 
    width: 160, 
    height: 160, 
    marginBottom: 20 
  },
  title: { 
    fontSize: 26, 
    fontWeight: "bold", 
    color: "#1A1A1A", 
    marginBottom: 10 
  },
  subtitle: { 
    fontSize: 16, 
    color: "#555", 
    marginBottom: 30, 
    textAlign: "center" 
  },
  buttons: { 
    width: "100%", 
    gap: 15 
  },
  button: {
    backgroundColor: "#007AFF",
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: "center",
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3
  },
  buttonText: { 
    color: "#FFF", 
    fontSize: 16, 
    fontWeight: "600" 
  }
});
