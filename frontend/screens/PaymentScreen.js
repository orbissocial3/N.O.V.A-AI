/**
 * PaymentScreen.js
 * ----------------------------
 * Pantalla de pagos de N.O.V.A
 * Premium, sobria y empresarial
 */

import React, { useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  StyleSheet,
  Image
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { useTranslation } from "react-i18next";
import logger from "../services/logger";

export default function PaymentScreen() {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handlePayment = (method) => {
    logger.info(`[PAYMENT] Iniciando pago con ${method}`);
    setLoading(true);
    setSuccess(false);
    setTimeout(() => {
      setLoading(false);
      setSuccess(true);
      logger.info(`[PAYMENT] Pago exitoso con ${method}`);
    }, 2000);
  };

  const PaymentButton = ({ title, method, color }) => (
    <TouchableOpacity
      style={[styles.button, { backgroundColor: color }]}
      onPress={() => handlePayment(method)}
    >
      <Text style={styles.buttonText}>{title}</Text>
    </TouchableOpacity>
  );

  return (
    <LinearGradient
      colors={["#0A0F2C", "#3B0A45", "#0ACFFF"]}
      style={styles.container}
    >
      <Text style={styles.title}>{t("payment.title")}</Text>

      {loading ? (
        <ActivityIndicator size="large" color="#00CFFF" style={{ marginTop: 20 }} />
      ) : success ? (
        <Text style={styles.successText}>{t("payment.success")}</Text>
      ) : (
        <View style={styles.buttons}>
          <PaymentButton
            title={t("payment.paypal")}
            method="PayPal"
            color="#003087"
          />
          <PaymentButton
            title={t("payment.stripe")}
            method="Stripe"
            color="#635BFF"
          />
        </View>
      )}

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
  container: { flex: 1, justifyContent: "center", alignItems: "center", padding: 20 },
  title: {
    fontSize: 26,
    fontWeight: "bold",
    marginBottom: 30,
    textAlign: "center",
    color: "#FFF",
    letterSpacing: 1.5
  },
  buttons: { width: "100%", gap: 15 },
  button: {
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: "center",
    shadowColor: "#000",
    shadowOpacity: 0.2,
    shadowRadius: 6,
    elevation: 4
  },
  buttonText: { color: "#FFF", fontSize: 16, fontWeight: "700" },
  successText: {
    fontSize: 18,
    color: "#00CFFF",
    fontWeight: "600",
    marginTop: 20,
    textAlign: "center"
  },
  footer: {
    position: "absolute",
    bottom: 30,
    flexDirection: "row",
    alignItems: "center"
  },
  footerLogo: { width: 22, height: 22, marginRight: 8 },
  footerText: { color: "#BBB", fontSize: 14 }
});
