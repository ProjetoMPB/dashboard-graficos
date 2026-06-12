from dash import Dash, State, html, dcc, callback, Output, Input
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from collections import Counter
from plotly.graph_objects import Figure
import os

######################
## CARREGA OS DADOS ##
######################

df_contorno=pd.read_csv("https://raw.githubusercontent.com/ProjetoMPB/mpb-corpus/refs/heads/main/dataset/contour_rhythm.csv",keep_default_na=False)
df_harmonia=pd.read_csv("https://raw.githubusercontent.com/ProjetoMPB/mpb-corpus/refs/heads/main/dataset/harmony.csv")
df_nota_fun=pd.read_csv('https://raw.githubusercontent.com/ProjetoMPB/mpb-corpus/refs/heads/main/dataset/note_function.csv')
artistas = sorted(list(set(df_contorno["corpus_id"].tolist())))
arts_dict={'João Bosco': 'BOSCO',
                           'Caetano Veloso': 'CAETANO',
                           'Chico Buarque': 'CHICO',
                           'Djavan': 'DJAVAN',
                           'Edu Lobo': 'EDU',
                           'Gilberto Gil': 'GIL',
                           'Tom Jobim': 'JOBIM',
                           'Ivan Lins': 'LINS',
                           'Milton Nascimento': 'MILTON',
                           'Rita Lee': 'RITA'}

############################
## INICIALIZA O DASHBOARD ##
############################

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
            meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
    ])

server = app.server

###############
## DASHBOARD ##
###############

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Dashboard Projeto MPB",
                        className="text-center fs-1, mb-4"), width=12)
    ]),

    dbc.Row([
        dbc.Col(html.H6(["Entenda a base de dados acessando",
                        html.Br(),
                        html.A(
                        "projetompb.com.br",
                        href="https://projetompb.com.br/",
                        style={
                            "color": "blue",
                            "textDecoration": "none"
                        }
                    )],
                    className="text-center fs-1, mb-4"), width=12)
    ]),

    dbc.Row([
        dbc.Col(html.H3("Selecione o parâmetro",  className="text-center fs-1, mb-4"),
                          width={"size": 12, "offset": 0, "order": 1})
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Dropdown(id="dropdown-par", options=['c-letras', 'r-letras', 'Tipos acordais', 'Categorias funcionais', 'Teia de notas-função'], labels= {'search': 'Procurar'}, className="mb-4"),
            width={"size": 4, "offset": 4, "order": 1})
            ]),
            
    dbc.Row([
        dbc.Col(
            html.Div(id="info")
            )
    ]),        

    dbc.Row([
        dbc.Col(html.H4("Selecione os artistas",  className="text-center fs-1, mb-4"),
                          width={"size": 12, "offset": 0, "order": 1})
    ]),

    dbc.Row([
        dbc.Col(dcc.Dropdown(id="dropdown-art", multi= True,  options= [{"label": 'João Bosco', "value": 'BOSCO'},
                                                                        {"label": 'Caetano Veloso', "value": 'CAETANO'},
                                                                        {"label": 'Chico Buarque', "value": 'CHICO'},
                                                                        {"label": 'Djavan', "value": 'DJAVAN'},
                                                                        {"label": 'Edu Lobo', "value": 'EDU'},
                                                                        {"label": 'Gilberto Gil', "value": 'GIL'},
                                                                        {"label": 'Tom Jobim', "value": 'JOBIM'},
                                                                        {"label": 'Ivan Lins', "value": 'LINS'},
                                                                        {"label": 'Milton Nascimento', "value": 'MILTON'},
                                                                        {"label": 'Rita Lee', "value": 'RITA'},
                                                                        ], labels={
            'select_all': 'selecionar todos',
            'deselect_all': 'limpar a seleção',
            'search': 'Procurar'}),
            width={"size": 12, "offset": 0, "order": 1}, className="mb-4")
    ]),

    dbc.Row([
        dbc.Col(html.Div(id="dropdown-ext",children=[
            html.H5("Selecione as músicas", className="text-center fs-1, mb-4"),
            dcc.Dropdown(id="dropdown-mus", multi= True, options=[], maxHeight=300)
                ], style={"display": "none"}))
    ]),

#aqui entram os gráficos
    dbc.Row([
        dbc.Col(html.Div(id="graf"))
        ])
])
@callback(
    Output(component_id="dropdown-ext", component_property="style"),
    Input(component_id="dropdown-par", component_property="value"),
    )
