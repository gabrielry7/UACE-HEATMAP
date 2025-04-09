import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="Dashboard de Inversiones Antifrágiles", layout="wide")

# Título y descripción
st.title("Dashboard de Inversiones Antifrágiles en Escenarios de Crisis")
st.markdown("""
Este dashboard permite visualizar el comportamiento de diferentes clases de activos 
en escenarios de crisis global y cómo ciertas inversiones alternativas pueden beneficiarse 
de la volatilidad y la incertidumbre (concepto de antifragilidad).
""")

# Sidebar para controles
st.sidebar.header("Parámetros de Simulación")

# Selección de escenario
escenario = st.sidebar.selectbox(
    "Escenario de Crisis",
    ["Guerra en Ucrania", "Crisis Energética", "Cambio Climático", "Guerra Arancelaria"]
)

# Nivel de intensidad de la crisis
intensidad = st.sidebar.slider("Intensidad de la Crisis", 1, 10, 5)

# Horizonte temporal
horizonte = st.sidebar.slider("Horizonte Temporal (años)", 1, 10, 5)

# Asignación de activos
st.sidebar.header("Asignación de Activos (%)")
st.sidebar.markdown("Total debe sumar 100%")

col1, col2 = st.sidebar.columns(2)
with col1:
    tradicionales = st.number_input("Activos Tradicionales", 0, 100, 60)
with col2:
    alternativos = st.number_input("Activos Alternativos", 0, 100, 40)

# Verificar que suman 100%
total = tradicionales + alternativos
if total != 100:
    st.sidebar.error(f"La asignación total es {total}%. Debe ser 100%")

# Distribución de activos tradicionales
st.sidebar.subheader("Distribución de Activos Tradicionales")
acciones = st.sidebar.slider("Acciones", 0, 100, 50)
bonos = st.sidebar.slider("Bonos", 0, 100, 30)
efectivo = st.sidebar.slider("Efectivo", 0, 100, 20)

# Distribución de activos alternativos
st.sidebar.subheader("Distribución de Activos Alternativos")
materias_primas = st.sidebar.slider("Materias Primas", 0, 100, 25)
energia_renovable = st.sidebar.slider("Energía Renovable", 0, 100, 25)
oro = st.sidebar.slider("Oro", 0, 100, 20)
cripto = st.sidebar.slider("Criptomonedas", 0, 100, 15)
volatilidad = st.sidebar.slider("ETFs de Volatilidad", 0, 100, 15)

