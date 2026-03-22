import streamlit as st

st.set_page_config(page_title="GRUPO 3: MACHINE LEARNING EN PRODUCCIÓN DESPLIEGUE WEB", page_icon=":streamlit:", initial_sidebar_state="expanded")

st.sidebar.image("files/images1.png",width='stretch')
st.sidebar.header("GRUPO 3")

st.markdown(
    """
    <style>
    .custom-title {
        background-color: #06457F; 
        color: white;             
        padding: 10px;            
        border-radius: 10px;       
        text-align: center;       
    }
    .st-emotion-cache-zy6yx3 {
        padding: 3rem 8rem 10rem;
    }
    
    .st-key-my_button button {
        background-color: #FF4B4B; /* Red background */
        color: white;             /* White text */
        border-radius: 10px;      /* Rounded corners */
        height: 3em;              /* Larger height */
        font-size: 20px;          /* Larger font */
    }
    .st-key-my_button button:hover {
        background-color: #FF7E7E; /* Lighter red on hover */
    }

    .st-key-my_button2 button {
        background-color: #FF4B4B; /* Red background */
        color: white;             /* White text */
        border-radius: 10px;      /* Rounded corners */
        height: 3em;              /* Larger height */
        font-size: 20px;          /* Larger font */
    }
    .st-key-my_button2 button:hover {
        background-color: #FF7E7E; /* Lighter red on hover */
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h3 class="custom-title" style="color:white">GRUPO 3<br>MACHINE LEARNING EN PRODUCCIÓN DESPLIEGUE WEB</h3>', unsafe_allow_html=True)
st.html("<br>")

col1, col2, col3 = st.columns(3)
with col1:
    st.warning('ELEGIR:')

with col2:
    if st.button("Modelo de Regresión", key="my_button"):
        st.switch_page("pages/1_Regression.py")

with col3:
    if st.button("Modelo de Clasificación", key="my_button2"):
        st.switch_page("pages/2_Clasificacion.py")


st.divider()

st.markdown("<h3 style='text-align:center;'>Integrantes del Grupo:</h3>", unsafe_allow_html=True)

col4, col5 = st.columns(2)

with col4:
    st.success(f"**LUJAN HUACHHUACO, JOSE ALBERTO**") 
    st.success("**MORALES RENGIFO, MARJORIE SUZANNE**") 
    st.success("**PADILLA PADILLA, JUAN MANUEL**") 

with col5:
    st.success("**SARAVIA AGUILAR, KARINA HELGA**") 
    st.success("**SUYO CHOQUE, JUAN TEOFILO**") 
    st.success("**VAL ZAPATA, NESTOR AUGUSTO**") 


#st.info("Integrantes del Grupo:") 
#st.success("LUJAN HUACHHUACO, JOSE ALBERTO") 
#st.success("MORALES RENGIFO, MARJORIE SUZANNE") 
#st.success("PADILLA PADILLA, JUAN MANUEL") 
#st.success("SARAVIA AGUILAR, KARINA HELGA") 
#st.success("SUYO CHOQUE, JUAN TEOFILO") 
#st.success("VAL ZAPATA, NESTOR AUGUSTO") 