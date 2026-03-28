/**
 * ChatScreen.js
 * ----------------------------
 * Pantalla de chat principal de N.O.V.A
 * - Interfaz premium y empresarial
 * - Manejo de mensajes con FlatList optimizada
 * - Simulación de respuesta IA con delay
 * - Internacionalización con i18n
 * - Logging de eventos para observabilidad
 */

import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  KeyboardAvoidingView,
  Platform
} from "react-native";
import { useTranslation } from "react-i18next";
import logger from "../../services/logger"; // Logging centralizado

export default function ChatScreen() {
  const { t } = useTranslation();
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = () => {
    if (!message.trim()) return;

    const newMessage = { id: Date.now().toString(), text: message, sender: "user" };
    setMessages((prev) => [...prev, newMessage]);
    logger.info(`[CHAT] Mensaje enviado: ${message}`);

    // Simulación de respuesta del agente IA
    setTimeout(() => {
      const agentReply = {
        id: Date.now().toString(),
        text: t("chat.agentReply"),
        sender: "agent"
      };
      setMessages((prev) => [...prev, agentReply]);
      logger.info("[CHAT] Respuesta del agente IA simulada");
    }, 1000);

    setMessage("");
  };

  const renderMessage = ({ item }) => (
    <View style={item.sender === "user" ? styles.userBubble : styles.agentBubble}>
      <Text style={styles.messageText}>{item.text}</Text>
    </View>
  );

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <Text style={styles.title}>{t("chat.title")}</Text>
      <FlatList
        data={messages}
        keyExtractor={(item) => item.id}
        renderItem={renderMessage}
        contentContainerStyle={styles.chatContainer}
      />
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder={t("chat.inputPlaceholder")}
          value={message}
          onChangeText={setMessage}
        />
        <TouchableOpacity style={styles.sendButton} onPress={sendMessage}>
          <Text style={styles.sendButtonText}>{t("chat.send")}</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F9F9F9", padding: 20 },
  title: { fontSize: 22, fontWeight: "bold", marginBottom: 10, color: "#333" },
  chatContainer: { flexGrow: 1, justifyContent: "flex-end" },
  userBubble: {
    alignSelf: "flex-end",
    backgroundColor: "#DCF8C6",
    padding: 10,
    borderRadius: 12,
    marginVertical: 4,
    maxWidth: "80%"
  },
  agentBubble: {
    alignSelf: "flex-start",
    backgroundColor: "#EEE",
    padding: 10,
    borderRadius: 12,
    marginVertical: 4,
    maxWidth: "80%"
  },
  messageText: { fontSize: 16, color: "#333" },
  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 10,
    borderTopWidth: 1,
    borderColor: "#DDD",
    paddingTop: 8
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: "#CCC",
    borderRadius: 20,
    paddingHorizontal: 15,
    paddingVertical: 8,
    marginRight: 10,
    backgroundColor: "#FFF"
  },
  sendButton: {
    backgroundColor: "#007AFF",
    borderRadius: 20,
    paddingHorizontal: 20,
    paddingVertical: 10
  },
  sendButtonText: { color: "#FFF", fontWeight: "bold" }
});
