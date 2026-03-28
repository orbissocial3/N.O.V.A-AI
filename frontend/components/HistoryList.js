/**
 * HistoryList.js
 * ----------------------------
 * Componente que muestra el historial de chats previos.
 * Recibe un array de mensajes y los renderiza en una lista.
 */

import React from "react";
import { View, Text, FlatList, StyleSheet } from "react-native";

export default function HistoryList({ history }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Historial de chats</Text>
      <FlatList
        data={history}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View
            style={[
              styles.message,
              item.role === "user" ? styles.user : styles.agent,
            ]}
          >
            <Text style={styles.text}>{item.text}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, marginVertical: 10 },
  title: { fontSize: 18, fontWeight: "bold", marginBottom: 10 },
  message: {
    padding: 8,
    borderRadius: 5,
    marginVertical: 2,
    maxWidth: "80%",
  },
  user: { alignSelf: "flex-end", backgroundColor: "#DCF8C6" },
  agent: { alignSelf: "flex-start", backgroundColor: "#EEE" },
  text: { fontSize: 16 },
});
