import streamlit as st

st.title("Inspeção de arquivo binário MPL")

uploaded_file = st.file_uploader("Escolha um arquivo .mpl", type="mpl")

if uploaded_file is not None:
    content = uploaded_file.read()
    st.write("Tamanho do arquivo:", len(content), "bytes")
    
    # Mostrar primeiros 256 bytes em hexadecimal
    hex_preview = content[:256].hex()
    st.code(hex_preview)
