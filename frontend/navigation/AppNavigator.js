/**
 * AppNavigator.js
 * ----------------------------
 * Navegador principal de la aplicación N.O.V.A
 * - Splash inicial con animación premium
 * - Stack de autenticación (Login, Registro, Recuperar contraseña)
 * - Stack principal (Home, Chat, Planes, Configuración)
 * - Redirección según estado de sesión
 * - Transiciones empresariales y fluidas
 */

import React from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

// Pantallas de autenticación
import LoginScreen from "../screens/LoginScreen";
// Preparado para expansión futura
// import RegisterScreen from "../screens/RegisterScreen";
// import ForgotPasswordScreen from "../screens/ForgotPasswordScreen";

// Pantallas principales
import HomeScreen from "../screens/HomeScreen";
import ChatScreen from "../screens/ChatScreen";
import PlanScreen from "../screens/PlanScreen";
import SettingsScreen from "../screens/SettingsScreen";
import SplashScreen from "../screens/SplashScreen";

const Stack = createNativeStackNavigator();

export default function AppNavigator({ isAuthenticated }) {
  return (
    <Stack.Navigator
      initialRouteName={isAuthenticated ? "Home" : "Splash"}
      screenOptions={{
        headerShown: false,
        animation: "fade", // transición premium
        gestureEnabled: true, // gestos fluidos
        animationDuration: 500, // velocidad elegante
      }}
    >
      {/* Pantalla inicial de carga */}
      <Stack.Screen name="Splash" component={SplashScreen} />

      {/* Stack de autenticación */}
      {!isAuthenticated && (
        <>
          <Stack.Screen name="Login" component={LoginScreen} />
          {/* Preparado para crecer */}
          {/* <Stack.Screen name="Register" component={RegisterScreen} /> */}
          {/* <Stack.Screen name="ForgotPassword" component={ForgotPasswordScreen} /> */}
        </>
      )}

      {/* Stack principal */}
      {isAuthenticated && (
        <>
          <Stack.Screen name="Home" component={HomeScreen} />
          <Stack.Screen name="Chat" component={ChatScreen} />
          <Stack.Screen name="Plans" component={PlanScreen} />
          <Stack.Screen name="Settings" component={SettingsScreen} />
        </>
      )}
    </Stack.Navigator>
  );
}
