/**
 * PlanCard.js
 * ----------------------------
 * Componente que muestra la información de un plan de suscripción
 * - Diseño empresarial y premium
 * - Claridad absoluta en nombre, precio y beneficios
 * - Botón de selección llamativo y elegante
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
    borderColor: "#DDD",
    borderRadius: 16,
    padding: 20,
    marginVertical: 12,
    backgroundColor: "#FFF",
    shadowColor: "#000",
    shadowOpacity: 0.08,
    shadowRadius: 6,
    elevation: 4,
  },
  name: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 6,
    color: "#1A1A1A",
    textAlign: "center",
  },
  price: {
    fontSize: 20,
    color: "#007AFF",
    marginBottom: 12,
    textAlign: "center",
    fontWeight: "600",
  },
  benefits: { marginBottom: 15 },
  benefit: {
    fontSize: 15,
    color: "#333",
    marginVertical: 2,
    lineHeight: 22,
  },
  button: {
    backgroundColor: "#007AFF",
    paddingVertical: 14,
    borderRadius: 10,
    alignItems: "center",
    marginTop: 10,
    shadowColor: "#007AFF",
    shadowOpacity: 0.2,
    shadowRadius: 6,
    elevation: 3,
  },
  buttonText: { color: "#FFF", fontSize: 16, fontWeight: "600" },
});
