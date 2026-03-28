import React from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import { useTranslation } from "react-i18next";

export default function PlanScreen() {
  const { t } = useTranslation();
  const [plan, setPlan] = React.useState("basic");

  const updatePlan = (newPlan) => {
    setPlan(newPlan);
    alert(`${t("plans.selectPlan")}: ${newPlan}`);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{t("plans.title")}</Text>
      <Text>{t("plans.currentPlan")}: {plan}</Text>
      <Button title={t("plans.basic")} onPress={() => updatePlan("basic")} />
      <Button title={t("plans.premium")} onPress={() => updatePlan("premium")} />
      <Button title={t("plans.enterprise")} onPress={() => updatePlan("enterprise")} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 20, marginBottom: 20 }
});
