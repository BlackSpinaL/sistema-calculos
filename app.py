import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistema de Cálculos", layout="wide")

st.title("📊 Sistema de Cálculos - Solicitações")

# Upload do arquivo
uploaded_file = st.file_uploader("Envie o arquivo de solicitações (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Transformar colunas de disciplinas em formato longo
    disciplinas = []
    for i in range(1, 5):  # até 4 disciplinas
        col_disc = f"{i}ª Disciplina"
        col_motivo = "Motivo Solicitação"  # todas as colunas têm o mesmo nome
        if col_disc in df.columns and col_motivo in df.columns:
            temp = df[[
                "Matrícula", "Nome do Aluno", "Código Turma",
                "Curso", "Ano Letivo", "Etapa", col_disc, col_motivo
            ]].copy()
            temp = temp.rename(columns={col_disc: "Disciplina", col_motivo: "Tipo"})
            disciplinas.append(temp)

    # Concatenar todas as solicitações
    if disciplinas:
        df_long = pd.concat(disciplinas)
    else:
        st.error("Nenhuma coluna de disciplina encontrada no arquivo enviado.")
        st.stop()

    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        turmas = st.multiselect("Selecione as turmas", df_long["Código Turma"].unique())
    with col2:
        segmentos = st.multiselect("Selecione os segmentos", df_long["Curso"].unique())
    with col3:
        tipo = st.selectbox("Tipo de avaliação", ["Todos", "RECUPERACAO", "MELHORIA DE NOTA"])

    # Aplicar filtros
    filtrado = df_long.copy()
    if turmas:
        filtrado = filtrado[filtrado["Código Turma"].isin(turmas)]
    if segmentos:
        filtrado = filtrado[filtrado["Curso"].isin(segmentos)]
    if tipo != "Todos":
        filtrado = filtrado[filtrado["Tipo"] == tipo]

    # Cálculos (contagem por disciplina e tipo)
    resultado = filtrado.groupby(["Disciplina", "Tipo"]).size().reset_index(name="Total")

    # Mostrar resultados
    st.subheader("Resultados filtrados")
    st.dataframe(resultado)

    st.subheader("Gráfico por disciplina")
    if not resultado.empty:
        st.bar_chart(resultado.set_index("Disciplina")["Total"])
    else:
        st.info("Nenhum dado encontrado para os filtros selecionados.")
