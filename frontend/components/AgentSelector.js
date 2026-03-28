/**
 * AgentSelector.js
 * ----------------------------
 * Componente para seleccionar el agente de IA con el que el usuario quiere interactuar.
 * Muestra una lista de agentes disponibles y permite elegir uno.
 */

import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";

const agents = [
  { id: "student", name: "Estudiante" },
  { id: "programmer", name: "Programador" },
  { id: "secretary", name: "Secretario" },
  { id: "investor", name: "Inversor" },
  { id: "creative", name: "Creativo" },
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
          <Text style={styles.buttonText}>{agent.name}</Text>
        </TouchableOpacity>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { marginVertical: 10 },
  title: { fontSize: 18, fontWeight: "bold", marginBottom: 10 },
  button: {
    padding: 10,
    backgroundColor: "#EEE",
    borderRadius: 5,
    marginVertical: 5,
  },
  selectedButton: { backgroundColor: "#007AFF" },
  buttonText: { color: "#000" },
});
