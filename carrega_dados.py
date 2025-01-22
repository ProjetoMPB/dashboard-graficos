import json

import pandas as pd


def carrega_c_letras():
    df = pd.read_csv(r'resultados\2M2b.csv', index_col=0)
    df *= 100
    corpora = df.index.tolist()

    saida = {
        'df': df,
        'x': {corpus: ['u', 'P', 'p', 'A', 'a', 'S', 's'] for corpus in corpora},
        'hover_data': {
            corpus: {
                'u': 'Movimento: Uníssono',
                 'P': 'Movimento: Passo ascendente',
                 'p': 'Movimento: Passo descendente',
                 'A': 'Movimento: Arpejo ascendente',
                 'a': 'Movimento: Arpejo descendente',
                 'S': 'Movimento: Salto ascendente',
                 's': 'Movimento: salto descendente'
            } for corpus in corpora
        },
        'graficos_por_linha': 4,
        'titulo_do_grafico': 'Porcentagem de ocorrência das c-letras em cada corpus selecionado'
    }

    return saida


def carrega_r_letras():
    df = pd.read_csv(r'resultados\2M3d.csv', index_col=0)
    df = df.fillna(0).sort_index()
    df *= 100
    corpora = df.index.tolist()

    saida = {
        'df': df,
        'x': {corpus: list("abcdefghijklmnopqrstuvwxyz") for corpus in corpora},
        'hover_data': {
             corpus: {
                 'a': 'Pontos de ataque: □□□ □□□ □□□ □□□',
                 'b': 'Pontos de ataque: ■□□ □□□ □□□ □□□',
                 'c': 'Pontos de ataque: □□□ ■□□ □□□ □□□',
                 'd': 'Pontos de ataque: □□□ □■□ □□□ □□□',
                 'e': 'Pontos de ataque: □□□ □□□ ■□□ □□□',
                 'f': 'Pontos de ataque: □□□ □□□ □□■ □□□',
                 'g': 'Pontos de ataque: □□□ □□□ □□□ ■□□',
                 'h': 'Pontos de ataque: ■□□ ■□□ □□□ □□□',
                 'i': 'Pontos de ataque: ■□□ □■□ □□□ □□□',
                 'j': 'Pontos de ataque: ■□□ □□□ ■□□ □□□',
                 'k': 'Pontos de ataque: ■□□ □□□ □□■ □□□',
                 'l': 'Pontos de ataque: ■□□ □□□ □□□ ■□□',
                 'm': 'Pontos de ataque: □□□ ■□□ ■□□ □□□',
                 'n': 'Pontos de ataque: □□□ ■□□ □□□ ■□□',
                 'o': 'Pontos de ataque: □□□ □■□ □□■ □□□',
                 'p': 'Pontos de ataque: □□□ □□□ ■□□ ■□□',
                 'q': 'Pontos de ataque: ■□□ ■□□ ■□□ □□□',
                 'r': 'Pontos de ataque: ■□□ ■□□ □□□ ■□□',
                 's': 'Pontos de ataque: ■□□ □■□ □□■ □□□',
                 't': 'Pontos de ataque: ■□□ □□□ ■□□ ■□□',
                 'u': 'Pontos de ataque: □□□ ■□□ ■□□ ■□□',
                 'v': 'Pontos de ataque: ■□□ ■□□ ■□□ ■□□',
                 'w': 'Pontos de ataque: ■□□ □□□ ■□■ □■□',
                 'x': 'Pontos de ataque: ■□□ ■□□ ■□■ □■□',
                 'y': 'Pontos de ataque: □□■ □■□ ■□■ □■□',
                 'z': 'Pontos de ataque: ■□■ □■□ □■□ □■□'
             } for corpus in corpora
         },
        'graficos_por_linha': 2,
        'titulo_do_grafico': 'Porcentagem de ocorrência das r-letras em cada corpus selecionado'
    }

    return saida


def carrega_genera():
    df = pd.read_csv(r'resultados\2H2b.csv', index_col=0)
    df *= 100
    corpora = df.index.tolist()

    saida = {
        'df': df,
        'x': {corpus: df.columns.tolist() for corpus in corpora},
        'hover_data': {
            corpus: {
                'Z': 'Genera: _M7',
                'Y': 'Genera: _7',
                'X': 'Genera: _(♭5)7',
                'W': 'Genera: _(♯5)7',
                'V': 'Genera: _ (tríade maior)',
                'z': 'Genera: _m7',
                'y': 'Genera: _ø',
                'x': 'Genera: _°7',
                'w': 'Genera: _m(M7)',
                'v': 'Genera: _m',
            } for corpus in corpora
        },
        'graficos_por_linha': 4,
        'titulo_do_grafico': 'Porcentagem de ocorrência dos genera de tipos acordais em cada corpus selecionado'
    }

    return saida


def carrega_tipos_acordais():
    df = pd.read_csv(r'resultados\2HD1.csv', index_col=0)
    df *= 100

    with open("lexico-tipos-acordais.json", "r", encoding="utf-8") as f:
        lexico_tipos_acordais = json.load(f)

    corpus_to_series = {corpus: df.loc[corpus].sort_values(ascending=False).dropna().head(40) for corpus in df.index}

    saida = {
        'df': pd.DataFrame([series.reset_index(drop=True) for series in corpus_to_series.values()]),
        'x': {corpus: series.index.tolist() for corpus, series in corpus_to_series.items()},
        'hover_data': {
            corpus: {
                ta: 'Tipo acordal: _' + lexico_tipos_acordais.get(ta, 'NaN') for ta in series.index
            } for corpus, series in corpus_to_series.items()
        },
        'graficos_por_linha': 1,
        'titulo_do_grafico': 'Porcentagem de ocorrência dos 40 tipos acordais mais comuns em cada corpus selecionado'
    }
    return saida


def carrega_acordes_especificos():
    df = pd.read_csv(r'resultados\2HD2.csv', index_col=0)
    df *= 100

    with open("lexico-tipos-acordais.json", "r") as f:
        lexico_tipos_acordais = json.load(f)

    # "inverte" dicionario de tipos acordais para cifra
    lexico_tipos_acordais = {v: k for k, v in lexico_tipos_acordais.items()}

    corpus_to_series = {corpus: df.loc[corpus].sort_values(ascending=False).dropna().head(40) for corpus in df.index}

    saida = {
        'df': pd.DataFrame([series.reset_index(drop=True) for series in corpus_to_series.values()]),
        'x': {corpus: series.index.tolist() for corpus, series in corpus_to_series.items()},
        'hover_data': {
            corpus: {
                acorde: f"Acorde: {acorde}" for acorde in series.head(40).index
            } for corpus, series in corpus_to_series.items()
        },
        'graficos_por_linha': 1,
        'titulo_do_grafico': 'Porcentagem de ocorrência dos 40 acordes específicos mais comuns em cada corpus selecionado'
    }
    return saida