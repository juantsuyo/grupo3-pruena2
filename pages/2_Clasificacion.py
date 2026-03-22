import streamlit as st
import pandas as pd
import numpy as np
import base64

from joblib import load

st.set_page_config(page_title="Clasificacion", page_icon=":trophy:", initial_sidebar_state="expanded")

@st.cache_data
def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def build_markup_for_logo(
    png_file,
    background_position="50% 10%",
    margin_top="5%",
    image_width="20%",
    image_height="",
):
    binary_string = get_base64_of_bin_file(png_file)
    return """
            <style>
                [data-testid="stSidebarHeader"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    background-position: %s;
                    margin-top: %s;
                    background-size: %s %s;
                }
            </style>
            """ % (
        binary_string,
        background_position,
        margin_top,
        image_width,
        image_height,
    )


def add_logo(png_file):
    logo_markup = build_markup_for_logo(png_file)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )

add_logo("files/images1.png")




MODEL_PATH = "rf_tuneado.joblib"

@st.cache_resource
def load_model():
    return load(MODEL_PATH)

try:
    model = load(MODEL_PATH)
except Exception as e:
    model = None
    st.error(f"No se pudo cargar el modelo '{MODEL_PATH}'. Detalle: {e}")

st.markdown("<h2 style='text-align:center;'>Predicción de Riesgo de Violencia Conyugal</h2>", unsafe_allow_html=True)
#st.title("Predicción de Riesgo de Violencia Conyugal")
st.divider()

st.markdown(
    """
    Esta aplicación usa un **pipeline de machine learning** ya entrenado para estimar
    la probabilidad de violencia conyugal.

    Se asume que el modelo fue entrenado con variables como:
    `edad_mujer`, `edad_primera_union_iqr`, `edad_primera_relacion_iqr`,
    `edad_conyuge_iqr`, `brecha_edad_pareja`, `frec_periodico`, `frec_radio`,
    `frec_tv`, `quintil_riqueza`, `alcohol_conyuge`, `educ_mujer_rec`,
    `educ_conyuge_rec`, `dif_educ_pareja_cat`, `control_machista`.
    """
)

st.sidebar.success(f"**Ingrese lo Datos**")

col1, col2, col9, col12 = st.sidebar.columns([1,1,1,1])

with col1:
    #st.write("**Edad de la mujer**")
    st.markdown("Edad de la mujer<br><br>", unsafe_allow_html=True) 
    edad_mujer = st.number_input("Edad de la mujer", min_value=15, max_value=49, value=30, step=1, label_visibility="collapsed")

with col2:
    st.markdown("Edad de la primera unión<br>", unsafe_allow_html=True) 
    edad_primera_union_iqr = st.number_input("Edad de la primera unión", min_value=10, max_value=40, value=20, step=1, label_visibility="collapsed")
    
with col9:
    st.markdown("Edad de la 1ra rel. sexual<br>", unsafe_allow_html=True) 
    edad_primera_relacion_iqr = st.number_input("Edad de la 1ra rel. sexual", min_value=10, max_value=40, value=18, step=1, label_visibility="collapsed")    

with col12:
    st.markdown("Edad del cónyuge<br><br>", unsafe_allow_html=True) 
    edad_conyuge_iqr = st.number_input("Edad del cónyuge", min_value=15, max_value=70, value=35, step=1, label_visibility="collapsed")


st.sidebar.markdown("### Frecuencia de medios")
col3, col4, col10  = st.sidebar.columns([1,1,1])

with col3:
    frec_periodico = st.selectbox(
        "Frecuencia de lectura de periódico/revista",
        options=[0, 1, 2, 3],
        format_func=lambda x: {
            0: "Nunca",
            1: "Menos de 1 vez por semana",
            2: "Al menos 1 vez por semana",
            3: "Casi todos los días"
        }[x]
    )
    
with col4:
    frec_radio = st.selectbox(
        "Frecuencia de radio",
        options=[0, 1, 2, 3],
        format_func=lambda x: {
            0: "Nunca",
            1: "Menos de 1 vez por semana",
            2: "Al menos 1 vez por semana",
            3: "Casi todos los días"
        }[x]
    )

with col10:
    frec_tv = st.selectbox(
        "Frecuencia de TV",
        options=[0, 1, 2, 3],
        format_func=lambda x: {
            0: "Nunca",
            1: "Menos de 1 vez por semana",
            2: "Al menos 1 vez por semana",
            3: "Casi todos los días"
        }[x]
    )


st.sidebar.markdown("### Condiciones sociodemográficas")

col5, col6, col11  = st.sidebar.columns([1,1,1])

with col5:
    quintil_riqueza = st.selectbox(
        "Quintil de riqueza",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {
            1: "Más pobre",
            2: "Pobre",
            3: "Medio",
            4: "Rico",
            5: "Más rico"
        }[x]
    )    

with col6:
    educ_mujer_rec = st.selectbox(
        "Educación de la mujer",
        options=[0, 1, 2],
        format_func=lambda x: {
            0: "Baja (sin educación/primaria)",
            1: "Secundaria",
            2: "Superior"
        }[x]
    )

with col11:
    educ_conyuge_rec = st.selectbox(
        "Educación del cónyuge",
        options=[0, 1, 2],
        format_func=lambda x: {
            0: "Baja (sin educación/primaria)",
            1: "Secundaria",
            2: "Superior"
        }[x]
    )


st.sidebar.markdown("### Factores relacionales")

col7, col8  = st.sidebar.columns([1,1])

