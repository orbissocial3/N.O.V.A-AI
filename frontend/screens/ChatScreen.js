/**
 * ChatScreen.js
 * ----------------------------
 * Pantalla de chat principal de N.O.V.A
 * Premium, limpia y empresarial
 */

import React, { useState, useRef } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  Animated
} from "react-native";
import { useTranslation } from "react-i18next";
import logger from "../../services/logger";

export default function ChatScreen() {
  const { t } = useTranslation();
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const fadeAnim = useRef(new Animated.Value(0)).current;

  const sendMessage = () => {
    if (!message.trim()) return;

    const newMessage = { id: Date.now().toString(), text: message, sender: "user" };
    setMessages((prev) => [...prev, newMessage]);
    logger.info(`[CHAT] Mensaje enviado: ${message}`);

    // Animación de entrada
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 500,
      useNativeDriver: true
    }).start();

    // Simulación de respuesta IA
    setTimeout(() => {
      const agentReply = {
        id: Date.now().toString(),
        text: t("chat.agentReply"),
        sender: "agent"
      };
      setMessages((prev) => [...prev, agentReply]);
      logger.info("[CHAT] Respuesta del agente IA simulada");
    }, 1200);

    setMessage("");
  };

  const renderMessage = ({ item }) => (
    <Animated.View
      style={[
        item.sender === "user" ? styles.userBubble : styles.agentBubble,
        { opacity: fadeAnim }
      ]}
    >
      <Text style={styles.messageText}>{item.text}</Text>
    </Animated.View>
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
          placeholderTextColor="#888"
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
  container: { flex: 1, backgroundColor: "#0A0F2C", padding: 20 },
  title: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 10,
    color: "#00CFFF",
    textAlign: "center",
    letterSpacing: 1.2
  },
  chatContainer: { flexGrow: 1, justifyContent: "flex-end" },
  userBubble: {
    alignSelf: "flex-end",
    backgroundColor: "#00CFFF",
    padding: 12,
    borderRadius: 16,
    marginVertical: 6,
    maxWidth: "80%",
    shadowColor: "#00CFFF",
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 4
  },
  agentBubble: {
    alignSelf: "flex-start",
    backgroundColor: "#1B1B2F",
    padding: 12,
    borderRadius: 16,
    marginVertical: 6,
    maxWidth: "80%",
    shadowColor: "#333",
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 2
  },
  messageText: { fontSize: 16, color: "#FFF" },
  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 10,
    borderTopWidth: 1,
    borderColor: "#222",
    paddingTop: 8
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: "#333",
    borderRadius: 25,
    paddingHorizontal: 15,
    paddingVertical: 10,
    marginRight: 10,
    backgroundColor: "#111",
    color: "#FFF"
  },
  sendButton: {
    backgroundColor: "#00CFFF",
    borderRadius: 25,
    paddingHorizontal: 20,
    paddingVertical: 10
  },
  sendButtonText: { color: "#0A0F2C", fontWeight: "bold", fontSize: 16 }
});
