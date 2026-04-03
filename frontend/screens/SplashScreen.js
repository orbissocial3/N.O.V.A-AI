/**
 * SplashScreen.js
 * ----------------------------
 * Pantalla inicial de N.O.V.A
 * Premium, vibrante y oscura
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
import { LinearGradient } from "expo-linear-gradient";
import { useTranslation } from "react-i18next";

export default function SplashScreen() {
  const { t } = useTranslation();
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.8)).current;
  const blinkAnim = useRef(new Animated.Value(1)).current;

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
      }),
      Animated.loop(
        Animated.sequence([
          Animated.timing(blinkAnim, {
            toValue: 0,
            duration: 800,
            useNativeDriver: true
          }),
          Animated.timing(blinkAnim, {
            toValue: 1,
            duration: 800,
            useNativeDriver: true
          })
        ])
      )
    ]).start();
  }, []);

  return (
    <LinearGradient
      colors={["#0A0F2C", "#3B0A45", "#0ACFFF"]} // azul → púrpura → cian eléctrico
      style={styles.container}
    >
      {/* Logo y nombre */}
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
      <Animated.Text style={[styles.text, { opacity: blinkAnim }]}>
        {t("app.loading")}
      </Animated.Text>

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
  logo: { width: 180, height: 180, marginBottom: 15 },
  title: {
    fontSize: 32,
    fontWeight: "bold",
    marginBottom: 5,
    color: "#fff",
    letterSpacing: 1.5
  },
  subtitle: {
    fontSize: 18,
    color: "#ddd",
    marginBottom: 20,
    textAlign: "center"
  },
  text: { marginTop: 10, fontSize: 16, color: "#fff" },
  footer: {
    position: "absolute",
    bottom: 40,
    flexDirection: "row",
    alignItems: "center"
  },
  footerLogo: { width: 24, height: 24, marginRight: 8 },
  footerText: { color: "#bbb", fontSize: 14 }
});
