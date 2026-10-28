
import pandas as pd
import streamlit as st
import plotly.express as px

# =========================================
# DASHBOARD DE PRODUCAO DE DETERGENTES
# Base ficticia para portfolio
# =========================================

st.set_page_config(
    page_title="Painel de Produção",
    page_icon="🏭",
    layout="wide"
)

# Estilo visual
st.markdown("""
<style>
    .stApp {
        background-color: #F4F7FB;
    }

    h1, h2, h3 {
        color: #17324D;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #E1E8F0;
        padding: 18px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Carregar dados
@st.cache_data
def carregar_dados():
    dados = pd.read_csv("dados_producao_ficticios.csv")

    dados = dados.dropna(how="all").copy()

    colunas_numericas = [
        "unidades_produzidas",
        "unidades_defeituosas",
        "horas_parada"
    ]

    for coluna in colunas_numericas:
        dados[coluna] = pd.to_numeric(
            dados[coluna], errors="coerce"
        )

    dados = dados.dropna(
        subset=[
            "linha_producao",
            "turno",
            "unidades_produzidas",
            "unidades_defeituosas",
            "horas_parada"
        ]
    ).copy()

    dados["taxa_defeitos_pct"] = (
        dados["unidades_defeituosas"]
        / dados["unidades_produzidas"].where(
            dados["unidades_produzidas"] != 0
        )
    ) * 100

    return dados


try:
    df = carregar_dados()

except FileNotFoundError:
    st.error(
        "CSV não encontrado. Coloque o arquivo "
        "'dados_producao_ficticios.csv' na mesma pasta "
        "do dashboard.py."
    )
    st.stop()

except Exception as erro:
    st.error(f"Não foi possível carregar os dados: {erro}")
    st.stop()


# Titulo e descricao
st.title("🏭 Painel de Inteligência da Produção")
st.caption(
    "Análise de qualidade, produtividade e paradas "
    "| Dados fictícios para fins de estudo"
)

# =========================================
# FILTROS
# =========================================

st.sidebar.header("Filtros")

linhas_disponiveis = sorted(
    df["linha_producao"].dropna().unique().tolist()
)

turnos_disponiveis = sorted(
    df["turno"].dropna().unique().tolist()
)

linhas_selecionadas = st.sidebar.multiselect(
    "Linhas de produção",
    options=linhas_disponiveis,
    default=linhas_disponiveis
)

turnos_selecionados = st.sidebar.multiselect(
    "Turnos",
    options=turnos_disponiveis,
    default=turnos_disponiveis
)

filtrado = df[
    df["linha_producao"].isin(linhas_selecionadas)
    & df["turno"].isin(turnos_selecionados)
].copy()

if filtrado.empty:
    st.warning("Selecione pelo menos uma linha e um turno.")
    st.stop()

# =========================================
# INDICADORES PRINCIPAIS
# =========================================

total_produzido = filtrado["unidades_produzidas"].sum()
total_defeitos = filtrado["unidades_defeituosas"].sum()
total_paradas = filtrado["horas_parada"].sum()

taxa_geral = (
    total_defeitos / total_produzido * 100
    if total_produzido > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Unidades produzidas",
    f"{total_produzido:,.0f}"
)

col2.metric(
    "Unidades defeituosas",
    f"{total_defeitos:,.0f}"
)

col3.metric(
    "Taxa de defeitos",
    f"{taxa_geral:.2f}%"
)

col4.metric(
    "Horas de parada",
    f"{total_paradas:.1f} h"
)

st.divider()

# =========================================
# GRAFICO 1 - TAXA DE DEFEITOS POR TURNO
# =========================================

st.subheader("Qualidade por turno")

por_turno = filtrado.groupby("turno").agg(
    produzidas=("unidades_produzidas", "sum"),
    defeituosas=("unidades_defeituosas", "sum")
).reset_index()

por_turno["taxa_defeitos_pct"] = (
    por_turno["defeituosas"]
    / por_turno["produzidas"].where(
        por_turno["produzidas"] != 0
    )
) * 100

grafico_turno = px.bar(
    por_turno,
    x="turno",
    y="taxa_defeitos_pct",
    color="taxa_defeitos_pct",
    color_continuous_scale="Teal",
    text="taxa_defeitos_pct",
    labels={
        "turno": "Turno",
        "taxa_defeitos_pct": "Taxa de defeitos (%)"
    },
    title="Taxa de defeitos por turno"
)

grafico_turno.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

grafico_turno.update_layout(
    template="plotly_white",
    coloraxis_showscale=False
)

st.plotly_chart(grafico_turno, use_container_width=True)

# =========================================
# GRAFICOS 2 E 3
# =========================================

col_esquerda, col_direita = st.columns(2)

with col_esquerda:
    st.subheader("Desempenho por linha")

    por_linha = filtrado.groupby("linha_producao").agg(
        produzidas=("unidades_produzidas", "sum"),
        defeituosas=("unidades_defeituosas", "sum")
    ).reset_index()

    por_linha["taxa_defeitos_pct"] = (
        por_linha["defeituosas"]
        / por_linha["produzidas"].where(
            por_linha["produzidas"] != 0
        )
    ) * 100

    grafico_linha = px.bar(
        por_linha,
        x="linha_producao",
        y="taxa_defeitos_pct",
        color="linha_producao",
        text="taxa_defeitos_pct",
        labels={
            "linha_producao": "Linha",
            "taxa_defeitos_pct": "Taxa de defeitos (%)"
        },
        title="Taxa de defeitos por linha"
    )

    grafico_linha.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    grafico_linha.update_layout(
        template="plotly_white",
        showlegend=False
    )

    st.plotly_chart(
        grafico_linha,
        use_container_width=True
    )

with col_direita:
    st.subheader("Motivos das paradas")

    paradas = (
        filtrado.groupby("motivo_parada")["horas_parada"]
        .sum()
        .reset_index()
        .sort_values("horas_parada", ascending=False)
    )

    grafico_paradas = px.bar(
        paradas,
        x="horas_parada",
        y="motivo_parada",
        orientation="h",
        color="horas_parada",
        color_continuous_scale="Oranges",
        labels={
            "horas_parada": "Horas de parada",
            "motivo_parada": "Motivo"
        },
        title="Horas de parada por motivo"
    )

    grafico_paradas.update_layout(
        template="plotly_white",
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False
    )

    st.plotly_chart(
        grafico_paradas,
        use_container_width=True
    )

# =========================================
# TIPOS DE FALHA
# =========================================

st.subheader("Distribuição dos tipos de falha")

falhas = (
    filtrado["tipo_falha"]
    .fillna("Não informado")
    .value_counts()
    .rename_axis("tipo_falha")
    .reset_index(name="quantidade")
)

grafico_falhas = px.pie(
    falhas,
    names="tipo_falha",
    values="quantidade",
    hole=0.55,
    title="Registros por tipo de falha"
)

grafico_falhas.update_layout(template="plotly_white")

st.plotly_chart(
    grafico_falhas,
    use_container_width=True
)


# =========================================
# ANALISE DE PARETO DAS FALHAS
# =========================================

st.divider()
st.header("📊 Priorização das falhas — Pareto")

st.write(
    "O gráfico ordena os tipos de falha por frequência e "
    "calcula a participação acumulada de cada categoria."
)

pareto = (
    filtrado["tipo_falha"]
    .fillna("Não informado")
    .value_counts()
    .rename_axis("tipo_falha")
    .reset_index(name="quantidade")
)

pareto["percentual"] = (
    pareto["quantidade"] / pareto["quantidade"].sum()
) * 100

pareto["percentual_acumulado"] = (
    pareto["percentual"].cumsum()
)

fig_pareto = px.bar(
    pareto,
    x="tipo_falha",
    y="quantidade",
    text="quantidade",
    title="Falhas mais frequentes e participação acumulada",
    labels={
        "tipo_falha": "Tipo de falha",
        "quantidade": "Número de registros"
    },
    color="quantidade",
    color_continuous_scale="Teal"
)

fig_pareto.add_scatter(
    x=pareto["tipo_falha"],
    y=pareto["percentual_acumulado"],
    name="Percentual acumulado",
    mode="lines+markers",
    yaxis="y2",
    line=dict(color="#E45756", width=3),
    marker=dict(size=8)
)

fig_pareto.update_layout(
    template="plotly_white",
    yaxis=dict(title="Número de registros"),
    yaxis2=dict(
        title="Percentual acumulado (%)",
        overlaying="y",
        side="right",
        range=[0, 110],
        ticksuffix="%"
    ),
    legend=dict(orientation="h", y=1.12),
    xaxis_tickangle=-25
)

st.plotly_chart(fig_pareto, use_container_width=True)

st.dataframe(
    pareto.round(2),
    use_container_width=True,
    hide_index=True
)

# =========================================
# RECOMENDACOES BASEADAS NOS RESULTADOS
# =========================================

st.subheader("🧭 Pontos de atenção para a operação")

turno_pior = por_turno.loc[
    por_turno["taxa_defeitos_pct"].idxmax()
]

linha_pior = por_linha.loc[
    por_linha["taxa_defeitos_pct"].idxmax()
]

motivo_pior = (
    filtrado.groupby("motivo_parada")["horas_parada"]
    .sum()
    .sort_values(ascending=False)
)

r1, r2, r3 = st.columns(3)

r1.metric(
    "Turno com maior taxa",
    str(turno_pior.name),
    f'{turno_pior["taxa_defeitos_pct"]:.2f}%'
)

r2.metric(
    "Linha com maior taxa",
    str(linha_pior.name),
    f'{linha_pior["taxa_defeitos_pct"]:.2f}%'
)

if not motivo_pior.empty:
    r3.metric(
        "Maior motivo de parada",
        str(motivo_pior.index[0]),
        f"{motivo_pior.iloc[0]:.1f} horas"
    )

st.markdown("""
**Ações recomendadas para investigação:**

1. Conferir regulagem de enchimento e fechamento nas linhas com
   maior taxa de defeitos.
2. Comparar os registros de parada entre turnos e verificar os
   motivos mais recorrentes.
3. Revisar os procedimentos de inspeção e manutenção preventiva.
4. Reavaliar os indicadores após as ações para verificar se houve
   melhoria.

Estas são hipóteses de investigação. Os dados disponíveis não
comprovam, por si só, que a manutenção ou a regulagem causaram
as falhas.
""")


# =========================================
# TABELA DETALHADA
# =========================================

# =========================================
# DETECCAO DE ANOMALIAS COM MACHINE LEARNING
# =========================================

from sklearn.ensemble import IsolationForest

st.divider()
st.header("🤖 Detecção de anomalias")
st.write(
    "O modelo identifica registros que apresentam combinações "
    "incomuns de defeitos, produção e horas de parada."
)

# Criar uma cópia para não alterar os dados originais
df_anomalias = filtrado.copy()

# Variáveis que o modelo irá analisar
colunas_modelo = [
    "unidades_produzidas",
    "unidades_defeituosas",
    "horas_parada",
    "taxa_defeitos_pct"
]

# Preparar os dados para o algoritmo
dados_modelo = df_anomalias[colunas_modelo].replace(
    [float("inf"), float("-inf")], float("nan")
)

# Tratar possíveis valores ausentes
dados_modelo = dados_modelo.fillna(
    dados_modelo.median()
)

if len(dados_modelo) < 10:
    st.warning(
        "Selecione mais registros para executar a análise "
        "com maior utilidade exploratória."
    )

else:
    # Treinar o modelo de detecção
    modelo = IsolationForest(
        n_estimators=200,
        contamination=0.10,
        random_state=42
    )

    previsoes = modelo.fit_predict(dados_modelo)

    # -1 = anomalia; 1 = registro não sinalizado
    df_anomalias["anomalia"] = [
        "Anomalia" if valor == -1 else "Padrão identificado"
        for valor in previsoes
    ]

    # Pontuação: valores menores indicam registros mais atípicos
    df_anomalias["pontuacao_anomalia"] = (
        modelo.decision_function(dados_modelo)
    )

    total_anomalias = (
        df_anomalias["anomalia"] == "Anomalia"
    ).sum()

    percentual_anomalias = (
        total_anomalias / len(df_anomalias) * 100
    )

    # Indicadores
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Registros analisados",
        len(df_anomalias)
    )

    c2.metric(
        "Registros sinalizados",
        int(total_anomalias)
    )

    c3.metric(
        "Percentual sinalizado",
        f"{percentual_anomalias:.1f}%"
    )

    # Gráfico interativo
    st.subheader("Onde estão as anomalias?")

    grafico_anomalias = px.scatter(
        df_anomalias,
        x="horas_parada",
        y="taxa_defeitos_pct",
        color="anomalia",
        symbol="anomalia",
        hover_data=[
            "linha_producao",
            "turno",
            "tipo_falha",
            "unidades_produzidas",
            "unidades_defeituosas",
            "pontuacao_anomalia"
        ],
        color_discrete_map={
            "Anomalia": "#E45756",
            "Padrão identificado": "#268BD2"
        },
        labels={
            "horas_parada": "Horas de parada",
            "taxa_defeitos_pct": "Taxa de defeitos (%)",
            "anomalia": "Classificação"
        },
        title="Taxa de defeitos versus horas de parada"
    )

    grafico_anomalias.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        grafico_anomalias,
        use_container_width=True
    )

    # Mostrar somente os registros sinalizados
    st.subheader("Registros que merecem investigação")

    suspeitos = df_anomalias[
        df_anomalias["anomalia"] == "Anomalia"
    ].sort_values("pontuacao_anomalia")

    if suspeitos.empty:
        st.info("Nenhuma anomalia foi sinalizada nesta seleção.")

    else:
        st.dataframe(
            suspeitos[
                [
                    "data",
                    "linha_producao",
                    "turno",
                    "tipo_falha",
                    "unidades_produzidas",
                    "unidades_defeituosas",
                    "taxa_defeitos_pct",
                    "horas_parada",
                    "anomalia",
                    "pontuacao_anomalia"
                ]
            ].round(3),
            use_container_width=True
        )

        csv_anomalias = suspeitos.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            label="Baixar registros sinalizados em CSV",
            data=csv_anomalias,
            file_name="anomalias_producao.csv",
            mime="text/csv"
        )

    st.caption(
        "O Isolation Forest sinaliza registros atípicos em relação "
        "ao conjunto analisado. O percentual configurado é uma "
        "estimativa do modelo, não uma taxa comprovada de falhas. "
        "Investigue os registros antes de concluir suas causas."
    )

with st.expander("Consultar dados utilizados"):
    st.dataframe(filtrado, use_container_width=True)

st.caption(
    "Projeto educacional com dados fictícios. "
    "Os resultados não representam uma fábrica real."
)


# =========================================
# RESUMO EXECUTIVO DO PROJETO
# =========================================

st.divider()
st.header("📋 Resumo executivo")

st.write(
    "Esta seção consolida os principais indicadores da "
    "produção para facilitar a interpretação dos resultados."
)

total_unidades = filtrado["unidades_produzidas"].sum()
total_defeitos_exec = filtrado["unidades_defeituosas"].sum()

taxa_exec = (
    total_defeitos_exec / total_unidades * 100
    if total_unidades > 0 else 0
)

horas_paradas_exec = filtrado["horas_parada"].sum()

st.markdown("### Indicadores consolidados")

resumo = pd.DataFrame({
    "Indicador": [
        "Registros analisados",
        "Unidades produzidas",
        "Unidades defeituosas",
        "Taxa de defeitos",
        "Horas de parada"
    ],
    "Resultado": [
        len(filtrado),
        f"{total_unidades:,.0f}",
        f"{total_defeitos_exec:,.0f}",
        f"{taxa_exec:.2f}%",
        f"{horas_paradas_exec:.1f} horas"
    ]
})

st.dataframe(
    resumo,
    use_container_width=True,
    hide_index=True
)

st.markdown("### Interpretação")

st.write(
    f"Foram analisados {len(filtrado)} registros, "
    f"com {total_unidades:,.0f} unidades produzidas e "
    f"taxa geral de defeitos de {taxa_exec:.2f}%."
)

st.write(
    f"O total registrado de paradas foi de "
    f"{horas_paradas_exec:.1f} horas."
)

st.info(
    "Os dados são fictícios. Os resultados representam uma "
    "simulação analítica e não devem ser apresentados como "
    "resultados reais de uma empresa."
)
