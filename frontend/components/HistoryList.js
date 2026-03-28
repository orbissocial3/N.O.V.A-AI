/**
 * HistoryList.js
 * ----------------------------
 * Componente que muestra el historial de chats previos
 * - Diseño empresarial y premium
 * - Diferenciación clara entre mensajes de usuario y agente
 * - Interactividad y limpieza impecable
 */

import React from "react";
import { View, Text, FlatList, StyleSheet } from "react-native";

export default function HistoryList({ history }) {
  const renderMessage = ({ item }) => (
    <View
      style={[
        styles.message,
        item.role === "user" ? styles.user : styles.agent,
      ]}
    >
      <Text
        style={[
          styles.text,
          item.role === "user" ? styles.userText : styles.agentText,
        ]}
      >
        {item.text}
      </Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>📜 Historial de chats</Text>
      <FlatList
        data={history}
        keyExtractor={(item, index) => index.toString()}
        renderItem={renderMessage}
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, marginVertical: 15, backgroundColor: "#F9FAFB", borderRadius: 12, padding: 10 },
  title: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 15,
    textAlign: "center",
    color: "#1A1A1A"
  },
  list: { paddingBottom: 20 },
  message: {
    padding: 12,
    borderRadius: 12,
    marginVertical: 6,
    maxWidth: "80%",
    shadowColor: "#000",
    shadowOpacity: 0.05,
    shadowRadius: 3,
    elevation: 2
  },
  user: {
    alignSelf: "flex-end",
    backgroundColor: "#007AFF",
  },
  agent: {
    alignSelf: "flex-start",
    backgroundColor: "#EEE",
  },
  text: { fontSize: 16, lineHeight: 22 },
  userText: { color: "#FFF", fontWeight: "600" },
  agentText: { color: "#333" },
});
