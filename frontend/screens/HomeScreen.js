/**
 * HomeScreen.js
 * ----------------------------
 * Pantalla principal de N.O.V.A
 * Premium, futurista y minimalista
 */

import React from "react";
import { View, Text, TouchableOpacity, StyleSheet, Image } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
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
    <LinearGradient
      colors={["#0A0F2C", "#1B0A45", "#0ACFFF"]} // degradado vibrante y oscuro
      style={styles.container}
    >
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
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  logo: { width: 180, height: 180, marginBottom: 20 },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#FFFFFF",
    marginBottom: 10,
    letterSpacing: 1.5
  },
  subtitle: {
    fontSize: 16,
    color: "#DDD",
    marginBottom: 30,
    textAlign: "center"
  },
  buttons: {
    width: "100%",
    gap: 15,
    marginTop: 20
  },
  button: {
    backgroundColor: "#0ACFFF",
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: "center",
    shadowColor: "#00CFFF",
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 4
  },
  buttonText: {
    color: "#0A0F2C",
    fontSize: 16,
    fontWeight: "700",
    letterSpacing: 1
  },
  footer: {
    position: "absolute",
    bottom: 40,
    flexDirection: "row",
    alignItems: "center"
  },
  footerLogo: { width: 24, height: 24, marginRight: 8 },
  footerText: { color: "#BBB", fontSize: 14 }
});
