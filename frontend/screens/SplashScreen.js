/**
 * SplashScreen.js
 * ----------------------------
 * Pantalla inicial de N.O.V.A
 * - Animación cautivadora y premium
 * - Logo y nombre con fade-in elegante
 * - Loader con sensación empresarial
 * - Experiencia impecable y emocional
 */

import React, { useEffect, useRef } from "react";
import {
  View,
  Text,
  ActivityIndicator,
  StyleSheet,
  Animated,
  Image
} from "react-native";
import { useTranslation } from "react-i18next";

export default function SplashScreen() {
  const { t } = useTranslation();
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.8)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 2000,
        useNativeDriver: true
      }),
      Animated.spring(scaleAnim, {
        toValue: 1,
        friction: 4,
        tension: 40,
        useNativeDriver: true
      })
    ]).start();
  }, []);

  return (
    <View style={styles.container}>
      {/* Animación de logo y nombre */}
      <Animated.View
        style={{
          opacity: fadeAnim,
          transform: [{ scale: scaleAnim }],
          alignItems: "center"
        }}
      >
        <Image
          source={require("../assets/logo.png")} // ruta corregida
          style={styles.logo}
          resizeMode="contain"
        />
        <Text style={styles.title}>{t("app.name")}</Text>
        <Text style={styles.subtitle}>{t("app.tagline")}</Text>
      </Animated.View>

      {/* Loader */}
      <ActivityIndicator size="large" color="#007AFF" style={{ marginTop: 30 }} />
      <Text style={styles.text}>{t("app.loading")}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#F9FAFB" },
  logo: { width: 160, height: 160, marginBottom: 15 },
  title: { fontSize: 28, fontWeight: "bold", marginBottom: 5, color: "#1A1A1A" },
  subtitle: { fontSize: 16, color: "#555", marginBottom: 20, textAlign: "center" },
  text: { marginTop: 10, fontSize: 16, color: "#333" }
});
