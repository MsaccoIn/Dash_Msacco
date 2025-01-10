import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("Dashboard MSacco")

# Caminho para o arquivo base de dados consolidado
file_path = "Resumo_Operacional_Com_Graficos.xlsx"

# Verifica se o arquivo existe
if os.path.exists(file_path):
    # Lê todas as abas do Excel
    sheets = pd.read_excel(file_path, sheet_name=None)

    # Seleção de abas
    sheet_names = list(sheets.keys())
    selected_sheet = st.selectbox("Selecione a aba que deseja visualizar:", sheet_names)

    # Carrega os dados da aba selecionada
    df = sheets[selected_sheet]

    # Formatação de valores como moeda
    columns_to_format = ['Vlr Médio Transporte', 'Lucro Bruto', 'Saldo Mensal', 'Custo Total']
    for col in columns_to_format:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"R$ {x:,.2f}" if pd.notnull(x) else x)

    # Exibe os dados na tabela
    st.subheader(f"Dados Consolidados - Aba: {selected_sheet}")
    st.dataframe(df)

    # Seleção de métrica para exibição gráfica
    st.subheader("Selecione a métrica para o gráfico")
    metrics = [
        'Sacas Entregues',
        'Projeção Caminhões',
        'Custo Médio Saca',
        'Spread Médio',
        'Lucro Bruto',
        'Saldo Mensal',
        'Custo Total'
    ]
    selected_metric = st.selectbox("Selecione a métrica:", [metric for metric in metrics if metric in df.columns])

    # Gráfico da métrica selecionada
    if 'Mês' in df.columns and selected_metric in df.columns:
        st.subheader(f"Gráfico de {selected_metric} por Mês")
        fig, ax = plt.subplots()
        df['Mês'] = df['Mês'].astype(str)  # Garante que o eixo X seja tratado como string
        df.plot(x='Mês', y=selected_metric, kind='line', ax=ax, marker='o', legend=False)

        # Adiciona os valores nos pontos
        for i, row in df.iterrows():
            ax.text(row['Mês'], row[selected_metric], f"{row[selected_metric]:,.0f}", fontsize=8, ha='center', va='bottom')

        ax.set_title(f"{selected_metric} por Mês")
        ax.set_ylabel(selected_metric)
        ax.set_xlabel("Mês")
        st.pyplot(fig)
else:
    st.error("O arquivo base de dados consolidado não foi encontrado no repositório.")
