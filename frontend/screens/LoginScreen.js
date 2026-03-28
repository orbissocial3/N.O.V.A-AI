/**
 * LoginScreen.js
 * ----------------------------
 * Pantalla de inicio de sesión de N.O.V.A
 * - Diseño empresarial y premium
 * - Validaciones claras y seguras
 * - Interacciones fluidas y atractivas
 * - Internacionalización con i18n
 * - Experiencia digna de la mejor IA
 */

import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform
} from "react-native";
import { useTranslation } from "react-i18next";
import auth from "../services/auth";
import logger from "../services/logger";

export default function LoginScreen({ navigation }) {
  const { t } = useTranslation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    if (!email.includes("@") || password.length < 6) {
      alert(t("auth.invalidCredentials"));
      logger.warning("[LOGIN] Credenciales inválidas");
      return;
    }

    try {
      const success = await auth.login(email, password);
      if (success) {
        logger.info("[LOGIN] Sesión iniciada correctamente");
        navigation.replace("Home");
      } else {
        alert(t("auth.invalidCredentials"));
        logger.error("[LOGIN] Fallo en autenticación");
      }
    } catch (error) {
      logger.error("[LOGIN] Error inesperado", error);
      alert(t("auth.serverError"));
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <Text style={styles.title}>{t("auth.login")}</Text>

      <TextInput
        style={styles.input}
        placeholder={t("auth.email")}
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />

      <TextInput
        style={styles.input}
        placeholder={t("auth.password")}
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      <TouchableOpacity style={styles.loginButton} onPress={handleLogin}>
        <Text style={styles.loginButtonText}>{t("auth.login")}</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.googleButton}
        onPress={() => alert("Google OAuth")}
      >
        <Text style={styles.googleButtonText}>{t("auth.googleLogin")}</Text>
      </TouchableOpacity>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: "center", backgroundColor: "#F9FAFB" },
  title: { fontSize: 26, fontWeight: "bold", marginBottom: 20, textAlign: "center", color: "#1A1A1A" },
  input: {
    borderWidth: 1,
    borderColor: "#CCC",
    borderRadius: 10,
    paddingHorizontal: 15,
    paddingVertical: 12,
    marginBottom: 15,
    backgroundColor: "#FFF",
    fontSize: 16
  },
  loginButton: {
    backgroundColor: "#007AFF",
    paddingVertical: 14,
    borderRadius: 10,
    alignItems: "center",
    marginBottom: 10,
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3
  },
  loginButtonText: { color: "#FFF", fontSize: 16, fontWeight: "600" },
  googleButton: {
    backgroundColor: "#DB4437",
    paddingVertical: 14,
    borderRadius: 10,
    alignItems: "center",
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3
  },
  googleButtonText: { color: "#FFF", fontSize: 16, fontWeight: "600" }
});
