
# 💧 Sistema Experto Difuso de Riesgo Hídrico Municipal

Trabajo Integrador Final para la Tecnicatura en Ciencia de Datos e IA Aplicada (UPATECO).

## 📋 Descripción del Proyecto
Este sistema es un motor de inferencia basado en **Lógica Difusa** diseñado para evaluar el **Riesgo Hídrico Urbano** a nivel municipal. El sistema analiza variables ambientales, topográficas y meteorológicas críticas para predecir escenarios de inundación o amenazas climáticas, permitiendo a los municipios tomar decisiones preventivas y activar protocolos de emergencia.

## 🚀 Acceso a la Aplicación Interactiva (Avance 3)
Para facilitar la evaluación de la cátedra sin requerir configuraciones ni instalaciones locales complejas, la aplicación interactiva con la interfaz gráfica se encuentra desplegada y funcionando de forma 100% online.

👉 **[HACÉ CLIC AQUÍ PARA ABRIR LA APP EN VIVO](https://sistemadifusoriesgoinundacion-dfvty3nzurybz8idunj2ws.streamlit.app/)**

---

## 📊 Arquitectura del Sistema Experto

### 1. Variables de Entrada (Antecedentes)
* **Precipitación acumulada (Lluvia):** Rango de 0 a 120 mm (Baja, Media, Alta, Crítica).
* **Humedad del suelo:** Rango de 0% a 100% (Seca, Media, Saturada).
* **Capacidad de drenaje:** Rango de 0% a 100% (Bajo, Medio, Alto).
* **Nivel de alerta meteorológica:** Escala de 0 a 3 (Sin Alerta, Moderada, Fuerte, Crítica).
* **Pendiente topográfica:** Rango de 0% a 10% (Llana, Moderada, Empinada).

### 2. Variable de Salida (Consecuente)
* **Riesgo Hídrico:** Escala difusa de 0.0 a 1.0, clasificada en los niveles:
  * **Bajo** (< 0.3)
  * **Medio** (0.3 a 0.6)
  * **Alto** (0.6 a 0.8)
  * **Crítico** (> 0.8)

---

## 🛠️ Stack Tecnológico Utilizado
* **Lenguaje principal:** Python 3.11
* **Lógica de IA:** `scikit-fuzzy`
* **Modelado de Redes Internas:** `networkx`
* **Cálculo Matemático y Datos:** `numpy` y `pandas`
* **Interfaz Gráfica y Despliegue Cloud:** `streamlit`

---

## 👥 Equipo de Trabajo
* **Grupo 16**
