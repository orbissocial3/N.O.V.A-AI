/**
 * PlanScreen.js
 * ----------------------------
 * Pantalla de selección de planes de N.O.V.A
 * Premium, transparente y empresarial
 */

import React, { useState } from "react";
import { View, Text, TouchableOpacity, StyleSheet, Image } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { useTranslation } from "react-i18next";
import logger from "../services/logger";

export default function PlanScreen() {
  const { t } = useTranslation();
  const [plan, setPlan] = useState("basic");

  const updatePlan = (newPlan) => {
    setPlan(newPlan);
    logger.info(`[PLAN] Plan actualizado a: ${newPlan}`);
    alert(`${t("plans.selectPlan")}: ${newPlan}`);
  };

  const PlanCard = ({ title, value, color, benefits }) => (
    <TouchableOpacity
      style={[
        styles.card,
        { borderColor: plan === value ? color : "#444" }
      ]}
      onPress={() => updatePlan(value)}
    >
      <Text style={[styles.cardTitle, { color }]}>{title}</Text>
      {benefits.map((b, i) => (
        <Text key={i} style={styles.cardBenefit}>• {b}</Text>
      ))}
      <Text style={styles.cardSelect}>
        {plan === value ? "✓ " + t("plans.selected") : ""}
      </Text>
    </TouchableOpacity>
  );

  return (
    <LinearGradient
      colors={["#0A0F2C", "#3B0A45", "#0ACFFF"]}
      style={styles.container}
    >
      <Text style={styles.title}>{t("plans.title")}</Text>
      <Text style={styles.current}>{t("plans.currentPlan")}: {plan}</Text>

      <View style={styles.cards}>
        <PlanCard
          title={t("plans.basic")}
          value="basic"
          color="#00CFFF"
          benefits={[
            t("plans.basicFeature1"),
            t("plans.basicFeature2"),
            t("plans.basicFeature3")
          ]}
        />
        <PlanCard
          title={t("plans.premium")}
          value="premium"
          color="#FF9500"
          benefits={[
            t("plans.premiumFeature1"),
            t("plans.premiumFeature2"),
            t("plans.premiumFeature3")
          ]}
        />
        <PlanCard
          title={t("plans.enterprise")}
          value="enterprise"
          color="#34C759"
          benefits={[
            t("plans.enterpriseFeature1"),
            t("plans.enterpriseFeature2"),
            t("plans.enterpriseFeature3")
          ]}
        />
      </View>

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
  container: { flex: 1, padding: 20, justifyContent: "center" },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    marginBottom: 10,
    textAlign: "center",
    color: "#FFF",
    letterSpacing: 1.5
  },
  current: { fontSize: 16, marginBottom: 20, textAlign: "center", color: "#DDD" },
  cards: { gap: 20 },
  card: {
    borderWidth: 2,
    borderRadius: 16,
    padding: 20,
    backgroundColor: "#111",
    shadowColor: "#000",
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 4
  },
  cardTitle: { fontSize: 20, fontWeight: "bold", marginBottom: 10 },
  cardBenefit: { fontSize: 14, color: "#CCC", marginBottom: 5 },
  cardSelect: { marginTop: 10, fontSize: 14, color: "#FFF" },
  footer: {
    position: "absolute",
    bottom: 30,
    flexDirection: "row",
    alignItems: "center",
    alignSelf: "center"
  },
  footerLogo: { width: 22, height: 22, marginRight: 8 },
  footerText: { color: "#BBB", fontSize: 14 }
});