# Función para generar datos simulados
def generar_datos_simulados(escenario, intensidad, horizonte):
    # Fechas
    fechas = [datetime.now() + timedelta(days=i*30) for i in range(horizonte*12)]
    
    # Factores de impacto según escenario
    factores = {
        "Guerra en Ucrania": {
            "Acciones": -0.05 * (intensidad/10),
            "Bonos": -0.03 * (intensidad/10),
            "Efectivo": 0.01,
            "Materias Primas": 0.08 * (intensidad/10),
            "Energía Renovable": 0.05 * (intensidad/10),
            "Oro": 0.07 * (intensidad/10),
            "Criptomonedas": 0.02 * (intensidad/10),
            "ETFs de Volatilidad": 0.09 * (intensidad/10)
        },
        "Crisis Energética": {
            "Acciones": -0.04 * (intensidad/10),
            "Bonos": -0.02 * (intensidad/10),
            "Efectivo": 0.01,
            "Materias Primas": 0.09 * (intensidad/10),
            "Energía Renovable": 0.10 * (intensidad/10),
            "Oro": 0.04 * (intensidad/10),
            "Criptomonedas": 0.01 * (intensidad/10),
            "ETFs de Volatilidad": 0.07 * (intensidad/10)
        },
        "Cambio Climático": {
            "Acciones": -0.03 * (intensidad/10),
            "Bonos": -0.02 * (intensidad/10),
            "Efectivo": 0.00,
            "Materias Primas": 0.04 * (intensidad/10),
            "Energía Renovable": 0.12 * (intensidad/10),
            "Oro": 0.03 * (intensidad/10),
            "Criptomonedas": 0.02 * (intensidad/10),
            "ETFs de Volatilidad": 0.05 * (intensidad/10)
        },
        "Guerra Arancelaria": {
            "Acciones": -0.06 * (intensidad/10),  # Mayor impacto en acciones por disrupción comercial
            "Bonos": -0.01 * (intensidad/10),     # Impacto moderado en bonos
            "Efectivo": 0.02,                     # Mayor valor del efectivo por incertidumbre
            "Materias Primas": 0.03 * (intensidad/10),  # Impacto mixto en materias primas
            "Energía Renovable": 0.02 * (intensidad/10), # Impacto moderado en renovables
            "Oro": 0.08 * (intensidad/10),        # Mayor demanda de oro como refugio
            "Criptomonedas": 0.06 * (intensidad/10), # Potencial beneficio como alternativa a divisas
            "ETFs de Volatilidad": 0.10 * (intensidad/10) # Alto beneficio de volatilidad por incertidumbre
        }
    }
    
    # Rendimientos base mensuales con volatilidad
    datos = {}
    datos["Fecha"] = fechas
    
    activos = ["Acciones", "Bonos", "Efectivo", "Materias Primas", 
               "Energía Renovable", "Oro", "Criptomonedas", "ETFs de Volatilidad"]
    
    for activo in activos:
        base_return = factores[escenario][activo]
        volatilidad = 0.02  # Volatilidad base
        
        if activo == "Criptomonedas":
            volatilidad = 0.15  # Mayor volatilidad para cripto
        elif activo == "ETFs de Volatilidad":
            volatilidad = 0.10  # Alta volatilidad
        elif activo == "Acciones":
            volatilidad = 0.05
            
        # Ajuste específico para Guerra Arancelaria
        if escenario == "Guerra Arancelaria":
            if activo == "Acciones":
                volatilidad = 0.07  # Mayor volatilidad en acciones durante guerra comercial
        
        # Generar rendimientos con tendencia y volatilidad
        rendimientos = [1.0]
        for i in range(horizonte*12 - 1):
            rendimiento_mensual = base_return + np.random.normal(0, volatilidad)
            # Añadir autocorrelación para hacer los movimientos más realistas
            if rendimientos[-1] > 1:
                rendimiento_mensual += 0.01  # Momentum positivo
            else:
                rendimiento_mensual -= 0.01  # Momentum negativo
                
            # Añadir shocks aleatorios para Guerra Arancelaria (anuncios de nuevos aranceles)
            if escenario == "Guerra Arancelaria" and np.random.random() < 0.1:
                if activo == "Acciones":
                    rendimiento_mensual -= np.random.uniform(0, 0.05) * intensidad/5
                elif activo == "Oro":
                    rendimiento_mensual += np.random.uniform(0, 0.04) * intensidad/5
                
            nuevo_valor = rendimientos[-1] * (1 + rendimiento_mensual)
            rendimientos.append(nuevo_valor)
        
        datos[activo] = rendimientos
    
    return pd.DataFrame(datos)

# Generación de datos
df = generar_datos_simulados(escenario, intensidad, horizonte)

# Calcular los rendimientos de la cartera
def calcular_rendimiento_cartera():
    # Pesos de activos tradicionales
    peso_acciones = tradicionales * acciones / 100 / 100
    peso_bonos = tradicionales * bonos / 100 / 100
    peso_efectivo = tradicionales * efectivo / 100 / 100
    
    # Pesos de activos alternativos
    peso_materias = alternativos * materias_primas / 100 / 100
    peso_renovable = alternativos * energia_renovable / 100 / 100
    peso_oro = alternativos * oro / 100 / 100
    peso_cripto = alternativos * cripto / 100 / 100
    peso_volatilidad = alternativos * volatilidad / 100 / 100
    
    # Calcular rendimiento ponderado
    rendimiento_cartera = (
        df["Acciones"] * peso_acciones +
        df["Bonos"] * peso_bonos +
        df["Efectivo"] * peso_efectivo +
        df["Materias Primas"] * peso_materias +
        df["Energía Renovable"] * peso_renovable +
        df["Oro"] * peso_oro +
        df["Criptomonedas"] * peso_cripto +
        df["ETFs de Volatilidad"] * peso_volatilidad
    )
    
    # Agregar al dataframe
    df["Rendimiento Cartera"] = rendimiento_cartera
    
    # Calcular rendimiento tradicional (60/40)
    rendimiento_tradicional = df["Acciones"] * 0.6 + df["Bonos"] * 0.4
    df["Cartera Tradicional 60/40"] = rendimiento_tradicional
    
    return df

df = calcular_rendimiento_cartera()

# Contenido principal
st.header(f"Escenario: {escenario} (Intensidad: {intensidad}/10)")

# Métricas clave
col1, col2, col3 = st.columns(3)
with col1:
    rendimiento_total = (df["Rendimiento Cartera"].iloc[-1] / df["Rendimiento Cartera"].iloc[0] - 1) * 100
    st.metric("Rendimiento Total", f"{rendimiento_total:.2f}%")
