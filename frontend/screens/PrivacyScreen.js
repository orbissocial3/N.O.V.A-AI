import React, { useState } from 'react';
import { SafeAreaView, ScrollView, Text, Button } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function PrivacyScreen({ navigation }) {
  const [accepted, setAccepted] = useState(false);

  const handleAccept = async () => {
    await AsyncStorage.setItem('privacyAccepted', 'true');
    setAccepted(true);
    navigation.replace('Home'); // redirige al inicio de la app
  };

  return (
    <SafeAreaView style={{ flex: 1, padding: 20 }}>
      <ScrollView>
        <Text style={{ fontSize: 22, fontWeight: 'bold', marginBottom: 15 }}>
          Política de Privacidad
        </Text>
        <Text style={{ fontSize: 16, marginBottom: 20 }}>
<Text> 📜 Documento Legal – N.O.V.A </Text>
Última actualización: Marzo 2026
<Text1>. Política de Privacidad</Text1>
<Text>1.1 Introducción</Text>
N.O.V.A respeta la privacidad de sus usuarios y se compromete a proteger la información personal.
<Text>1.2 Datos almacenados</Text>
Usuarios individuales:

Historial de chats: almacenado en la cuenta de Google del usuario (retención 30 días).
Recordatorios y agendas: guardados en caché de la cuenta de Google.
Configuraciones (modo oscuro/claro, idioma, accesibilidad): almacenadas en la cuenta del usuario.

Empresas clientes (plan empresarial):

N.O.V.A solo almacena:
- Número de empresas que usan el servicio.
- Cantidad de horas dedicadas al uso de la plataforma.

El contenido de chats empresariales y agendas internas no es accesible por N.O.V.A, solo por la empresa cliente.
Datos de pago: procesados por terceros (PayPal, Stripe).
Comprobantes: enviados por Gmail.
1.3 Uso de la información
- Proporcionar servicios de IA según el plan contratado.
- Generar reportes empresariales para administradores.
- Garantizar seguridad y auditoría.
1.4 Seguridad
- Cifrado end-to-end en segundo plano.
- Almacenamiento seguro en Azure.
- Acceso restringido en cuentas empresariales.
1.5 Derechos del usuario
- Activar modo incógnito para no guardar historial.
- Cancelar o modificar plan.
- Solicitar eliminación de datos según normativa aplicable.
2. Términos y Condiciones de Uso
2.1 Aceptación
Al usar N.O.V.A, el usuario acepta estos términos.
2.2 Planes
Free: acceso limitado a agentes básicos.
Premium: acceso a agentes avanzados (Creativo, Inversor, Secretario completo).
Empresarial: funciones compartidas, reportes, panel de administración.
2.3 Limitaciones
- La IA ofrece sugerencias, no ejecuta trading ni garantiza resultados financieros.
- Prohibido uso ilegal.
- Chats cifrados solo accesibles por la cuenta propietaria.
2.4 Responsabilidad empresarial
- El administrador puede suspender/eliminar usuarios.
- Reportes de productividad son informativos, no evaluaciones laborales oficiales.
2.5 Propiedad intelectual
- Logo, marca y código son propiedad exclusiva de N.O.V.A.
- Prohibida copia, modificación o distribución sin autorización.
3. Política de Pagos y Reembolsos
3.1 Métodos de pago
PayPal, Stripe. 
3.2 Renovación
Manual, no automática.
3.3 Comprobantes
Enviados por Gmail tras cada pago.
3.4 Reembolsos – Planes personales (Free/Premium)
0–24h: reembolso del 100%.
24–72h: reembolso del 50%.
72–96h: reembolso del 15%.
Después de 96h: no hay reembolso permitido.
3.5 Reembolsos – Plan empresarial
0–24h: reembolso del 30%.
Después de 24h: no hay reembolso permitido.
4. Acuerdo de Licencia de Usuario Final (EULA)
4.1 Licencia
Se otorga al usuario una licencia limitada, no exclusiva, para usar N.O.V.A.
4.2 Restricciones
- No modificar, copiar ni distribuir el software.
- No usar para fines ilegales.
4.3 Propiedad intelectual
Todo el contenido, logo y código son propiedad de N.O.V.A.
4.4 Limitación de responsabilidad
N.O.V.A no garantiza resultados financieros ni académicos.
El uso de la app es bajo responsabilidad del usuario.
5. Política de Contenido Generado
5.1 Introducción
N.O.V.A permite a los usuarios generar contenido mediante inteligencia artificial. Para garantizar un entorno seguro y legal, se establecen las siguientes reglas.
5.2 Contenido prohibido
- Contenido sexual explícito o +18.
- Contenido relacionado con drogas ilegales.
- Violencia explícita o gore.
- Discurso de odio o discriminación.
- Actividades ilegales.
- Información médica peligrosa sin respaldo profesional.
5.3 Contenido restringido
Permitido solo en contextos:
- Educativos (historia, medicina, ciencia).
- Artísticos (referencias figurativas o metafóricas).
- Profesionales (debates sobre políticas públicas o leyes).
5.4 Moderación y cumplimiento
- N.O.V.A podrá suspender o eliminar cuentas que generen contenido prohibido.
- Administradores empresariales podrán establecer filtros adicionales.
- El sistema de auditoría registrará intentos de generar contenido prohibido.
5.5 Responsabilidad del usuario
El usuario es responsable del contenido que genere.
N.O.V.A no se hace responsable de daños derivados del uso indebido de la aplicación.
6. Aviso Legal
6.1 Naturaleza del servicio
N.O.V.A es una herramienta de inteligencia artificial diseñada para asistir en tareas de productividad, creatividad y gestión empresarial.
6.2 Limitación de responsabilidad
N.O.V.A no sustituye asesoría profesional en áreas financieras, médicas, legales o académicas.
El contenido generado es orientativo y no debe considerarse consejo definitivo.
El usuario es responsable de verificar la información antes de tomar decisiones críticas.
6.3 Jurisdicción
Este aviso se rige por las leyes del país donde se comercializa el servicio.
7. Política de Seguridad y Accesibilidad
7.1 Seguridad
- Todos los datos se almacenan en servidores seguros (Azure).
- Se aplica cifrado end-to-end en segundo plano.
- Acceso restringido a datos empresariales, solo para administradores autorizados.
7.2 Accesibilidad
- Compatibilidad con lectores de pantalla.
- Opciones de contraste y modo oscuro/claro.
- Configuración de idioma adaptable.
- Compromiso de mejora continua para cumplir estándares internacionales de accesibilidad (WCAG).
8. Política de Soporte
8.1 Canales de contacto
- Correo electrónico oficial de soporte.
- Formulario dentro de la aplicación.
8.2 Tiempos de respuesta
- Consultas generales: entre 24 y 72 horas hábiles.
- Incidencias críticas (fallos de acceso, problemas de pago): prioridad máxima, respuesta en menos de 24 horas.
8.3 Procedimiento de reclamaciones
El usuario debe enviar una descripción detallada del problema.
N.O.V.A evaluará la incidencia y ofrecerá solución o compensación según corresponda.
9. Política de Actualizaciones
9.1 Cambios en el servicio
N.O.V.A podrá actualizar funciones, planes y precios.
Los cambios se comunicarán mediante notificación en la aplicación o correo electrónico.
9.2 Cambios en las políticas
Las políticas de privacidad, uso y reembolsos podrán actualizarse para cumplir con nuevas normativas.
El usuario será notificado de cualquier cambio relevante.
9.3 Continuidad del servicio
El uso continuado de N.O.V.A tras una actualización implica aceptación de los nuevos términos.
10. Política de Permisos Android
10.1 Permisos solicitados
La aplicación N.O.V.A solicita los siguientes permisos:
- Almacenamiento: guardar y recuperar chats, agendas y configuraciones.
- Cámara: capturar imágenes para uso en agentes o funciones empresariales.
- Galería: subir imágenes desde el dispositivo.
- Configuraciones del sistema: ajustar idioma, modo oscuro/claro y accesibilidad.
- Otros permisos necesarios: se solicitarán únicamente para funciones esenciales de la app.
10.2 Justificación
Cada permiso se solicita exclusivamente para garantizar el correcto funcionamiento de la aplicación y nunca para fines externos o comerciales.
11. Política de Retención de Datos Empresariales
N.O.V.A almacena únicamente:
- Número de empresas que usan el servicio.
- Cantidad de horas dedicadas al uso de la plataforma.

Estos datos se conservan mientras la cuenta empresarial esté activa.
Al eliminar la cuenta, los datos se eliminan de forma definitiva.
12. Política de Cierre de Servicio
En caso de que N.O.V.A deje de operar, se notificará a los usuarios con al menos 30 días de antelación.
Durante ese período, los usuarios podrán descargar sus datos personales y empresariales.
Una vez cerrado el servicio, todos los datos serán eliminados de forma definitiva.
13. Política de Propiedad de Datos
Los datos personales y empresariales generados en N.O.V.A son propiedad exclusiva del usuario o empresa cliente.
N.O.V.A solo provee la infraestructura para su almacenamiento y gestión.
N.O.V.A no explota, comercializa ni comparte los datos con terceros, salvo lo estrictamente necesario para procesar pagos o cumplir con la ley.

        </Text>
      </ScrollView>
      <Button title="Acepto" onPress={handleAccept} />
    </SafeAreaView>
  );
}
