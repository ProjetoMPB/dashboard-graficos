import dash
from dash import dcc, html, Input, Output #, State
# import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# import pandas as pd
import carrega_dados
import math
import os

############################
## INICIALIZA O DASHBOARD ##
############################

app = dash.Dash(__name__)

######################
## CARREGA OS DADOS ##
######################

dfs = {}

## c-letras
dfs['c'] = carrega_dados.carrega_c_letras()

## r-letras
dfs['r'] = carrega_dados.carrega_r_letras()

# genera de tipos acordais, tipos acordais e acordes específicos
dfs['genera'], dfs['tas'], dfs['ac_espec'] = carrega_dados.carrega_genera_tas_acordes()

#########################
## DICIONARIO DE CORES ##
#########################

dict_cores = {}

for corpus in dfs['c']['df'].columns.values.tolist():
    if corpus in ['JAZZ', 'CHORO', 'SAMBA']:
        dict_cores[corpus] = 'lightsalmon'
    elif corpus == 'MPB':
        dict_cores[corpus] = 'purple'
    else:
        dict_cores[corpus] = 'firebrick'

################################################
## ATUALIZA GRÁFICOS DOS CORPORA SELECIONADOS ##
################################################

# Callback para atualizar os gráficos dos corpora selecionados
@app.callback(
    Output("dynamic-charts-container", "children"),
    [Input("dropdown-grafico", "value"),
     Input("dropdown-corpora", "value"),
     Input("generate-button", "n_clicks")]
)
    # Input("generate-button", "n_clicks"),
    # State("dropdown-corpora", "value")    
# )

def update_dynamic_charts(selected_graph, selected_corpora, n_clicks):
    if not n_clicks:
        return []  # Não mostra gráficos até o botão ser clicado
    
    if not selected_graph:  # Se nenhuma coluna foi selecionada
        return go.Figure().update_layout(title="Selecione valores para gerar o gráfico")
    
    # Determina o número de linhas necessárias para acomodar a quantidade necessária gráficos por linha
    num_cols = dfs[selected_graph]['graficos_por_linha']
    num_rows = math.ceil(len(selected_corpora) / num_cols)
    
    # Cria a figura de subplots para gráficos dos corpora selecionados
    fig_dynamic = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=selected_corpora)
    
    # Seleciona dataframe de acordo com o gráfico de interesse
    df = dfs[selected_graph]['df']
    x = dfs[selected_graph]['x']
    # hover_data = dfs[selected_graph]['hover_data']

    # Adiciona um gráfico de barras para cada corpus selecionado
    for i, value in enumerate(selected_corpora):
        row = (i // num_cols) + 1
        col = (i % num_cols) + 1
        fig_dynamic.add_trace(
            go.Bar(x=x[value], y=df[value],
                   name = '',
                   marker_color=dict_cores[value],
                   showlegend=False,
                   hovertemplate="%{customdata}<br>Ocorrência: %{y:.2f}%",
                   customdata=[dfs[selected_graph]['hover_data'][value].get(xx) for xx in x[value]]),
            row=row, col=col
        )

    # Atualiza o layout da figura com os gráficos dos corpora selecionados
    fig_dynamic.update_layout(height=350 * num_rows, title_text=dfs[selected_graph]['titulo_do_grafico'], showlegend=False)

    # Retorna o gráfico dos corpora selecionados como um componente Graph do Dash
    return dcc.Graph(figure=fig_dynamic, config={'displayModeBar': False})

#######################
## MONTA O DASHBOARD ##
#######################

# Layout do app
app.layout = html.Div([
    # Coluna à esquerda
    html.Div([
        # Seletor de tipo do gráfico
        html.H2("Parâmetro"),

        dcc.Dropdown(
            id="dropdown-grafico",
            options=[
                {"label": "c-letras", "value": "c"},
                {"label": "r-letras", "value": "r"},
                {"label": "genera de tipos acordais", "value": "genera"},
                {"label": "tipos acordais", "value": "tas"},
                {"label": "acordes específicos", "value": "ac_espec"}
            ],
            placeholder="Selecione"
        ),

        # Seletor de corpora
        html.H2("Corpora"),

        dcc.Dropdown(
            id="dropdown-corpora",
            options=sorted(dfs['c']['df'].columns.values.tolist()),
            value=[],
            multi=True,
            placeholder="Selecione"
        ),
        
        # Botão para gerar gráficos
        html.Button("Gerar Gráficos", id="generate-button", style={
                "backgroundColor": "#4CAF50",  # Cor de fundo verde
                "color": "white",              # Cor do texto
                "border": "none",              # Sem borda padrão
                "padding": "10px 20px",        # Espaçamento
                "fontSize": "16px",            # Tamanho da fonte
                "borderRadius": "12px",        # Bordas arredondadas
                "cursor": "pointer",           # Cursor de ponteiro
                "marginTop": "10px",
                "transition": "0.3s"           # Efeito de transição para hover
            }
        ),
    ], style={"width": "10%", "display": "inline-block", "verticalAlign": "top", "padding": "20px"}),

    # Coluna à direita para os gráficos dos corpora selecionados
    html.Div([
        # Área onde os gráficos dos corpora selecionados serão exibidos
        html.Div(id="dynamic-charts-container")
    ], style={"width": "85%", "display": "inline-block", "verticalAlign": "top", "padding": "20px", "overflowY": "auto", "height": "100%"})

], style={"height": "95vh", "margin": "0", "padding": "0", "overflow": "hidden", "display": "flex", "fontFamily": "Helvetica, sans-serif"}) 
# style={"height": "100vh", "margin": "0", "padding": "0", "overflow": "hidden", "display": "flex", "fontFamily": "Helvetica, sans-serif"})

######################
## RODA O DASHBOARD ##
######################

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))

# if __name__ == "__main__":
    # app.run_server(debug=True)