with col2:
    rendimiento_tradicional = (df["Cartera Tradicional 60/40"].iloc[-1] / df["Cartera Tradicional 60/40"].iloc[0] - 1) * 100
    st.metric("Rendimiento Cartera 60/40", f"{rendimiento_tradicional:.2f}%")
with col3:
    diferencia = rendimiento_total - rendimiento_tradicional
    st.metric("Diferencia vs 60/40", f"{diferencia:.2f}%", delta=f"{diferencia:.2f}%")

# Gráficos
st.subheader("Evolución del Rendimiento")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Fecha"], y=df["Rendimiento Cartera"], 
                         mode='lines', name='Tu Cartera Antifrágil'))
fig.add_trace(go.Scatter(x=df["Fecha"], y=df["Cartera Tradicional 60/40"], 
                         mode='lines', name='Cartera Tradicional 60/40'))
fig.update_layout(xaxis_title="Fecha", yaxis_title="Valor (base=1)", height=500)
st.plotly_chart(fig, use_container_width=True)

# Rendimiento por Activo
st.subheader("Rendimiento por Clase de Activo")
fig2 = go.Figure()
activos = ["Acciones", "Bonos", "Efectivo", "Materias Primas", 
          "Energía Renovable", "Oro", "Criptomonedas", "ETFs de Volatilidad"]
for activo in activos:
    fig2.add_trace(go.Scatter(x=df["Fecha"], y=df[activo], mode='lines', name=activo))
fig2.update_layout(xaxis_title="Fecha", yaxis_title="Valor (base=1)", height=500)
st.plotly_chart(fig2, use_container_width=True)

# Correlación entre activos
st.subheader("Matriz de Correlación")
corr = df[activos].corr()
fig3 = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r',
                aspect="auto", height=500)
st.plotly_chart(fig3, use_container_width=True)

# Composición de la cartera
st.subheader("Composición de la Cartera")
# Datos para el gráfico de composición
comp_data = {
    'Clase': ['Acciones', 'Bonos', 'Efectivo', 'Materias Primas', 
              'Energía Renovable', 'Oro', 'Criptomonedas', 'ETFs de Volatilidad'],
    'Valor': [
        tradicionales * acciones / 100 / 100, 
        tradicionales * bonos / 100 / 100, 
        tradicionales * efectivo / 100 / 100,
        alternativos * materias_primas / 100 / 100,
        alternativos * energia_renovable / 100 / 100,
        alternativos * oro / 100 / 100,
        alternativos * cripto / 100 / 100,
        alternativos * volatilidad / 100 / 100
    ]
}
df_comp = pd.DataFrame(comp_data)
fig4 = px.pie(df_comp, values='Valor', names='Clase', height=400)
st.plotly_chart(fig4, use_container_width=True)

# Indicador de Antifragilidad
st.subheader("Indicador de Antifragilidad")
# Calcular correlación con intensidad
# Simulamos datos de intensidad escalonados
intensidad_escalada = [intensidad * (i/10) for i in range(1, horizonte*12+1)]
intensidad_escalada = intensidad_escalada[:len(df)]
df["Intensidad Crisis"] = intensidad_escalada

# Calcular correlación con rendimiento para medir antifragilidad
corr_antifragilidad = np.corrcoef(intensidad_escalada, df["Rendimiento Cartera"])[0,1]
nivel_antifragilidad = corr_antifragilidad * 100

# Crear un indicador visual
fig5 = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = nivel_antifragilidad,
    title = {'text': "Índice de Antifragilidad"},
    gauge = {
        'axis': {'range': [-100, 100]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [-100, -50], 'color': "red"},
            {'range': [-50, 0], 'color': "orange"},
            {'range': [0, 50], 'color': "lightgreen"},
            {'range': [50, 100], 'color': "green"}
        ],
        'threshold': {
            'line': {'color': "black", 'width': 4},
            'thickness': 0.75,
            'value': nivel_antifragilidad
        }
    }
))
fig5.update_layout(height=300)
st.plotly_chart(fig5, use_container_width=True)

# Explicación del índice de antifragilidad
st.info("""
**Índice de Antifragilidad**: Mide cómo se comporta la cartera cuando aumenta la intensidad de la crisis.
- Valores negativos: La cartera sufre con la crisis (frágil)
- Valores cercanos a cero: La cartera resiste la crisis (robusta)
- Valores positivos: La cartera se beneficia de la crisis (antifrágil)
""")

# Recomendaciones dinámicas
st.header("Recomendaciones Estratégicas")

