import streamlit as st

st.title("Visualizador de arquivos MPL")

# Upload do arquivo
uploaded_file = st.file_uploader("Escolha um arquivo .mpl", type="mpl")

if uploaded_file is not None:
    # Tenta ler como texto
    try:
        content = uploaded_file.read().decode("utf-8")
        st.success("Arquivo lido como texto:")
        st.text_area("Conteúdo do arquivo", content, height=300)
    except UnicodeDecodeError:
        st.warning("Arquivo parece ser binário. Exibindo bytes iniciais:")
        uploaded_file.seek(0)
        content = uploaded_file.read(500)  # mostra os primeiros 500 bytes
        st.code(content)
