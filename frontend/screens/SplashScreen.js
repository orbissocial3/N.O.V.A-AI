/**
 * SplashScreen.js
 * ----------------------------
 * Pantalla inicial de N.O.V.A
 * - Fondo degradado premium (azul → púrpura)
 * - Logo y nombre con animación elegante
 * - Loader en cian brillante
 * - Footer estilo META con branding corporativo
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
import { LinearGradient } from "expo-linear-gradient"; // para el degradado
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
    <LinearGradient
      colors={["#0A0F2C", "#3B0A45"]} // azul profundo → púrpura premium
      style={styles.container}
    >
      {/* Animación de logo y nombre */}
      <Animated.View
        style={{
          opacity: fadeAnim,
          transform: [{ scale: scaleAnim }],
          alignItems: "center"
        }}
      >
        <Image
          source={require("../assets/logo.png")}
          style={styles.logo}
          resizeMode="contain"
        />
        <Text style={styles.title}>{t("app.name")}</Text>
        <Text style={styles.subtitle}>{t("app.tagline")}</Text>
      </Animated.View>

      {/* Loader premium */}
      <ActivityIndicator size="large" color="#00CFFF" style={{ marginTop: 30 }} />
      <Text style={styles.text}>{t("app.loading")}</Text>

      {/* Footer estilo META */}
      <View style={styles.footer}>
        <Image
          source={require("../assets/logo.png")}
          style={styles.footerLogo}
          resizeMode="contain"
        />
        <Text style={styles.footerText}>From Nova Artificial Intelligence Systems</Text>
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  logo: { width: 160, height: 160, marginBottom: 15 },
  title: { fontSize: 30, fontWeight: "bold", marginBottom: 5, color: "#fff", letterSpacing: 1 },
  subtitle: { fontSize: 16, color: "#ddd", marginBottom: 20, textAlign: "center" },
  text: { marginTop: 10, fontSize: 16, color: "#fff" },
  footer: { position: "absolute", bottom: 40, flexDirection: "row", alignItems: "center" },
  footerLogo: { width: 22, height: 22, marginRight: 8 },
  footerText: { color: "#bbb", fontSize: 14 }
});