# Recomendaciones basadas en el escenario
recomendaciones = {
    "Guerra en Ucrania": [
        "Aumentar exposición a oro y materias primas",
        "Reducir exposición a bonos de países cercanos al conflicto", 
        "Considerar inversiones en defensa y ciberseguridad",
        "Diversificar geográficamente hacia mercados alejados del conflicto"
    ],
    "Crisis Energética": [
        "Aumentar inversión en energías renovables y tecnologías de almacenamiento",
        "Exposición selectiva a empresas con baja intensidad energética",
        "Considerar opciones sobre futuros energéticos como cobertura",
        "Inversión en empresas de eficiencia energética y redes inteligentes"
    ],
    "Cambio Climático": [
        "Aumentar exposición a empresas de tecnología verde y economía circular",
        "Inversión en agricultura sostenible y gestión del agua",
        "Reducir exposición a activos con alto riesgo climático (inmuebles en zonas costeras)",
        "Considerar bonos verdes y de impacto social como alternativa a bonos tradicionales"
    ],
    "Guerra Arancelaria": [
        "Preferir empresas con cadenas de suministro diversificadas o domésticas",
        "Exposición a sectores menos dependientes del comercio internacional",
        "Considerar oro y criptomonedas como protección contra volatilidad en divisas",
        "Inversión en ETFs de volatilidad como cobertura táctica",
        "Explorar oportunidades en empresas de logística y automatización adaptables"
    ]
}

for rec in recomendaciones[escenario]:
    st.markdown(f"- {rec}")

# Análisis específico para Guerra Arancelaria
if escenario == "Guerra Arancelaria":
    st.subheader("Impacto Sectorial de la Guerra Arancelaria")
    
    # Crear datos simulados de impacto sectorial
    sectores = ["Tecnología", "Consumo Básico", "Salud", "Industria", "Materiales", "Financiero"]
    impacto_data = {
        'Sector': sectores,
        'Impacto': [
            -0.08 * intensidad/10,  # Tecnología (muy afectada)
            -0.03 * intensidad/10,  # Consumo Básico (menos afectado)
            -0.02 * intensidad/10,  # Salud (menos afectado)
            -0.07 * intensidad/10,  # Industria (muy afectada)
            -0.06 * intensidad/10,  # Materiales (afectado)
            -0.04 * intensidad/10   # Financiero (moderadamente afectado)
        ]
    }
    
    df_impacto = pd.DataFrame(impacto_data)
    df_impacto['Impacto'] = df_impacto['Impacto'] * 100  # Convertir a porcentaje
    
    # Gráfico de barras de impacto sectorial
    fig6 = px.bar(df_impacto, x='Sector', y='Impacto', 
                 title=f"Impacto Estimado por Sector (Intensidad: {intensidad}/10)",
                 labels={'Impacto': 'Impacto Estimado (%)'})
    fig6.update_layout(height=400)
    st.plotly_chart(fig6, use_container_width=True)
    
    # Añadir información específica sobre guerra arancelaria
    st.markdown("""
    ### Consideraciones Específicas sobre Guerra Arancelaria
    
    Las tensiones comerciales y guerras arancelarias tienen impactos asimétricos en diferentes sectores y regiones:
    
    1. **Disrupciones en cadenas de suministro**: Las empresas con cadenas de suministro globales complejas suelen ser más vulnerables
    
    2. **Volatilidad en divisas**: Los movimientos arancelarios frecuentemente provocan volatilidad en los tipos de cambio
    
    3. **Oportunidades en producción local**: Empresas con producción doméstica pueden beneficiarse de la protección arancelaria
    
    4. **Cambios en patrones de comercio**: Se crean nuevas rutas y relaciones comerciales para evitar aranceles
    
    5. **Innovación acelerada**: La presión económica puede estimular la búsqueda de alternativas y soluciones innovadoras
    """)

st.markdown("""
### Consideraciones Sobre Antifragilidad

La antifragilidad va más allá de la resiliencia; significa que la cartera no solo resiste la volatilidad,
sino que potencialmente se beneficia de ella. Este dashboard permite explorar estrategias de inversión
que podrían capitalizar escenarios de crisis mediante:

1. **Asimetrías positivas**: Activos que tienen potencial de ganancia desproporcionado en situaciones de estrés
2. **Optimalidad convexa**: Combinaciones de activos muy seguros con otros de alto riesgo/recompensa
3. **Exposición a la volatilidad**: Instrumentos que se benefician directamente del aumento de la incertidumbre
""")

# Nota final
st.caption("Nota: Este es un modelo simplificado con datos simulados. Las proyecciones no representan rendimientos reales y no deben utilizarse para tomar decisiones de inversión.")