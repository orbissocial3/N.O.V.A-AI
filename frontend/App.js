/**
 * App.js
 * ----------------------------
 * Punto de entrada principal de la aplicación móvil N.O.V.A.
 * Inicializa:
 *  - Navegación global con React Navigation
 *  - Estado global con UserContext
 *  - Pantalla de carga inicial (Splash)
 *  - Manejo de sesión y autenticación
 *  - Configuración de idioma/tema con i18n y persistencia
 *  - Observabilidad con logging y monitoreo
 *  - Flujo de aceptación de Política de Privacidad
 */

import React, { useEffect, useState } from "react";
import { NavigationContainer, DefaultTheme, DarkTheme } from "@react-navigation/native";
import { StatusBar } from "expo-status-bar";
import { ActivityIndicator, View, StyleSheet, Text } from "react-native";
import NetInfo from "@react-native-community/netinfo";
import AsyncStorage from "@react-native-async-storage/async-storage";

// Contexto global de usuario
import { UserProvider } from "./context/UserContext";

// Navegación principal
import AppNavigator from "./navigation/AppNavigator";

// Pantalla de Política de Privacidad
import PrivacyScreen from "./app/screens/PrivacyScreen";

// Servicios
import auth from "./services/auth"; // Manejo de login/logout
import api from "./services/api";   // Conexión al backend
import logger from "./services/logger"; // Logging centralizado

// Internacionalización
import "./i18n"; // Inicializa configuración de idiomas
import { useTranslation } from "react-i18next";

// Hook de preferencias
import { usePreferences } from "./hooks/usePreferences";

export default function App() {
  const { t } = useTranslation();
  const { theme } = usePreferences(); // obtenemos tema persistido

  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isOffline, setIsOffline] = useState(false);
  const [privacyAccepted, setPrivacyAccepted] = useState(null);

  useEffect(() => {
    // Detectar estado de red
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsOffline(!state.isConnected);
    });

    const initializeApp = async () => {
      try {
        // Revisar aceptación de política
        const accepted = await AsyncStorage.getItem("privacyAccepted");
        setPrivacyAccepted(accepted === "true");

        // Validar sesión
        const token = await auth.getToken();
        if (token) {
          const response = await api.get("/auth/validate", {
            headers: { Authorization: `Bearer ${token}` },
          });
          if (response.status === 200) {
            setIsAuthenticated(true);
          }
        }
      } catch (error) {
        logger.error("Error inicializando la app", error);
      } finally {
        setLoading(false);
      }
    };

    initializeApp();
    return () => unsubscribe();
  }, []);

  if (loading) {
    return (
      <View style={styles.loader}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text>{t("app.loading")}</Text>
      </View>
    );
  }

  if (isOffline) {
    return (
      <View style={styles.loader}>
        <Text style={styles.offlineText}>{t("app.offline")}</Text>
      </View>
    );
  }

  // Si no aceptó la política, mostrar PrivacyScreen
  if (privacyAccepted === false) {
    return <PrivacyScreen />;
  }

  return (
    <UserProvider>
      <NavigationContainer theme={theme === "dark" ? DarkTheme : DefaultTheme}>
        <StatusBar style={theme === "dark" ? "light" : "dark"} />
        <AppNavigator isAuthenticated={isAuthenticated} />
      </NavigationContainer>
    </UserProvider>
  );
}

const styles = StyleSheet.create({
  loader: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#FFF",
  },
  offlineText: {
    fontSize: 16,
    color: "#FF3B30",
    fontWeight: "bold",
  },
});
