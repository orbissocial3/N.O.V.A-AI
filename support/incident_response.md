# N.O.V.A - Plan de Respuesta a Incidentes

---

## Objetivos
- Detectar, contener y resolver incidentes de seguridad o disponibilidad.
- Minimizar impacto en usuarios y operaciones.
- Documentar y aprender de cada incidente.

---

## Clasificación de Incidentes
- **Críticos**: caída total del servicio, fuga de datos.
- **Altos**: degradación significativa del rendimiento, errores en autenticación.
- **Medios**: fallos en módulos específicos, problemas de integración.
- **Bajos**: bugs menores, errores visuales.

---

## Protocolo de Respuesta
1. **Detección**  
   - Alertas automáticas (Prometheus, Tracing, Logs).
   - Reportes de usuarios vía soporte.

2. **Contención**  
   - Aislar servicios afectados.
   - Activar redundancia o fallback.

3. **Resolución**  
   - Aplicar fix o rollback.
   - Validar integridad de datos.

4. **Comunicación**  
   - Notificar a usuarios vía correo y dashboard de estado.
   - Informar a equipo interno con detalles técnicos.

5. **Postmortem**  
   - Documentar causa raíz.
   - Definir acciones preventivas.
   - Actualizar protocolos y monitoreo.

---

## Roles y Responsabilidades
- **Incident Manager**: coordina respuesta y comunicación.
- **DevOps**: ejecuta contención y despliegues.
- **Security Officer**: valida impacto en datos.
- **Support Team**: comunica con usuarios.

---

## Tiempo de Respuesta Objetivo (SLA)
- Críticos: < 50 minutos.
- Altos: < 3 horas.
- Medios: < 48 horas.
- Bajos: < 72 horas.
