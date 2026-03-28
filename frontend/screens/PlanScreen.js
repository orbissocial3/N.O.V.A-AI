/**
 * PlanScreen.js
 * ----------------------------
 * Pantalla de selección de planes de N.O.V.A
 * - Diseño empresarial y premium
 * - Interacciones fluidas y atractivas
 * - Internacionalización con i18n
 * - Experiencia impecable y soñadora
 */

import React, { useState } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { useTranslation } from "react-i18next";
import logger from "../services/logger"; // Observabilidad

export default function PlanScreen() {
  const { t } = useTranslation();
  const [plan, setPlan] = useState("basic");

  const updatePlan = (newPlan) => {
    setPlan(newPlan);
    logger.info(`[PLAN] Plan actualizado a: ${newPlan}`);
    alert(`${t("plans.selectPlan")}: ${newPlan}`);
  };

  const PlanButton = ({ title, value, color }) => (
    <TouchableOpacity
      style={[
        styles.button,
        { backgroundColor: plan === value ? color : "#EEE" }
      ]}
      onPress={() => updatePlan(value)}
    >
      <Text style={styles.buttonText}>
        {title} {plan === value ? "✓" : ""}
      </Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{t("plans.title")}</Text>
      <Text style={styles.current}>{t("plans.currentPlan")}: {plan}</Text>

      <View style={styles.buttons}>
        <PlanButton title={t("plans.basic")} value="basic" color="#007AFF" />
        <PlanButton title={t("plans.premium")} value="premium" color="#FF9500" />
        <PlanButton title={t("plans.enterprise")} value="enterprise" color="#34C759" />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: "center", backgroundColor: "#F9FAFB" },
  title: { fontSize: 26, fontWeight: "bold", marginBottom: 20, textAlign: "center", color: "#1A1A1A" },
  current: { fontSize: 16, marginBottom: 30, textAlign: "center", color: "#555" },
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
  buttonText: { fontSize: 16, fontWeight: "600", color: "#1A1A1A" }
});
