import React, { useState } from "react";
import { View, Text, Button, ActivityIndicator, StyleSheet } from "react-native";
import { useTranslation } from "react-i18next";

export default function PaymentScreen() {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false);

  const handlePayment = (method) => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      alert(t("payment.success"));
    }, 2000);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{t("payment.title")}</Text>
      {loading ? (
        <ActivityIndicator size="large" color="#007AFF" />
      ) : (
        <>
          <Button title={t("payment.paypal")} onPress={() => handlePayment("PayPal")} />
          <Button title={t("payment.stripe")} onPress={() => handlePayment("Stripe")} />
          <Button title={t("payment.googlePlay")} onPress={() => handlePayment("Google Play")} />
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 20, marginBottom: 20 }
});
