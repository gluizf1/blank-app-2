import streamlit as st
import pandas as pd
import laspy
import pydeck as pdk
from io import BytesIO

st.title("Visualizador de arquivos LiDAR (.mpl / .las)")

# Upload do arquivo
uploaded_file = st.file_uploader("Escolha um arquivo (.mpl ou .las)", type=["mpl", "las"])

if uploaded_file is not None:
    content = uploaded_file.read()
    
    if uploaded_file.name.endswith(".mpl"):
        st.warning("Arquivo MPL binário carregado. Não é possível ler diretamente os pontos LiDAR.")
        st.write("Tamanho do arquivo:", len(content), "bytes")
        st.code(content[:256].hex())  # Mostra primeiros bytes em hex
        st.info("Para processar os pontos, exporte o arquivo MPL para LAS/LAZ usando o software original.")
    
    elif uploaded_file.name.endswith(".las"):
        st.success("Arquivo LAS carregado com sucesso!")
        uploaded_file.seek(0)
        las_file = laspy.read(BytesIO(uploaded_file.read()))
        
        # Cria DataFrame com coordenadas
        df = pd.DataFrame({
            "X": las_file.x,
            "Y": las_file.y,
            "Z": las_file.z,
            "Intensity": las_file.intensity
        })
        st.write("Número de pontos:", len(df))
        st.dataframe(df.head(10))
        
        # Estatísticas básicas
        st.write("Estatísticas básicas:")
        st.write(df.describe())
        
        # Visualização 3D com pydeck
        st.write("Visualização 3D:")
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