def mostra_drop(input_par):
    if input_par == 'Teia de notas-função':
        return {"display": "block"}
    return {"display": "none"}

@callback(
    Output(component_id="dropdown-mus", component_property="options"),
    Input(component_id="dropdown-art", component_property="value"),
    )
def drop_mus(input_art):
    options = []
    if input_art==None or input_art==[]:
        return []
    else:
        for i in input_art:
            art_lab = next(k for k, v in arts_dict.items() if v == i)
            musicas = list(
                dict.fromkeys(
                    df_nota_fun[df_nota_fun["corpus_id"] == i]["composition_name"].tolist()
                    ))
            for musica in musicas:
                options.append({
                    "label": f"{musica} - {art_lab}",
                    "value": musica})
    return options
    

@callback(
    Output(component_id="graf", component_property="children"),
    Input(component_id="dropdown-par", component_property="value"),
    Input(component_id="dropdown-art", component_property="value"),
    Input(component_id="dropdown-mus", component_property="value")
)
def gera_graficos(input_par, input_art, input_mus):
#deixa zerado antes de qualquer input
    if input_par is None:
        return []
    
    if input_art is None or input_art == []:
        return []
    
    if input_par == "c-letras":
#cria lista vazia para graficos
        grafs = []
#itera para cada grafico
        for i in input_art:
#junta todas as palavras usadas pelo artista
            art_lab = next(k for k, v in arts_dict.items() if v == i)
            c = "".join(
                df_contorno[df_contorno["corpus_id"] == i]["c_word"].tolist()
                )
#conta o numero de apariçoes de cada letra e gera um dicionario
            di = {k: Counter(c)[k]
            for k in ['u', 'p', 'P', 'a', 'A', 's', 'S']
            }
#calcula porcentagem de uso
            porcentagem = [
        (v / sum(di.values())) *100 
        for v in di.values()
        ]
#gera os graficos
            fig = px.bar(
                x=list(di.keys()),
                y=list(porcentagem),
                labels={
                    "x": "Letras",
                    "y": "Porcentagem de uso"
                },
                title=art_lab
            )
#centraliza o titulo
            fig.update_layout(title_x=0.5)
#da nome pra cada letra
            labels = {
        'u': 'Uníssono',
        'p': 'Passo descendente',
        'P': 'Passo ascendente',
        'a': 'Arpejo descendente',
        'A': 'Arpejo ascendente',
        's': 'Salto descendente',
        'S': 'Salto ascendente'
    }
    #gera uma lista com os novos nomes e com os valores de aparição
            customdata = [
        [
            labels[k],
            v
        ]
        for k, v in di.items()
    ]
    #define o hover
            fig.update_traces(
                customdata=customdata,
        hovertemplate=
        f"Artista: {art_lab}<br>" +
        "c-letra: %{x}<br>" +
        "Descrição da c-letra: %{customdata[0]}<br>" +
        "Percentual de uso: %{y:.2f}%<br>" +
        "Número de usos da letra: %{customdata[1]}<br>" +
        "<extra></extra>"
    )
    #adiciona cada grafico em uma coluna 
            grafs.append(
                dbc.Col(
                    dcc.Graph(figure=fig),
                    width=4
                )
            )
    # caso a row encha ele automaticamente cria uma nova
        return dbc.Row(grafs)

    if input_par == "r-letras":
#cria lista vazia para graficos
        grafs = []
#itera para cada grafico
        for i in input_art:
#junta todas as palavras usadas pelo artista
            art_lab = next(k for k, v in arts_dict.items() if v == i)
            c = "".join(
                df_contorno[df_contorno["corpus_id"] == i]["r_word"].tolist()
                )
