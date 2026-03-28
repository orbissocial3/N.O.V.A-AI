import React, { useState } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";
import { useTranslation } from "react-i18next";

export default function ChatScreen() {
  const { t } = useTranslation();
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = () => {
    if (!message.trim()) return;
    const newMessage = { id: Date.now().toString(), text: message, sender: "user" };
    setMessages([...messages, newMessage]);

    // Simulación de respuesta del agente IA
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { id: Date.now().toString(), text: t("chat.agentReply"), sender: "agent" }
      ]);
    }, 1000);

    setMessage("");
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{t("chat.title")}</Text>
      <FlatList
        data={messages}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <Text style={item.sender === "user" ? styles.userMsg : styles.agentMsg}>
            {item.text}
          </Text>
        )}
      />
      <TextInput
        style={styles.input}
        placeholder={t("chat.inputPlaceholder")}
        value={message}
        onChangeText={setMessage}
      />
      <Button title={t("chat.send")} onPress={sendMessage} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 20, marginBottom: 10 },
  input: { borderWidth: 1, padding: 10, marginBottom: 10 },
  userMsg: { alignSelf: "flex-end", backgroundColor: "#DCF8C6", padding: 8, marginVertical: 4 },
  agentMsg: { alignSelf: "flex-start", backgroundColor: "#EEE", padding: 8, marginVertical: 4 }
});
