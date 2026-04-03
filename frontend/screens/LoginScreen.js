/**
 * LoginScreen.js
 * ----------------------------
 * Pantalla de inicio de sesión de N.O.V.A
 * Premium, empresarial y atractiva
 */

import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  Image
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { useTranslation } from "react-i18next";
import auth from "../services/auth";
import logger from "../services/logger";

export default function LoginScreen({ navigation }) {
  const { t } = useTranslation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    if (!email.includes("@") || password.length < 6) {
      setError(t("auth.invalidCredentials"));
      logger.warning("[LOGIN] Credenciales inválidas");
      return;
    }

    try {
      const success = await auth.login(email, password);
      if (success) {
        logger.info("[LOGIN] Sesión iniciada correctamente");
        navigation.replace("Home");
      } else {
        setError(t("auth.invalidCredentials"));
        logger.error("[LOGIN] Fallo en autenticación");
      }
    } catch (error) {
      logger.error("[LOGIN] Error inesperado", error);
      setError(t("auth.serverError"));
    }
  };

  return (
    <LinearGradient
      colors={["#0A0F2C", "#3B0A45", "#0ACFFF"]}
      style={styles.container}
    >
      <KeyboardAvoidingView
        style={styles.innerContainer}
        behavior={Platform.OS === "ios" ? "padding" : undefined}
      >
        {/* Logo */}
        <Image
          source={require("../assets/logo.png")}
          style={styles.logo}
          resizeMode="contain"
        />

        <Text style={styles.title}>{t("auth.login")}</Text>

        {/* Inputs */}
        <TextInput
          style={[styles.input, error && styles.inputError]}
          placeholder={t("auth.email")}
          placeholderTextColor="#888"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />

        <TextInput
          style={[styles.input, error && styles.inputError]}
          placeholder={t("auth.password")}
          placeholderTextColor="#888"
          secureTextEntry
          value={password}
          onChangeText={setPassword}
        />

        {error ? <Text style={styles.errorText}>{error}</Text> : null}

        {/* Botón Login */}
        <TouchableOpacity style={styles.loginButton} onPress={handleLogin}>
          <Text style={styles.loginButtonText}>{t("auth.login")}</Text>
        </TouchableOpacity>

        {/* Botón Google OAuth */}
        <TouchableOpacity
          style={styles.googleButton}
          onPress={() => alert("Google OAuth")}
        >
          <Text style={styles.googleButtonText}>{t("auth.googleLogin")}</Text>
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
      </KeyboardAvoidingView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  innerContainer: { flex: 1, justifyContent: "center", alignItems: "center", padding: 20 },
  logo: { width: 120, height: 120, marginBottom: 20 },
  title: { fontSize: 28, fontWeight: "bold", marginBottom: 20, color: "#FFF", letterSpacing: 1.5 },
  input: {
    width: "100%",
    borderWidth: 1,
    borderColor: "#444",
    borderRadius: 12,
    paddingHorizontal: 15,
    paddingVertical: 12,
    marginBottom: 15,
    backgroundColor: "#111",
    fontSize: 16,
    color: "#FFF"
  },
  inputError: { borderColor: "#FF4D4D" },
  errorText: { color: "#FF4D4D", marginBottom: 10 },
  loginButton: {
    backgroundColor: "#00CFFF",
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: "center",
    marginBottom: 10,
    width: "100%",
    shadowColor: "#00CFFF",
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 4
  },
  loginButtonText: { color: "#0A0F2C", fontSize: 16, fontWeight: "700" },
  googleButton: {
    backgroundColor: "#DB4437",
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: "center",
    width: "100%",
    shadowColor: "#DB4437",
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 4
  },
  googleButtonText: { color: "#FFF", fontSize: 16, fontWeight: "700" },
  footer: { position: "absolute", bottom: 30, flexDirection: "row", alignItems: "center" },
  footerLogo: { width: 22, height: 22, marginRight: 8 },
  footerText: { color: "#BBB", fontSize: 14 }
});
