/**
 * ChatInput.js
 * ----------------------------
 * Componente para escribir y enviar mensajes en el chat.
 * Incluye un TextInput y un botón de enviar.
 */

import React, { useState } from "react";
import { View, TextInput, Button, StyleSheet } from "react-native";

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
      />
      <Button title="Enviar" onPress={handleSend} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flexDirection: "row", alignItems: "center", marginTop: 10 },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: "#CCC",
    borderRadius: 5,
    padding: 8,
    marginRight: 5,
  },
});