#conta o numero de apariçoes de cada letra e gera um dicionario
            di = {k: Counter(c)[k]
            for k in ['a', 'b', 'c', 'd', 'e', 'f', 'g','h', 'i', 'j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
            }
#calcula porcentagem de uso
            porcentagem = [
        (v / sum(di.values())) *100 
        for v in di.values()
        ]
#gera os graficos
            fig = px.bar(
                x=list(di.keys()),
                y=list(porcentagem),
                labels={
                    "x": "Letras",
                    "y": "Porcentagem de uso"
                },
                title=art_lab
            )
#centraliza o titulo
            fig.update_layout(title_x=0.5)
#da nome pra cada letra
            labels = {
        'a': '□□□□ □□□□ □□□□',
        'b': '■□□□ □□□□ □□□□',
        'c': '□□□■ □□□□ □□□□',
        'd': '□□□□ ■□□□ □□□□',
        'e': '□□□□ □□■□ □□□□',
        'f': '□□□□ □□□□ ■□□□',
        'g': '□□□□ □□□□ □■□□',
        'h': '■□□■ □□□□ □□□□',
        'i': '■□□□ ■□□□ □□□□',
        'j': '■□□□ □□■□ □□□□',
        'k': '■□□□ □□□□ ■□□□',
        'l': '■□□□ □□□□ □■□□',
        'm': '□□□■ □□■□ □□□□',
        'n': '□□□■ □□□□ □■□□',
        'o': '□□□□ ■□□□ ■□□□',
        'p': '□□□□ □□■□ □■□□',
        'q': '■□□■ □□■□ □□□□',
        'r': '■□□■ □□□□ □■□□',
        's': '■□□□ ■□□□ ■□□□',
        't': '■□□□ □□■□ □■□□',
        'u': '□□□■ □□■□ □■□□',
        'v': '■□□■ □□■□ □■□□',
        'w': '■□□□ □□■□ ■□■□',
        'x': '■□□■ □□■□ ■□■□',
        'y': '□□■□ ■□■□ ■□■□',
        'z': '■□■□ ■□■□ ■□■□'
    }
    #gera uma lista com os novos nomes e com os valores de aparição
            customdata = [
        [
            labels[k],
            v
        ]
        for k, v in di.items()
    ]
    #define o hover
            fig.update_traces(
                customdata=customdata,
        hovertemplate=
        f"Artista: {art_lab}<br>" +
        "r-letra: %{x}<br>" +
        "Pontos de ataque: %{customdata[0]}<br>" +
        "Percentual de uso: %{y:.2f}%<br>" +
        "Número de usos da letra: %{customdata[1]}<br>" +
        "<extra></extra>"
    )
    #adiciona cada grafico em uma coluna 
            grafs.append(
                dbc.Col(
                    dcc.Graph(figure=fig),
                    width=12

                )
            )
    # caso a row encha ele automaticamente cria uma nova
        return dbc.Row(grafs)
    
    if input_par == "Tipos acordais":
#cria lista vazia para graficos
        grafs = []
#itera para cada grafico
        for i in input_art:
            art_lab = next(k for k, v in arts_dict.items() if v == i)
#puxa uma lista com todos os acordes usados
            c = df_harmonia[df_harmonia["corpus_id"] == i]["chord_symbol"].tolist()
#conta os mais usados e gera porcentagem
            di = Counter(c)
            di_20 = dict(di.most_common(20))
            porcentagem = [
            (v / sum(di.values())) *100 
            for v in di_20.values()
            ]
#gera os graficos
            fig = px.bar(
                x=list(di_20.keys()),
                y=list(porcentagem),
                labels={
                    "x": "Tipos de acorde",
                    "y": "Porcentagem de uso"
                },
                title=art_lab
            )
            fig.update_layout(title_x=0.5)
            customdata= [
        [
            v
        ]
        for v in di_20.values()
    ]
    #define o hover
            fig.update_traces(customdata=customdata,
        hovertemplate=
        f"Artista: {art_lab}<br>" +
        "Tipo de acorde: %{x}<br>" +
        "Percentual de uso: %{y:.2f}%<br>" +
        "Número de usos do acorde: %{customdata[0]}<br>" +
        "<extra></extra>"
    )
    #adiciona cada grafico em uma coluna 
            grafs.append(
                dbc.Col(
                    dcc.Graph(figure=fig),
                    width=12

                )
            )
    # caso a row encha ele automaticamente cria uma nova
        return dbc.Row(grafs)
    
    if input_par == "Categorias funcionais":
#cria lista vazia para graficos
        grafs = []
#itera para cada grafico
        for i in input_art:
            art_lab = next(k for k, v in arts_dict.items() if v == i)
    #puxa uma lista com todos os acordes usados
            c = df_harmonia[df_harmonia["corpus_id"] == i]["functional_category"].tolist()
    #conta os mais usados e gera porcentagem
            di = Counter(c)
            di_20 = dict(di.most_common(20))
            porcentagem = [
            (v / sum(di.values())) *100 
            for v in di_20.values()
            ]
    #gera os graficos
            fig = px.bar(
                x=list(di_20.keys()),
                y=list(porcentagem),
                labels={
                    "x": "Categoria do Acorde",
                    "y": "Porcentagem de uso"
                },
                title=art_lab
            )
            fig.update_layout(title_x=0.5)
            customdata= [
        [
            v
        ]
        for v in di_20.values()
    ]
    #define o hover
            fig.update_traces(customdata=customdata,
        hovertemplate=
        f"Artista: {art_lab}<br>" +
        "Categoria funcional: %{x}<br>" +
        "Percentual de uso: %{y:.2f}%<br>" +
        "Número de usos: %{customdata[0]}<br>" +
        "<extra></extra>"
    )
    #adiciona cada grafico em uma coluna 
            grafs.append(
                dbc.Col(
                    dcc.Graph(figure=fig),
                    width=12

                )
            )
    # caso a row encha ele automaticamente cria uma nova
        return dbc.Row(grafs)
    
    if input_par == "Teia de notas-função":
        grafs=[]
        if input_mus==None or input_mus==[]:
            return []
        else:
            for i in input_mus:
                art1= df_nota_fun[df_nota_fun["composition_name"] == i]["corpus_id"].tolist() 
                art2= art1[0]
                art_lab = next(k for k, v in arts_dict.items() if v == art2)                                                     
                m = df_nota_fun[df_nota_fun["composition_name"] == i]["mode"].tolist()
                modo = m[0]
                notas = df_nota_fun[df_nota_fun["composition_name"] == i]["scale_degree"].tolist()
                funcoes = df_nota_fun[df_nota_fun["composition_name"] == i]["note_function"].tolist()
                # nf_prime = list(zip(funcoes, notas))
                funcoes_dic = {'x': "Inflexão",
                            '1': "Notas triadicas (1,3 e 5)", '3': "Notas triadicas (1,3 e 5)", '5': "Notas triadicas (1,3 e 5)",
                            '6': "Sétima/Sexta (6 e 7)", '7': "Sétima/Sexta (6 e 7)",
                            '9': "Tensão simples (9, 11, 13 e 14)", '11': "Tensão simples (9, 11, 13 e 14)",
                            '13': "Tensão simples (9, 11, 13 e 14)", '14': "Tensão simples (9, 11, 13 e 14)",
                            'b9/#9': "Tensão alterada (b9/#9, #11 e b13)",
                            '#11': "Tensão alterada (b9/#9, #11 e b13)", 'b13': "Tensão alterada (b9/#9, #11 e b13)"}
                funcoes_hover = [funcoes_dic[x] for x in funcoes]
                nf_custom = list(zip(funcoes_hover, notas))
                raio = {'x': 1,
                            '1': 2, '3': 2, '5': 2,
                            '6': 3, '7': 3,
                            '9': 4, '11': 4, '13': 4, '14': 4,
                            'b9/#9': 5, '#11': 5, 'b13': 5}
                raio_funcao = [raio[x] for x in funcoes]
                if modo == "minor":
                    angulo = {'1': 90,
                                '#1/b2': 60,
                                '2': 30,
                                '3': 0,
                                '#3': 330,
                                '4': 300,
                                '#4/b5': 270,
                                '5': 240,
                                '6': 210,
                                '#6': 180,
                                'b7': 150,
                                '7': 120}
                    angulo_nota = [angulo[x] for x in notas]
                if modo == "major":
                    angulo = {'1': 90,
                                '#1/b2': 60,
                                '2': 30,
                                '#2/b3': 0,
                                '3': 330,
                                '4': 300,
                                '#4/b5': 270,
                                '5': 240,
                                '#5/b6': 210,
                                '6': 180,
                                '#6/b7': 150,
                                '7': 120}
                    angulo_nota = [angulo[x] for x in notas]
                nf = list(zip(raio_funcao, angulo_nota))
                nf_contagem = Counter(nf)
                ordenado = sorted(nf_contagem.items(),
                                key=lambda x: x[1],  # ordena pela contagem
                                reverse=True
                                )
                keys = [k for k, v in ordenado]
                porcentagem = [
                    100 * v / sum(nf_contagem.values())
                    for k, v in ordenado
                    ]
                porcentagem_dict = dict(zip(keys, porcentagem))
                porcentagem_array = [porcentagem_dict[x] for x in nf]

                def faixa(p):
                    if p < 2:
                        return "0% ~ 2%"
                    elif p < 4:
                        return "2% ~ 4%"
                    elif p < 6:
                        return "4% ~ 6%"
                    elif p < 8:
                        return "6% ~ 8%"
                    elif p < 10:
                        return "8% ~ 10%"
                    else:
                        return "> 10%"

                # faixas = [faixa(p) for p in porcentagem_array]

                # cores = {
                #     "0% ~ 2%": "#1200A8",
                #     "2% ~ 4%": "#6A00C8",
                #     "4% ~ 6%": "#B12A9B",
                #     "6% ~ 8%": "#D95F5F",
                #     "8% ~ 10%": "#F5A832",
                #     "> 10%": "#EAEA1A"
                # }

                # fig = px.scatter_polar(r=raio_funcao,
                #                        theta=angulo_nota,
                #                        color=faixas,
                #                        color_discrete_map = cores,
                #                        category_orders={
                #                            "color": [
                #                                "0% ~ 2%",
                #                                "2% ~ 4%",
                #                                "4% ~ 6%",
                #                                "6% ~ 8%",
                #                                "8% ~ 10%",
                #                                "> 10%"]})

                fig = px.scatter_polar(r=raio_funcao, theta=angulo_nota, color=porcentagem_array, color_continuous_scale=[ "#1200A8", "#6A00C8", "#B12A9B", "#D95F5F", "#F5A832", "#EAEA1A"])

                
                fig.update_layout(coloraxis_colorbar=dict(
                    title="Porcentagem de occorrencia",
                    tickvals=[1, 3, 5, 7, 9, 11],
                    ticktext=[
                        "0%-2%",
                        "2%-4%",
                        "4%-6%",
                        "6%-8%",
                        "8%-10%",
                        ">10%"]),coloraxis=dict(cmin=0,cmax=12),title={"text": f"{i} - {art_lab}", "x": 0.435, "xanchor": "center"})
                        
                
                if modo == "major":
                    fig.update_layout(polar=dict(angularaxis=dict(
                        tickmode="array",
                        tickvals=[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330],
                        ticktext=["", "2", "", "1", "7", "", "6", "", "5", "","4","3"]), radialaxis=dict(
                        range=[0, 5],
                        tickmode="array",
                        tickvals=[0, 1, 2, 3, 4, 5],
                        ticktext=["", "", "", "", "",""])))
                
                if modo == "minor":
                    fig.update_layout(polar=dict(angularaxis=dict(
                        tickmode="array",
                        tickvals=[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330],
                        ticktext=["3", "2", "", "1", "", "7", "", "6", "5", "","4",""]), radialaxis=dict(
                        range=[0, 5],
                        tickmode="array",
                        tickvals=[0, 1, 2, 3, 4, 5],
                        ticktext=["", "", "", "", "", ""])))
                    
                fig.update_traces(customdata=nf_custom,
                                hovertemplate=
                                f"Artista: {art_lab}<br>" +
                                f"Música: {i}<br>" +
                                "Grau escalar: %{customdata[1]}<br>" +
                                "Nota-função: %{customdata[0]}<br>" +
                                "Porcentagem de uso: %{marker.color:.2f}%<br>" +
                                "<extra></extra>"
                                )
                grafs.append(dbc.Col(dcc.Graph(figure=fig),width=6))
        return dbc.Row(grafs)

    
@callback(
    Output(component_id="info", component_property="children"),
    Input(component_id="dropdown-par", component_property="value")
    )
def info(input_par):
    if input_par == None:
        return None

    if input_par == "Tipos acordais":
        return dbc.Col(html.H6(
            ["Aqui ""*"" representa uma fundamental genérica.",
            html.Br(),
            "Pela grande quantidade de tipos acordais diferentes, mostramos aqui os 20 mais recorrentes no repertório dos artistas selecionados."],
            className="text-center fs-1, mb-4"), width={"size": 12, "offset": 0, "order": 1})
    
    if input_par == "Categorias funcionais":
        return dbc.Col(html.H6(
            "Pela grande quantidade de categorias funcionais diferentes, mostramos aqui as 20  mais recorrentes no repertório dos artistas selecionados.",
                               className="text-center fs-1, mb-4"), width={"size": 12, "offset": 0, "order": 1})

######################
## RODA O DASHBOARD ##
######################

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))

# if __name__ == "__main__":
#     app.run(debug=True)
