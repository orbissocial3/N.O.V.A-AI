/**
 * test_chat.js
 * ----------------------------
 * Pruebas unitarias para ChatScreen
 * - Renderizado inicial
 * - Envío de mensaje por el usuario
 * - Respuesta automática del agente IA
 */

import React from "react";
import { render, fireEvent, waitFor } from "@testing-library/react-native";
import ChatScreen from "../screens/ChatScreen";
import { I18nextProvider } from "react-i18next";
import i18n from "../i18n";

describe("ChatScreen", () => {
  const renderWithI18n = () =>
    render(
      <I18nextProvider i18n={i18n}>
        <ChatScreen />
      </I18nextProvider>
    );

  it("renderiza el título del chat", () => {
    const { getByText } = renderWithI18n();
    expect(getByText(i18n.t("chat.title"))).toBeTruthy();
  });

  it("envía un mensaje del usuario y lo muestra en pantalla", async () => {
    const { getByPlaceholderText, getByText } = renderWithI18n();

    const input = getByPlaceholderText(i18n.t("chat.inputPlaceholder"));
    fireEvent.changeText(input, "Hola N.O.V.A");
    fireEvent.press(getByText(i18n.t("chat.send")));

    expect(getByText("Hola N.O.V.A")).toBeTruthy();
  });

  it("simula respuesta automática del agente IA", async () => {
    const { getByPlaceholderText, getByText, findByText } = renderWithI18n();

    const input = getByPlaceholderText(i18n.t("chat.inputPlaceholder"));
    fireEvent.changeText(input, "¿Cómo estás?");
    fireEvent.press(getByText(i18n.t("chat.send")));

    // Espera la respuesta automática del agente
    const agentReply = await waitFor(() => findByText(i18n.t("chat.agentReply")));
    expect(agentReply).toBeTruthy();
  });
});
