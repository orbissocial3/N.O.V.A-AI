import React, { useEffect, useRef } from "react";
import { View, Text, ActivityIndicator, StyleSheet, Animated, Image } from "react-native";
import { useTranslation } from "react-i18next";

export default function SplashScreen() {
  const { t } = useTranslation();
  const fadeAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 2000,
      useNativeDriver: true,
    }).start();
  }, []);

  return (
    <View style={styles.container}>
      {/* Animación de logo y nombre */}
      <Animated.View style={{ opacity: fadeAnim, alignItems: "center" }}>
        <Image
          source={require("../assets/logo.png")} // ruta corregida
          style={styles.logo}
          resizeMode="contain"
        />
        <Text style={styles.title}>{t("app.name")}</Text>
      </Animated.View>

      {/* Loader */}
      <ActivityIndicator size="large" color="#007AFF" style={{ marginTop: 20 }} />
      <Text style={styles.text}>{t("app.loading")}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#FFF" },
  logo: { width: 150, height: 150, marginBottom: 10 },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 10 },
  text: { marginTop: 10, fontSize: 16 },
});
