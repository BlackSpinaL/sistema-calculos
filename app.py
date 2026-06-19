import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistema de Cálculos", layout="wide")

st.title("📊 Sistema de Cálculos - Solicitações")

uploaded_file = st.file_uploader("Envie o arquivo de solicitações (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Identificar colunas de disciplina e motivo
    disciplina_cols = [col for col in df.columns if "Disciplina" in col]
    motivo_cols = [col for col in df.columns if "Motivo" in col]

    disciplinas = []
    # Parear cada disciplina com o motivo correspondente pelo índice
    for i, col_disc in enumerate(disciplina_cols):
        if i < len(motivo_cols):
            col_motivo = motivo_cols[i]
            temp = df[[
                "Matrícula", "Nome do Aluno", "Código Turma",
                "Curso", "Ano Letivo", "Etapa", col_disc, col_motivo
            ]].copy()
            temp = temp.rename(columns={col_disc: "Disciplina", col_motivo: "Tipo"})
            temp = temp[temp["Disciplina"].notna()]
            disciplinas.append(temp)

    if disciplinas:
        df_long = pd.concat(disciplinas)
    else:
        st.error(f"Colunas encontradas: {df.columns.tolist()}")
        st.stop()

    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        turmas = st.multiselect("Selecione as turmas", df_long["Código Turma"].unique())
    with col2:
        segmentos = st.multiselect("Selecione os segmentos", df_long["Curso"].unique())
    with col3:
        tipo = st.selectbox("Tipo de avaliação", ["Todos", "RECUPERACAO", "MELHORIA DE NOTA"])

    filtrado = df_long.copy()
    if turmas:
        filtrado = filtrado[filtrado["Código Turma"].isin(turmas)]
    if segmentos:
        filtrado = filtrado[filtrado["Curso"].isin(segmentos)]
    if tipo != "Todos":
        filtrado = filtrado[filtrado["Tipo"] == tipo]

    resultado = filtrado.groupby(["Disciplina", "Tipo"]).size().reset_index(name="Total")

    st.subheader("Resultados filtrados")
    st.dataframe(resultado)

    st.subheader("Gráfico por disciplina")
    if not resultado.empty:
        st.bar_chart(resultado.set_index("Disciplina")["Total"])
    else:
        st.info("Nenhum dado encontrado para os filtros selecionados.")
