// services/logger.js
import AsyncStorage from "@react-native-async-storage/async-storage";
import NetInfo from "@react-native-community/netinfo";
import axios from "axios";

const LOG_STORAGE_KEY = "NOVA_LOGS";
const LOG_SERVER = "http://127.0.0.1:8000/logs"; // Ajusta a tu backend real

// Función para obtener timestamp legible
const getTimestamp = () => new Date().toISOString();

// Guardar log en AsyncStorage
const saveLog = async (log) => {
  try {
    const existing = await AsyncStorage.getItem(LOG_STORAGE_KEY);
    const logs = existing ? JSON.parse(existing) : [];
    logs.push(log);
    await AsyncStorage.setItem(LOG_STORAGE_KEY, JSON.stringify(logs));
  } catch (err) {
    console.error("[LOGGER] Error guardando log en AsyncStorage", err);
  }
};

// Enviar logs al backend
const syncLogs = async () => {
  try {
    const existing = await AsyncStorage.getItem(LOG_STORAGE_KEY);
    if (!existing) return;

    const logs = JSON.parse(existing);
    if (logs.length === 0) return;

    await axios.post(LOG_SERVER, { logs });
    await AsyncStorage.removeItem(LOG_STORAGE_KEY);
    console.log("[LOGGER] Logs sincronizados con backend ✅");
  } catch (err) {
    console.error("[LOGGER] Error sincronizando logs con backend", err);
  }
};

// Suscribirse al estado de red para sincronizar cuando vuelva conexión
NetInfo.addEventListener((state) => {
  if (state.isConnected) {
    syncLogs();
  }
});

// API del logger
const logger = {
  info: async (msg, context = {}) => {
    const log = { level: "info", msg, context, timestamp: getTimestamp() };
    console.log("[INFO]", msg, context);
    await saveLog(log);
  },
  warn: async (msg, context = {}) => {
    const log = { level: "warn", msg, context, timestamp: getTimestamp() };
    console.warn("[WARN]", msg, context);
    await saveLog(log);
  },
  error: async (msg, err = {}, context = {}) => {
    const log = { level: "error", msg, error: err?.toString(), context, timestamp: getTimestamp() };
    console.error("[ERROR]", msg, err, context);
    await saveLog(log);
  },
  debug: async (msg, context = {}) => {
    const log = { level: "debug", msg, context, timestamp: getTimestamp() };
    console.debug("[DEBUG]", msg, context);
    await saveLog(log);
  },
  sync: syncLogs, // Permite forzar sincronización manual
};

export default logger;
