import streamlit as st
import pandas as pd
import laspy
import pydeck as pdk
from io import BytesIO

st.set_page_config(layout="wide")
st.title("Visualizador e Conversor de LiDAR (.mpl / .las)")

uploaded_file = st.file_uploader("Escolha um arquivo (.mpl ou .las)", type=["mpl", "las"])

if uploaded_file:
    content = uploaded_file.read()
    
    if uploaded_file.name.endswith(".mpl"):
        st.warning("Arquivo MPL binário carregado. Não é possível ler diretamente os pontos LiDAR.")
        st.write("Tamanho do arquivo:", len(content), "bytes")
        st.code(content[:256].hex())  # primeiros 256 bytes em hexadecimal
        st.info("""
        Para processar os pontos:
        1. Abra o arquivo MPL no software original que gerou ele.
        2. Exporte para LAS ou LAZ.
        3. Faça upload do arquivo LAS/LAZ aqui para análise.
        """)
    
    elif uploaded_file.name.endswith(".las"):
        st.success("Arquivo LAS carregado com sucesso!")
        uploaded_file.seek(0)
        las_file = laspy.read(BytesIO(uploaded_file.read()))
        
        # Cria DataFrame com coordenadas e intensidade
        df = pd.DataFrame({
            "X": las_file.x,
            "Y": las_file.y,
            "Z": las_file.z,
            "Intensity": las_file.intensity
        })
        
        st.subheader("Informações gerais")
        st.write("Número de pontos:", len(df))
        st.write("Estatísticas básicas:")
        st.dataframe(df.describe())
        
        st.subheader("Visualização 3D da nuvem de pontos")
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=df['Y'].mean(),
                longitude=df['X'].mean(),
                zoom=15,
                pitch=45
            ),
            layers=[
                pdk.Layer(
                    'PointCloudLayer',
                    data=df,
                    get_position='[X, Y, Z]',
                    get_color='[Intensity, Intensity, Intensity]',
                    point_size=2,
                )
            ]
        ))
