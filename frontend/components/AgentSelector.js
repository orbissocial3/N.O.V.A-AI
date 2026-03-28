/**
 * AgentSelector.js
 * ----------------------------
 * Componente para seleccionar el agente de IA
 * - Diseño empresarial y premium
 * - Feedback visual inmediato
 * - Experiencia impecable y atractiva
 */

import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";

const agents = [
  { id: "student", name: "🎓 Estudiante" },
  { id: "programmer", name: "💻 Programador" },
  { id: "secretary", name: "📑 Secretario" },
  { id: "investor", name: "📈 Inversor" },
  { id: "creative", name: "🎨 Creativo" },
];

export default function AgentSelector({ selectedAgent, onSelect }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Selecciona tu agente IA:</Text>
      {agents.map((agent) => (
        <TouchableOpacity
          key={agent.id}
          style={[
            styles.button,
            selectedAgent === agent.id && styles.selectedButton,
          ]}
          onPress={() => onSelect(agent.id)}
        >
          <Text
            style={[
              styles.buttonText,
              selectedAgent === agent.id && styles.selectedText,
            ]}
          >
            {agent.name}
          </Text>
        </TouchableOpacity>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { marginVertical: 20 },
  title: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 15,
    textAlign: "center",
    color: "#1A1A1A",
  },
  button: {
    paddingVertical: 14,
    paddingHorizontal: 20,
    backgroundColor: "#EEE",
    borderRadius: 10,
    marginVertical: 6,
    shadowColor: "#000",
    shadowOpacity: 0.05,
    shadowRadius: 3,
    elevation: 2,
    alignItems: "center",
  },
  selectedButton: {
    backgroundColor: "#007AFF",
    shadowOpacity: 0.2,
    shadowRadius: 6,
    elevation: 4,
  },
  buttonText: { fontSize: 16, fontWeight: "500", color: "#333" },
  selectedText: { color: "#FFF", fontWeight: "600" },
});
