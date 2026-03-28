/**
 * ChatInput.js
 * ----------------------------
 * Componente para escribir y enviar mensajes en el chat
 * - Diseño futurista y elegante
 * - Botón de envío premium con feedback visual
 * - Experiencia impecable y memorable
 */

import React, { useState } from "react";
import { View, TextInput, TouchableOpacity, Text, StyleSheet } from "react-native";

export default function ChatInput({ onSend }) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (text.trim()) {
      onSend(text);
      setText("");
    }
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        value={text}
        onChangeText={setText}
        placeholder="Escribe tu mensaje..."
        placeholderTextColor="#999"
      />
      <TouchableOpacity style={styles.sendButton} onPress={handleSend}>
        <Text style={styles.sendButtonText}>➤</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 10,
    backgroundColor: "#F0F2F5",
    borderRadius: 12,
    paddingHorizontal: 10,
    paddingVertical: 6,
    shadowColor: "#000",
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2
  },
  input: {
    flex: 1,
    borderWidth: 0,
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
    color: "#1A1A1A",
    backgroundColor: "#FFF",
    marginRight: 8,
    shadowColor: "#000",
    shadowOpacity: 0.03,
    shadowRadius: 2,
    elevation: 1
  },
  sendButton: {
    backgroundColor: "#007AFF",
    borderRadius: 50,
    width: 44,
    height: 44,
    alignItems: "center",
    justifyContent: "center",
    shadowColor: "#007AFF",
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 4
  },
  sendButtonText: {
    color: "#FFF",
    fontSize: 20,
    fontWeight: "bold"
  }
});