with col7:
    alcohol_conyuge = st.selectbox(
        "Consumo de alcohol del cónyuge",
        options=[0, 1, 2],
        format_func=lambda x: {
            0: "No consume",
            1: "Consume pero no se embriaga",
            2: "Consume y se embriaga"
        }[x]
    )

with col8:
    control_machista = st.slider("Control machista (escala)", min_value=0, max_value=6, value=1, step=1)


brecha_edad_pareja = edad_conyuge_iqr - edad_mujer

if educ_mujer_rec > educ_conyuge_rec:
    dif_educ_pareja_cat = 1
elif educ_mujer_rec < educ_conyuge_rec:
    dif_educ_pareja_cat = -1
else:
    dif_educ_pareja_cat = 0

obs = pd.DataFrame({
    "edad_mujer": [edad_mujer],
    "edad_primera_union_iqr": [edad_primera_union_iqr],
    "edad_primera_relacion_iqr": [edad_primera_relacion_iqr],
    "edad_conyuge_iqr": [edad_conyuge_iqr],
    "brecha_edad_pareja": [brecha_edad_pareja],
    "frec_periodico": [frec_periodico],
    "frec_radio": [frec_radio],
    "frec_tv": [frec_tv],
    "quintil_riqueza": [quintil_riqueza],
    "alcohol_conyuge": [alcohol_conyuge],
    "educ_mujer_rec": [educ_mujer_rec],
    "educ_conyuge_rec": [educ_conyuge_rec],
    "dif_educ_pareja_cat": [dif_educ_pareja_cat],
    "control_machista": [control_machista],
})


# ----------------------------------------------------------------------
# Initialize session state variables
if 'btn1_state' not in st.session_state:
    st.session_state.btn1_state = False
if 'btn2_state' not in st.session_state:
    st.session_state.btn2_state = False

# Callback functions to update session state
def click_btn1():
    st.session_state.btn1_state = True

def click_btn2():
    st.session_state.btn2_state = True

col_a, col_b = st.columns(2)

with col_a:
    st.button('Predecir', on_click=click_btn1, use_container_width=True)

with col_b:
    st.button('Mostrar variables derivadas', on_click=click_btn2, use_container_width=True)

if st.session_state.btn1_state:
    if model is None:
            st.stop()
    try:            
        pred = model.predict(obs)[0]
        proba = model.predict_proba(obs)[0, 1] if hasattr(model, "predict_proba") else np.nan

        st.markdown("<u><h3 style='text-align:center;'>Resultado</h3></u>", unsafe_allow_html=True)
        #st.subheader("Resultado")
        st.write("**Observación evaluada:**")
        st.dataframe(obs, use_container_width=True)

        colAA, colBB, colCC = st.columns([1, 1, 1])
        with colAA:
            if pred == 1:
                st.error("Predicción: Riesgo de violencia (1)")
            else:
                st.success("Predicción: No riesgo de violencia (0)")
                        
        if not np.isnan(proba):
            with colBB:
                st.metric("Probabilidad estimada de violencia", f"{proba:.2%}")
            
            with colCC:
                if proba < 0.33:
                    st.info("Nivel estimado: Bajo")
                elif proba < 0.66:
                    st.warning("Nivel estimado: Medio")
                else:
                    st.error("Nivel estimado: Alto")

    except Exception as e:
        st.error(f"Ocurrió un error durante la predicción: {e}")

if st.session_state.btn2_state:    
    st.markdown("<u><h3 style='text-align:center;'>Variables derivadas calculadas</h3></u>", unsafe_allow_html=True)
    #st.subheader("Variables derivadas calculadas")

    colDD, colEE = st.columns([1, 1])
    with colDD:
        st.write(f"**brecha_edad_pareja** = {brecha_edad_pareja}")
    with colEE:
        st.write(f"**dif_educ_pareja_cat** = {dif_educ_pareja_cat}")
    st.dataframe(obs, use_container_width=True)

# ----------------------------------------------------------------------
_ = """
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Predecir", use_container_width=True):
        if model is None:
            st.stop()

        try:            
            pred = model.predict(obs)[0]
            proba = model.predict_proba(obs)[0, 1] if hasattr(model, "predict_proba") else np.nan

            st.subheader("Resultado")
            st.write("**Observación evaluada:**")
            st.dataframe(obs, use_container_width=True)

            if pred == 1:
                st.error("Predicción: Riesgo de violencia (1)")
            else:
                st.success("Predicción: No riesgo de violencia (0)")

            if not np.isnan(proba):
                st.metric("Probabilidad estimada de violencia", f"{proba:.2%}")

                if proba < 0.33:
                    st.info("Nivel estimado: Bajo")
                elif proba < 0.66:
                    st.warning("Nivel estimado: Medio")
                else:
                    st.error("Nivel estimado: Alto")

        except Exception as e:
            st.error(f"Ocurrió un error durante la predicción: {e}")

with col2:
    if st.button("Mostrar variables derivadas", use_container_width=True):
        st.subheader("Variables derivadas calculadas")
        st.write(f"**brecha_edad_pareja** = {brecha_edad_pareja}")
        st.write(f"**dif_educ_pareja_cat** = {dif_educ_pareja_cat}")
        st.dataframe(obs, use_container_width=True)
"""

st.markdown("---")
st.caption(
    "Aplicación Streamlit para un pipeline de clasificación. "
    "Recuerda mantener en la misma carpeta el archivo del modelo `.joblib` y este script `.py`."
)