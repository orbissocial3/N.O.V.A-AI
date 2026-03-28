/**
 * validator.js
 * ----------------------------
 * Utilidades de validación para N.O.V.A
 * - Emails
 * - Contraseñas
 * - Nombres de usuario
 * - Tarjetas de crédito
 * - Campos vacíos
 */

export const isEmailValid = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(String(email).toLowerCase());
};

export const isPasswordValid = (password) => {
  // Al menos 6 caracteres, una mayúscula, una minúscula y un número
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$/;
  return regex.test(password);
};

export const isUsernameValid = (username) => {
  // Solo letras, números y guiones bajos, entre 3 y 20 caracteres
  const regex = /^[a-zA-Z0-9_]{3,20}$/;
  return regex.test(username);
};

export const isCreditCardValid = (cardNumber) => {
  // Algoritmo de Luhn para validar tarjetas
  const sanitized = cardNumber.replace(/\D/g, "");
  let sum = 0;
  let shouldDouble = false;

  for (let i = sanitized.length - 1; i >= 0; i--) {
    let digit = parseInt(sanitized.charAt(i), 10);

    if (shouldDouble) {
      digit *= 2;
      if (digit > 9) digit -= 9;
    }

    sum += digit;
    shouldDouble = !shouldDouble;
  }

  return sum % 10 === 0;
};

export const isEmpty = (value) => {
  return !value || value.trim().length === 0;
};
