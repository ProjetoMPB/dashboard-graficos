import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import carrega_dados
import math

############################
## INICIALIZA O DASHBOARD ##
############################

app = dash.Dash(__name__)

######################
## CARREGA OS DADOS ##
######################

df = carrega_dados.carrega_c_letras()
x = df.index.values.tolist()
x_extenso = {'u': 'Uníssono',
             'P': 'Passo ascendente',
             'p': 'Passo descendente',
             'A': 'Arpejo ascendente',
             'a': 'Arpejo descendente',
             'S': 'Salto ascendente',
             's': 'salto descendente'}

#########################
## DICIONARIO DE CORES ##
#########################

dict_cores = {}

for corpus in df.columns.values.tolist():
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
    Input("generate-button", "n_clicks"),
    State("dropdown", "value")
)

def update_dynamic_charts(n_clicks, selected_values):#, dict_cores):
    if not n_clicks:
        return []  # Não mostra gráficos até o botão ser clicado
    
    # Determina o número de linhas necessárias para acomodar 4 gráficos por linha
    num_cols = 4
    num_rows = math.ceil(len(selected_values) / num_cols)
    
    # Cria a figura de subplots para gráficos dos corpora selecionados
    fig_dynamic = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=selected_values)
    
    # Adiciona um gráfico de barras para cada corpus selecionado
    for i, value in enumerate(selected_values):
        row = (i // num_cols) + 1
        col = (i % num_cols) + 1
        fig_dynamic.add_trace(
            go.Bar(x=x, y=df[value],
                   name = '',
                   marker_color=dict_cores[value],
                   showlegend=False,
                   hovertemplate="Movimento: %{customdata}<br>Ocorrência: %{y:.2f}%",
                   customdata=[x_extenso.get(xx) for xx in x]),
            row=row, col=col
        )

    # Atualiza o layout da figura com os gráficos dos corpora selecionados
    fig_dynamic.update_layout(height=350 * num_rows, title_text="Porcentagem de ocorrência das c-letras em cada corpus selecionado", showlegend=False)
    
    # Retorna o gráfico dos corpora selecionados como um componente Graph do Dash
    return dcc.Graph(figure=fig_dynamic, config={'displayModeBar': False})

#######################
## MONTA O DASHBOARD ##
#######################

# Layout do app
app.layout = html.Div([
    # Coluna à esquerda
    html.Div([
        html.H2("Corpora"),
        # Seletor de corpora
        dcc.Dropdown(
            id="dropdown",
            options=sorted(df.columns.values.tolist()),
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
            }),
        
    ], style={"width": "10%", "display": "inline-block", "verticalAlign": "top", "padding": "20px"}),

    # Coluna à direita para os gráficos dos corpora selecionados
    html.Div([
        # Área onde os gráficos dos corpora selecionados serão exibidos
        html.Div(id="dynamic-charts-container")
        
    ], style={"width": "85%", "display": "inline-block", "padding": "20px", "verticalAlign": "top", 
                "overflowY": "auto", "height": "100%"})

], style={"height": "100vh", "margin": "0", "padding": "0", "overflow": "hidden", "display": "flex", "fontFamily": "Helvetica, sans-serif"})

######################
## RODA O DASHBOARD ##
######################

if __name__ == "__main__":
    app.run_server(debug=True)