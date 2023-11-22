import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Título
st.title(':blue[Registro de pacientes] :dna:')
st.subheader('Análise baseada nas relações entre amostra coletada e data do infarto agudo do miocárdio', divider='rainbow')

df = pd.read_csv("planilha_pacientes_csv.csv")

# Título da barra lateral
st.sidebar.title("**Filtrar pacientes** 📊")

# Slider
tempo_pos_iam_meses_range = st.sidebar.slider(
    label="Filtrar Tempo após o infarto agudo do miocárdio (em meses)",
    min_value=df['TEMPO_POS_IAM_MESES'].min(),
    max_value=df['TEMPO_POS_IAM_MESES'].max(),
    value=(df['TEMPO_POS_IAM_MESES'].min(), df['TEMPO_POS_IAM_MESES'].max()),
    step=2.0
)
filtered_df = df[(df['TEMPO_POS_IAM_MESES'] >= tempo_pos_iam_meses_range[0]) & (df['TEMPO_POS_IAM_MESES'] <= tempo_pos_iam_meses_range[1])]

# Valores crescentes
filtered_df = filtered_df.sort_values(by='TEMPO_POS_IAM_MESES')

# Métrica
st.metric(label='Total de pacientes', value=filtered_df['COD'].count(), help='Número total de pacientes incluídos na pesquisa')

# Filtro local
mapeamento_local = {"AMB": "Ambulatório", "HEMO": "Hemodinâmica"}
filtered_df['LOCAL'] = filtered_df['LOCAL'].map(mapeamento_local)
local_options = ["Todos"] + filtered_df['LOCAL'].unique().tolist()
local = st.sidebar.radio(
    "Filtrar por local de coleta dos pacientes",
    local_options,
    index=0  # Valor padrão selecionado
)
if local != "Todos":
    filtered_df = filtered_df[filtered_df['LOCAL'] == local]
st.sidebar.markdown(f"<span style='color:blue'>Número de pacientes selecionados: {filtered_df['COD'].count()}</span>", unsafe_allow_html=True)

# Filtro retorno
mapeamento_retorno = {'N': 'Não retornou', 'S': 'Retornou'}
retorno_options = ["Todos", 'Retornou', 'Não retornou']
retorno = st.sidebar.radio("Filtrar por retorno dos pacientes", retorno_options, index=0)

if retorno != "Todos":
    valor_retorno = 'S' if retorno == 'Retornou' else 'N'
    filtered_df = filtered_df[filtered_df['RETORNO'] == valor_retorno]
st.sidebar.markdown(f"<span style='color:blue'>Número de pacientes selecionados: {filtered_df['COD'].count()}</span>", unsafe_allow_html=True)

# Escolha de guia
guia = st.sidebar.selectbox("Selecione a guia:", ["Tempo após o infarto agudo do miocárdio", "Idades", 'Sexo'])

if guia == "Tempo após o infarto agudo do miocárdio":
    filtered_df['TEMPO_POS_IAM_MESES'] = filtered_df['TEMPO_POS_IAM_MESES']
    
    # Mapeia os valores da coluna 'SEXO' para 'Homens' e 'Mulheres'
    sexo_mapping = {'M': 'Homens', 'F': 'Mulheres'}
    filtered_df['SEXO_NOME'] = filtered_df['SEXO'].map(sexo_mapping)
    
    fig = px.bar(filtered_df, x="COD", y="TEMPO_POS_IAM_MESES", color="SEXO_NOME", barmode="group")

    fig.update_traces(
        hovertemplate='Código: %{x}<br>Tempo pós IAM em meses: %{y}<br>Sexo: %{customdata[0]}<extra></extra>',
        customdata=filtered_df[['SEXO_NOME']]
    )

    fig.update_xaxes(title_text="Código do paciente")
    fig.update_yaxes(title_text="Tempo pós infarto agudo do miocárdio em meses")
    fig.update_layout(title="Tempo após o infarto agudo do miocárdio")
    fig.update_layout(xaxis_title="Código do paciente", yaxis_title="Tempo pós infarto agudo do miocárdio em meses")
    fig.update_layout(hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"))
    st.plotly_chart(fig, use_container_width=True)

elif guia == "Idades":
        media_idades = filtered_df['IDADE'].mean()
        media_formatada = int(round(media_idades))
        fig_idades = px.line(filtered_df, x='COD', y='IDADE', labels={'x': 'Pacientes', 'y': 'IdadeS'})
        fig_idades.add_hline(y=media_idades, line_dash="dash", line_color="green", name=f'Média: {media_idades:.2f}')
        fig_idades.add_trace(go.Scatter(x=[filtered_df['COD'].min(), filtered_df['COD'].max()], y=[media_idades, media_idades],
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
        
        
elif guia == "Sexo":
    filtered_df['SEXO_NOME'] = filtered_df['SEXO'].map({'M': 'Homens', 'F': 'Mulheres'})
    fig_genero = px.pie(filtered_df, names='SEXO_NOME', title='Proporção entre homens e mulheres incluídos no estudo')
    fig_genero.update_traces(
        hovertemplate='Sexo: %{label}<br>%{percent}<extra></extra>'
    )
    
    st.plotly_chart(fig_genero)
