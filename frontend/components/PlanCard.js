/**
 * PlanCard.js
 * ----------------------------
 * Componente que muestra la información de un plan de suscripción.
 * Incluye nombre, precio y beneficios, con un botón para seleccionar.
 */

import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";

export default function PlanCard({ plan, onSelect }) {
  return (
    <View style={styles.card}>
      <Text style={styles.name}>{plan.name}</Text>
      <Text style={styles.price}>${plan.price}/mes</Text>
      <View style={styles.benefits}>
        {plan.benefits.map((benefit, index) => (
          <Text key={index} style={styles.benefit}>
            • {benefit}
          </Text>
        ))}
      </View>
      <TouchableOpacity
        style={styles.button}
        onPress={() => onSelect(plan.id)}
      >
        <Text style={styles.buttonText}>Seleccionar</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    borderWidth: 1,
    borderColor: "#CCC",
    borderRadius: 8,
    padding: 15,
    marginVertical: 10,
    backgroundColor: "#FFF",
  },
  name: { fontSize: 20, fontWeight: "bold", marginBottom: 5 },
  price: { fontSize: 18, color: "#007AFF", marginBottom: 10 },
  benefits: { marginBottom: 10 },
  benefit: { fontSize: 14, color: "#333" },
  button: {
    backgroundColor: "#007AFF",
    padding: 10,
    borderRadius: 5,
    alignItems: "center",
  },
  buttonText: { color: "#FFF", fontWeight: "bold" },
});
