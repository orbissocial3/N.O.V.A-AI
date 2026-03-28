/**
 * PaymentScreen.js
 * ----------------------------
 * Pantalla de pagos de N.O.V.A
 * - Diseño empresarial y premium
 * - Interacciones fluidas y atractivas
 * - Internacionalización con i18n
 * - Simulación de proceso de pago con feedback visual
 */

import React, { useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  StyleSheet
} from "react-native";
import { useTranslation } from "react-i18next";
import logger from "../services/logger"; // Observabilidad

export default function PaymentScreen() {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false);

  const handlePayment = (method) => {
    logger.info(`[PAYMENT] Iniciando pago con ${method}`);
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      alert(t("payment.success"));
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
    <View style={styles.container}>
      <Text style={styles.title}>{t("payment.title")}</Text>
      {loading ? (
        <ActivityIndicator size="large" color="#007AFF" />
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
          <PaymentButton
            title={t("payment.googlePlay")}
            method="Google Play"
            color="#34A853"
          />
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: "center", backgroundColor: "#F9FAFB" },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 30, textAlign: "center", color: "#1A1A1A" },
  buttons: { gap: 15 },
  button: {
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: "center",
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3
  },
  buttonText: { color: "#FFF", fontSize: 16, fontWeight: "600" }
});
