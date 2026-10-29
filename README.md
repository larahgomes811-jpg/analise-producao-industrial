
[![Abrir Dashboard](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://industry-an.streamlit.app/)

**Dashboard online:** https://industry-an.streamlit.app/

# Análise de Produção Industrial — Detecção de Falhas e Anomalias

## Sobre o projeto

Este projeto simula um cenário de produção industrial de detergentes e utiliza análise de dados para investigar defeitos, paradas de máquinas e diferenças de desempenho entre linhas de produção e turnos de trabalho.

O objetivo é transformar dados operacionais em informações que apoiem a identificação de problemas e a tomada de decisões.

**Observação:** todos os dados utilizados são fictícios e foram criados exclusivamente para fins de estudo e demonstração profissional.

## Objetivos

- Identificar padrões de defeitos na produção.
- Comparar indicadores entre turnos e linhas de produção.
- Investigar os principais tipos de falhas e motivos de parada.
- Desenvolver um dashboard interativo para explorar os indicadores.
- Aplicar detecção exploratória de anomalias com aprendizado de máquina.
- Propor ações para reduzir perdas e melhorar a eficiência operacional.

## Tecnologias utilizadas

- **Python:** processamento e análise dos dados.
- **Pandas:** limpeza, transformação e análise exploratória.
- **SQL / SQLite:** armazenamento e consulta dos dados.
- **Matplotlib e Seaborn:** visualização de dados.
- **Plotly e Streamlit:** dashboard interativo.
- **Scikit-learn:** detecção exploratória de anomalias com Isolation Forest.

## Análises desenvolvidas

- Taxa de defeitos por turno e linha de produção.
- Distribuição dos tipos de falha.
- Análise de horas de parada por motivo.
- Cruzamento entre turnos e tipos de falha.
- Análise de Pareto para priorização de problemas.
- Identificação de registros potencialmente anômalos.
- Elaboração de recomendações para investigação operacional.

## Resultados preliminares

Na base fictícia analisada, o turno da noite apresentou uma taxa de defeitos de aproximadamente 3,09%, superior às taxas observadas nos turnos da manhã (0,85%) e da tarde (1,13%).

O resultado sugere que o turno da noite merece investigação prioritária. Entretanto, essa diferença não comprova, por si só, que o turno seja a causa dos defeitos.

As hipóteses incluem condições de manutenção, regulagem de máquinas e diferenças operacionais entre turnos. Elas precisam ser investigadas com dados adicionais antes de qualquer conclusão definitiva.

## Recomendações iniciais

1. Investigar as condições de regulagem e manutenção das máquinas durante o turno da noite.
2. Comparar as ocorrências de defeitos por linha de produção e tipo de falha.
3. Verificar a relação entre horas desde a última manutenção, paradas e defeitos, quando esses dados estiverem disponíveis.
4. Monitorar os indicadores em um dashboard para acompanhar possíveis melhorias.
5. Validar os alertas de anomalia antes de utilizá-los como evidência de falhas reais.

## Limitações

Este projeto utiliza uma base fictícia e relativamente pequena. Portanto, os resultados são demonstrativos e não representam conclusões sobre uma fábrica real.

A detecção de anomalias é exploratória: um registro sinalizado pelo algoritmo precisa ser analisado antes de ser classificado como problema operacional.

## Estrutura do projeto

- `dados_producao_ficticios.csv` — base de dados.
- `analise_producao.py` — análise exploratória e gráficos.
- `criar_banco.py` — criação do banco SQLite.
- `dashboard.py` — dashboard interativo e análise de anomalias.
- `gerar_relatorio.py` — geração do relatório em PDF.
- `relatorio_producao.pdf` — relatório dos resultados.

---

**Projeto de portfólio — Ciência de Dados**

Desenvolvido para demonstrar habilidades em análise de dados, SQL, visualização e investigação de problemas operacionais.
