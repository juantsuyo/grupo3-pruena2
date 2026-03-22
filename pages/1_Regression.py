import streamlit as st
import pandas as pd
from joblib import load
import pickle
import numpy as np
import base64

from sklearn.preprocessing import StandardScaler
#import pyautogui


st.set_page_config(page_title="Regression", page_icon=":material/thumb_up:", initial_sidebar_state="expanded")


@st.cache_data
def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def build_markup_for_logo(
    png_file,
    background_position="50% 10%",
    margin_top="1%",
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


# Cargar el modelo de regresión
regressor = load('randomforest_model_reg.joblib')

# Cargar el encoder
#with open('encoderpipeline.pickle', 'rb') as f:
#    encoder = pickle.load(f)

# Inicializar variables
field_edad = field_nro_personas_trabajo = 1
field_horas_trabajo = 0

field_select_sexo = "Masculino"
field_select_NIVELI = 'Primaria'
field_select_Informal_P = 'Empleo Formal'

# Streamlit app
st.markdown("<h2 style='text-align:center;'>Determinantes socioeconómicos del ingreso laboral en trabajadores independientes de la ciudad de Cajamarca, 2024</h2>", unsafe_allow_html=True)
#st.title("")

st.divider()
st.markdown("###### Esta aplicación utiliza el modelo de Random Forest para la prediccion.")

# Sidebar para la entrada del usuario
st.sidebar.success(f"**Ingrese lo Datos**")

col1, col2 = st.sidebar.columns([1,1])

with col1:
    st.markdown("<div style='display:flex; align-items: flex-end;'><h3>Edad</h3>&nbsp;&nbsp;<h5>(Min=0, Max=99)</h5></div>", unsafe_allow_html=True)    
    field_edad = st.number_input("**edad (Min=0, Max=99)**", min_value=0, value=int(field_edad), label_visibility="collapsed")

with col2:
    st.markdown("<div style='display:flex; align-items: flex-end;'><h3>Horas de Trabajo</h3>&nbsp;&nbsp;<h5>(Min=0, Max=112)</h5></div>", unsafe_allow_html=True)    
    field_horas_trabajo = st.number_input("**horas_trabajo (Min=0, Max=112)**", min_value=0, value=int(field_horas_trabajo), label_visibility="collapsed")

st.sidebar.markdown("<div style='display:flex; align-items: flex-end;'><h3>Nro. de Personas por trabajo</h3>&nbsp;&nbsp;<h5>(Min=1, Max=31)</h5></div>", unsafe_allow_html=True)    
field_nro_personas_trabajo = st.sidebar.number_input("**nro_personas_trabajo (Min=1, Max=31)**", min_value=1, value=int(field_nro_personas_trabajo), label_visibility="collapsed")


col3, col4 = st.sidebar.columns([1,1])

with col3:
    
    st.markdown("<h3>Sexo</h3>", unsafe_allow_html=True)
    field_select_sexo = st.selectbox("Select Sexo", ["Masculino", "Femenino"], index=["Masculino", "Femenino"].index(field_select_sexo), label_visibility="collapsed")
    
    st.markdown("<h3>Nivel Educativo</h3>", unsafe_allow_html=True)
    field_select_NIVELI = st.selectbox("Select Nivel Educativo", ["Primaria", "Secundaria", "Superior"], index=["Primaria", "Secundaria", "Superior"].index(field_select_NIVELI), label_visibility="collapsed")

with col4:    
    st.markdown("<h3>Situación de Informalidad</h3>", unsafe_allow_html=True)
    field_select_Informal_P = st.selectbox("Select Situación de Informalidad", ["Empleo Formal", "Empleo Informal"], index=["Empleo Formal", "Empleo Informal"].index(field_select_Informal_P), label_visibility="collapsed")


# Función para resetear las entradas
def reset_inputs():
    global field_edad, field_horas_trabajo, field_select_sexo, field_select_NIVELI, field_select_Informal_P
    
    field_edad = field_nro_personas_trabajo = 1
    field_horas_trabajo = 0

    field_select_sexo = "Masculino"
    field_select_NIVELI = 'Primaria'
    field_select_Informal_P = 'Empleo Formal'


# Botón para predecir
if st.button("Predecir", use_container_width=True):

    # Validar las entradas

    if all(isinstance(val, (int)) and val >= 1 for val in [field_edad, field_nro_personas_trabajo,]) and all(isinstance(val, (int)) and val >= 0 for val in [field_horas_trabajo,]):
        # Crear un DataFrame con las entradas del usuario
        obs = pd.DataFrame({
            'sexo': [field_select_sexo],
            'edad': [field_edad],
            'nro_personas_trabajo': [field_nro_personas_trabajo],
            'horas_trabajo': [field_horas_trabajo],
            'NIVELI': [field_select_NIVELI],
            'Informal_P': [field_select_Informal_P]
        })

        # Mostrar el DataFrame de entradas para depuración
        st.write("DataFrame de Entradas:")
        st.write(obs)

        #----------------------Pipeline-------------------------
        # Predecir usando el modelo
        target = regressor.predict(obs)

        # Mostrar la predicción con un tamaño de fuente grande usando markdown
        st.markdown(f'<p style="font-size: 40px; color: green;">La predicción del "Ingreso Laboral" será: S/. {target[0]:,.2f}</p>', unsafe_allow_html=True)

    else:
        st.warning("Rellene todos los espacios en blanco")

# Colocar el botón "Resetear" debajo del botón "Predecir"
if st.sidebar.button("Resetear", use_container_width=True):
    # Resetear inputs
    reset_inputs()

