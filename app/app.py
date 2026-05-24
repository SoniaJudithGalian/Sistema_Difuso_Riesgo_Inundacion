
# --- PARCHE DE COMPATIBILIDAD OBLIGATORIO PARA SCIPY ---
import sys
import scipy
if not hasattr(scipy, 'linalg'):
    import scipy.linalg
    sys.modules['scipy.linalg'] = scipy.linalg
# ------------------------------------------------------

import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Configuración de la página web
st.set_page_config(page_title="RiesgoHídrico - Control Municipal", layout="centered")

st.title("💧 Sistema Experto Difuso de Riesgo Hídrico Municipal")
st.write("Evaluación del riesgo hídrico urbano utilizando motores de inferencia de lógica difusa.")

# --- Inicialización del Motor Difuso en Caché ---
@st.cache_resource
def inicializar_sistema_difuso():
    lluvia = ctrl.Antecedent(np.arange(0, 121, 1), 'lluvia')       
    humedad = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad')     
    drenaje = ctrl.Antecedent(np.arange(0, 101, 1), 'drenaje')     
    alerta = ctrl.Antecedent(np.arange(0, 4, 1), 'alerta')         
    pendiente = ctrl.Antecedent(np.arange(0, 11, 1), 'pendiente')  
    
    riesgo = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'riesgo')     

    # Funciones de pertenencia exactas del notebook
    lluvia['baja'] = fuzz.trimf(lluvia.universe, [0, 0, 30])       
    lluvia['media'] = fuzz.trimf(lluvia.universe, [20, 50, 60])    
    lluvia['alta'] = fuzz.trimf(lluvia.universe, [50, 90, 100])    
    lluvia['critica'] = fuzz.trapmf(lluvia.universe, [90, 100, 120, 120]) 

    humedad['seca'] = fuzz.trimf(humedad.universe, [0, 0, 35])     
    humedad['media'] = fuzz.trimf(humedad.universe, [25, 50, 70])  
    humedad['saturada'] = fuzz.trimf(humedad.universe, [60, 100, 100]) 

    drenaje['bajo'] = fuzz.trimf(drenaje.universe, [0, 0, 40])     
    drenaje['medio'] = fuzz.trimf(drenaje.universe, [30, 50, 70])  
    drenaje['alto'] = fuzz.trimf(drenaje.universe, [60, 100, 100]) 

    alerta['sin'] = fuzz.trimf(alerta.universe, [0, 0, 0])         
    alerta['moderada'] = fuzz.trimf(alerta.universe, [1, 1, 1])    
    alerta['fuerte'] = fuzz.trimf(alerta.universe, [2, 2, 2])      
    alerta['critica'] = fuzz.trimf(alerta.universe, [3, 3, 3])     

    pendiente['llana'] = fuzz.trimf(pendiente.universe, [0, 0, 2.5])   
    pendiente['moderada'] = fuzz.trimf(pendiente.universe, [2, 5, 5.5])
    pendiente['empinada'] = fuzz.trimf(pendiente.universe, [5, 10, 10])

    riesgo['bajo'] = fuzz.trimf(riesgo.universe, [0, 0, 0.3])      
    riesgo['medio'] = fuzz.trimf(riesgo.universe, [0.2, 0.5, 0.6]) 
    riesgo['alto'] = fuzz.trimf(riesgo.universe, [0.5, 0.7, 0.9])  
    riesgo['critico'] = fuzz.trimf(riesgo.universe, [0.8, 1, 1])   

    # --- BASE DE REGLAS MEJORADA Y COMPLETADA ---
    reglas = [
        ctrl.Rule(lluvia['alta'] & drenaje['bajo'], riesgo['critico']),   
        ctrl.Rule(alerta['fuerte'] & humedad['saturada'], riesgo['alto']),
        ctrl.Rule(lluvia['media'] & drenaje['medio'], riesgo['medio']),   
        ctrl.Rule(lluvia['baja'] & drenaje['alto'], riesgo['bajo']),      
        ctrl.Rule(alerta['critica'], riesgo['critico']),                  
        ctrl.Rule(pendiente['empinada'] & lluvia['alta'], riesgo['alto']),
        
        # Nuevas reglas para solucionar las inconsistencias de valores extremos:
        ctrl.Rule(lluvia['critica'], riesgo['critico']), # Si la lluvia es crítica, el riesgo SIEMPRE es crítico
        ctrl.Rule(lluvia['alta'] & humedad['saturada'], riesgo['critico']), # Lluvia alta con suelo saturado colapsa el drenaje
        ctrl.Rule(lluvia['media'] & drenaje['bajo'], riesgo['alto']) # Lluvia media en zona sin drenaje es peligroso
    ]
    
    sc = ctrl.ControlSystem(reglas)
    return ctrl.ControlSystemSimulation(sc)

# Inicializar simulación
sistema = inicializar_sistema_difuso()

# --- Interfaz de Controles ---
st.sidebar.header("Parámetros del Municipio")
lluvia_input = st.sidebar.slider("Precipitación acumulada (mm)", 0, 120, 55) 
humedad_input = st.sidebar.slider("Humedad del suelo (%)", 0, 100, 65)       
drenaje_input = st.sidebar.slider("Capacidad de drenaje (%)", 0, 100, 55)    
pendiente_input = st.sidebar.slider("Pendiente topográfica (%)", 0, 10, 5)   

alerta_input = st.sidebar.selectbox(
    "Nivel de alerta meteorológica", 
    [0, 1, 2, 3],         
    format_func=lambda x: ["Sin alerta", "Moderada", "Fuerte", "Crítica"][x],
    index=0
)

# Asignar valores al sistema difuso
sistema.input['lluvia'] = lluvia_input
sistema.input['humedad'] = humedad_input
sistema.input['drenaje'] = drenaje_input
sistema.input['alerta'] = alerta_input
sistema.input['pendiente'] = pendiente_input

# Procesar la inferencia
try:
    sistema.compute()
    riesgo_valor = sistema.output['riesgo']
except:
    riesgo_valor = 0.5

st.subheader("💡 Recomendación del Sistema")

# Clasificación según los umbrales de tu Colab
if riesgo_valor < 0.3:
    nivel = "Bajo"
    st.success(f"🔎 Nivel estimado de riesgo: {nivel} (Valor difuso: {riesgo_valor:.2f})")
    st.info("El sistema municipal se encuentra en condiciones seguras y estables.")
elif riesgo_valor < 0.6:
    nivel = "Medio"
    st.warning(f"🔎 Nivel estimado de riesgo: {nivel} (Valor difuso: {riesgo_valor:.2f})")
    st.info("Monitoreo preventivo aconsejado en zonas bajas o cuencas vulnerables.")
elif riesgo_valor < 0.8:
    nivel = "Alto"
    st.error(f"🔎 Nivel estimado de riesgo: {nivel} (Valor difuso: {riesgo_valor:.2f})")
    st.error("Alerta: Se recomienda preparar sistemas de bombeo y activar protocolos de contingencia.")
else:
    nivel = "Crítico"
    st.error(f"🚨 Nivel estimado de riesgo: {nivel} (Valor difuso: {riesgo_valor:.2f})")
    st.sidebar.warning("¡ESTADO DE EMERGENCIA ACTIVADO!")

# Barra de progreso visual
st.progress(float(riesgo_valor))
