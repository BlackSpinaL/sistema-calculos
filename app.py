import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistema de Cálculos", layout="wide")

st.title("📊 Sistema de Cálculos - Solicitações")

# Upload do arquivo
uploaded_file = st.file_uploader("Envie o arquivo de solicitações (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        turmas = st.multiselect("Selecione as turmas", df["Turma"].unique())
    with col2:
        segmentos = st.multiselect("Selecione os segmentos", df["Segmento"].unique())
    with col3:
        tipo = st.selectbox("Tipo de avaliação", ["Todos", "Melhoria", "Recuperação"])

    # Aplicar filtros
    filtrado = df.copy()
    if turmas:
        filtrado = filtrado[filtrado["Turma"].isin(turmas)]
    if segmentos:
        filtrado = filtrado[filtrado["Segmento"].isin(segmentos)]
    if tipo != "Todos":
        filtrado = filtrado[filtrado["Tipo"] == tipo]

    # Cálculos (exemplo: contar solicitações por disciplina e tipo)
    resultado = filtrado.groupby(["Disciplina", "Tipo"]).size().reset_index(name="Total")

    # Mostrar resultados
    st.subheader("Resultados filtrados")
    st.dataframe(resultado)

    st.subheader("Gráfico por disciplina")
    st.bar_chart(resultado.set_index("Disciplina")["Total"])