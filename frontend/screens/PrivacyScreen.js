/**
 * PrivacyScreen.js
 * ----------------------------
 * Pantalla de aceptación de políticas de N.O.V.A
 * Premium, sobria y empresarial
 */

import React, { useState } from "react";
import {
  SafeAreaView,
  ScrollView,
  Text,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  View,
  Image
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useTranslation } from "react-i18next";
import logger from "../services/logger";

export default function PrivacyScreen({ navigation }) {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false);

  const handleAccept = async () => {
    setLoading(true);
    try {
      await AsyncStorage.setItem("privacyAccepted", "true");
      logger.info("[PRIVACY] Políticas aceptadas por el usuario");
      navigation.replace("Home");
    } catch (error) {
      logger.error("[PRIVACY] Error al guardar aceptación", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <LinearGradient
      colors={["#0A0F2C", "#3B0A45", "#0ACFFF"]}
      style={styles.container}
    >
      <SafeAreaView style={{ flex: 1 }}>
        <ScrollView contentContainerStyle={styles.scroll}>
          <Text style={styles.title}>{t("privacy.title")}</Text>
          <Text style={styles.subtitle}>{t("privacy.lastUpdate")}: Marzo 2026</Text>

          {/* Documento legal */}
          <Text style={styles.text}>
            📜 Documento Legal – N.O.V.A{"\n\n"}
            {t("privacy.intro")}
            {"\n\n"}
            {/* Aquí se mantiene todo el contenido legal redactado */}
            {/* Se recomienda dividirlo en secciones con subtítulos claros */}
          </Text>
        </ScrollView>

        {/* Botón de aceptación */}
        <TouchableOpacity
          style={styles.acceptButton}
          onPress={handleAccept}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#FFF" />
          ) : (
            <Text style={styles.acceptButtonText}>{t("privacy.accept")}</Text>
          )}
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
      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  scroll: { padding: 20 },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    marginBottom: 10,
    textAlign: "center",
    color: "#FFF",
    letterSpacing: 1.5
  },
  subtitle: {
    fontSize: 14,
    color: "#DDD",
    marginBottom: 20,
    textAlign: "center"
  },
  text: {
    fontSize: 16,
    lineHeight: 24,
    color: "#EEE",
    marginBottom: 30
  },
  acceptButton: {
    backgroundColor: "#00CFFF",
    paddingVertical: 16,
    margin: 20,
    borderRadius: 12,
    alignItems: "center",
    shadowColor: "#00CFFF",
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 4
  },
  acceptButtonText: { color: "#0A0F2C", fontSize: 18, fontWeight: "700" },
  footer: {
    position: "absolute",
    bottom: 20,
    flexDirection: "row",
    alignItems: "center",
    alignSelf: "center"
  },
  footerLogo: { width: 22, height: 22, marginRight: 8 },
  footerText: { color: "#BBB", fontSize: 14 }
});
