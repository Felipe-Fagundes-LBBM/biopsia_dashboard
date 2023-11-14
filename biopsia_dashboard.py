import pandas as pd
import streamlit as st
import requests
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

# Título
st.title(':blue[Registro de pacientes] :dna:')
st.subheader('Análise baseada nas relações entre amostra coletada e data do infarto agudo do miocárdio', divider='rainbow')

df = pd.read_csv('panilha_pacientes_csv.csv')

# Métrica
st.metric(label='Total de pacientes', value=df['COD'].count(), help='Número total de pacientes incluídos na pesquisa')

# Escolha de guia
guia = st.selectbox("Selecione a guia:", ["Tempo após o infarto agudo do miocárdio 📈 ", "DataFrame 📁 ", "Idades e Sexo 📊 "])

if guia == "Tempo após o infarto agudo do miocárdio 📈 ":
    df['TEMPO_POS_IAM_MESES'] = df['TEMPO_POS_IAM_MESES'].str.replace(',', '.').astype(float)
    fig = px.bar(df, x="COD", y="TEMPO_POS_IAM_MESES", color="SEXO", barmode="group")
    fig.update_xaxes(title_text="Código do paciente")
    fig.update_yaxes(title_text="Tempo pós infarto agudo do miocárdio em meses")
    # Adicionar título ao layout
    fig.update_layout(title="Tempo após o infarto agudo do miocárdio")
    st.plotly_chart(fig, use_container_width=True)

elif guia == "Idades e Sexo 📊 ":
    col1, col2 = st.columns(2)

    # Gráfico de Idades
    with col1:
        media_idades = df['IDADE'].mean()
        media_formatada = int(round(media_idades))
        fig_idades = px.line(df, x='COD', y='IDADE', labels={'x': 'Pacientes', 'y': 'IdadeS'})
        fig_idades.add_hline(y=media_idades, line_dash="dash", line_color="green", name=f'Média: {media_idades:.2f}')
        fig_idades.add_trace(go.Scatter(x=[df['COD'].min(), df['COD'].max()], y=[media_idades, media_idades],
                                        line=dict(color='green', dash='dash'),
                                        name=f'Média: {media_formatada}'))
        fig_idades.update_layout(
            title='Idades dos Pacientes e Média',
            xaxis_title='Código do paciente',
            yaxis_title='Idades',
            xaxis_tickangle=45,
            legend=dict(font=dict(size=12)),
            legend_traceorder='reversed',
        )
        st.plotly_chart(fig_idades)
        
        # Gráfico de Proporção de Gênero
    with col2:
        df['SEXO_NOME'] = df['SEXO'].map({'M': 'Homens', 'F': 'Mulheres'})
        fig_genero = px.pie(df, names='SEXO_NOME', title='Proporção entre homens e mulheres incluídos no estudo',
                            hover_data=['SEXO_NOME'])
        fig_genero.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_genero)


elif guia == "DataFrame 📁 ":
    st.dataframe(df)



