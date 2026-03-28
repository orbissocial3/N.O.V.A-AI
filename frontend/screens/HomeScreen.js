import React from "react";
import { View, Text, Button, StyleSheet, Image } from "react-native";
import { useTranslation } from "react-i18next";

export default function HomeScreen({ navigation }) {
  const { t } = useTranslation();

  return (
    <View style={styles.container}>
      {/* Logo y bienvenida */}
      <Image
        source={require("../assets/logo.png")} // ruta corregida
        style={styles.logo}
        resizeMode="contain"
      />
      <Text style={styles.title}>{t("app.welcome")}</Text>

      {/* Accesos rápidos */}
      <View style={styles.buttons}>
        <Button title={t("chat.title")} onPress={() => navigation.navigate("Chat")} />
        <Button title={t("plans.title")} onPress={() => navigation.navigate("Plans")} />
        <Button title={t("payment.title")} onPress={() => navigation.navigate("Payment")} />
        <Button title={t("settings.title")} onPress={() => navigation.navigate("Settings")} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#FFF" },
  logo: { width: 150, height: 150, marginBottom: 20 },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 30 },
  buttons: { width: "80%", gap: 10 },
});
