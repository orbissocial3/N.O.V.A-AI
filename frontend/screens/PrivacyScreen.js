/**
 * PrivacyScreen.js
 * ----------------------------
 * Pantalla de aceptación de políticas de N.O.V.A
 * - Diseño empresarial y premium
 * - Scroll elegante para lectura completa
 * - Botón de aceptación destacado
 * - Experiencia impecable y seria
 */

import React, { useState } from "react";
import {
  SafeAreaView,
  ScrollView,
  Text,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator
} from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useTranslation } from "react-i18next";
import logger from "../services/logger";

export default function PrivacyScreen({ navigation }) {
  const { t } = useTranslation();
  const [accepted, setAccepted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleAccept = async () => {
    setLoading(true);
    try {
      await AsyncStorage.setItem("privacyAccepted", "true");
      setAccepted(true);
      logger.info("[PRIVACY] Políticas aceptadas por el usuario");
      navigation.replace("Home"); // redirige al inicio de la app
    } catch (error) {
      logger.error("[PRIVACY] Error al guardar aceptación", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scroll}>
        <Text style={styles.title}>{t("privacy.title")}</Text>
        <Text style={styles.subtitle}>{t("privacy.lastUpdate")}: Marzo 2026</Text>

        {/* Documento legal */}
        <Text style={styles.text}>
          📜 Documento Legal – N.O.V.A{"\n\n"}
          {t("privacy.intro")}
          {"\n\n"}
          {/* Aquí se mantiene todo el contenido legal que ya tienes redactado */}
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
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F9FAFB" },
  scroll: { padding: 20 },
  title: {
    fontSize: 26,
    fontWeight: "bold",
    marginBottom: 10,
    textAlign: "center",
    color: "#1A1A1A"
  },
  subtitle: {
    fontSize: 14,
    color: "#555",
    marginBottom: 20,
    textAlign: "center"
  },
  text: {
    fontSize: 16,
    lineHeight: 24,
    color: "#333",
    marginBottom: 30
  },
  acceptButton: {
    backgroundColor: "#007AFF",
    paddingVertical: 16,
    margin: 20,
    borderRadius: 12,
    alignItems: "center",
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3
  },
  acceptButtonText: { color: "#FFF", fontSize: 18, fontWeight: "600" }
});
