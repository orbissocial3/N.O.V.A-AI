import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import { useTranslation } from "react-i18next";
import auth from "../services/auth";   // ✔️ Ruta corregida

export default function LoginScreen({ navigation }) {
  const { t } = useTranslation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    if (!email.includes("@")) {
      alert(t("auth.invalidCredentials"));
      return;
    }
    if (password.length < 6) {
      alert(t("auth.invalidCredentials"));
      return;
    }

    const success = await auth.login(email, password);
    if (success) {
      navigation.replace("Home");
    } else {
      alert(t("auth.invalidCredentials"));
    }
  };

  return (
    <View style={styles.container}>
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

      <Button title={t("auth.login")} onPress={handleLogin} />
      <Button title={t("auth.googleLogin")} onPress={() => alert("Google OAuth")} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: "center" },
  title: { fontSize: 24, marginBottom: 20, textAlign: "center" },
  input: { borderWidth: 1, padding: 10, marginBottom: 10, borderRadius: 6 }
});
