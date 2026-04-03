/**
 * AppNavigator.js
 * ----------------------------
 * Navegador principal de N.O.V.A
 * Premium, seguro y apasionado
 */

import React from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { NavigationContainer } from "@react-navigation/native";
import { StatusBar } from "react-native";

// Pantallas
import SplashScreen from "../screens/SplashScreen";
import LoginScreen from "../screens/LoginScreen";
import HomeScreen from "../screens/HomeScreen";
import ChatScreen from "../screens/ChatScreen";
import PlanScreen from "../screens/PlanScreen";
import SettingsScreen from "../screens/SettingsScreen";

const Stack = createNativeStackNavigator();

export default function AppNavigator({ isAuthenticated }) {
  return (
    <NavigationContainer>
      <StatusBar
        barStyle="light-content"
        backgroundColor="#0A0F2C"
        translucent={true}
      />
      <Stack.Navigator
        initialRouteName={isAuthenticated ? "Home" : "Splash"}
        screenOptions={{
          headerShown: false,
          animation: "fade",
          gestureEnabled: true,
          animationDuration: 500,
          contentStyle: { backgroundColor: "#0A0F2C" },
        }}
      >
        {/* Splash inicial */}
        <Stack.Screen name="Splash" component={SplashScreen} />

        {/* Autenticación */}
        {!isAuthenticated && (
          <>
            <Stack.Screen name="Login" component={LoginScreen} />
          </>
        )}

        {/* Principal */}
        {isAuthenticated && (
          <>
            <Stack.Screen name="Home" component={HomeScreen} />
            <Stack.Screen name="Chat" component={ChatScreen} />
            <Stack.Screen name="Plans" component={PlanScreen} />
            <Stack.Screen name="Settings" component={SettingsScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
