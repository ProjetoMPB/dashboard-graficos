import pandas as pd
from collections import Counter

def carrega_c_letras():
    # abrir a lista acumulada de c-palavras
    c_palavras=[]
    with open('c_palavras_corpora.txt', 'r') as file:
        for linha in file:
            c_palavras.append(linha)

    # normalização
    x=c_palavras
    c_palavras1=[]

    # Remover as aspas externas de cada elemento
    x = [item.strip("'") for item in x]

    # Converter cada elemento em uma lista usando eval()
    x = [eval(item) for item in x]

    # Imprimir nova lista
    for item in x:
        c_palavras1.extend(item)

    c_palavras1_dict = {c_palavras1[k]:c_palavras1[k + 1] for k in range(0, len(c_palavras1) - 1, 2)}

    c_letras_pct_dict = {}

    for corpus in c_palavras1_dict.keys():
        # Iniciar a contabilização de c-letras
        # vetor c-letras
        v_c_letras=7*[0]

        prv=[]
        for k in c_palavras1_dict[corpus]:
            a=k
            for j in a:
                if j=='u':
                    v_c_letras[0]=v_c_letras[0]+1
                elif j=='P':
                    v_c_letras[1]=v_c_letras[1]+1  
                elif j=='p':
                    v_c_letras[2]=v_c_letras[2]+1  
                elif j=='A':
                    v_c_letras[3]=v_c_letras[3]+1  
                elif j=='a':
                    v_c_letras[4]=v_c_letras[4]+1  
                elif j=='S':
                    v_c_letras[5]=v_c_letras[5]+1  
                elif j=='s':
                    v_c_letras[6]=v_c_letras[6]+1  
                    
        # Total de c-letras
        total_c_letras=sum(v_c_letras)

        # atribuindo percentuais ao vetor
        perc_c_letras = []
        tx=100/total_c_letras
        for i in v_c_letras:
            a=i*tx
            perc_c_letras.append(a)
        
        prv.extend(perc_c_letras)
        
        c_letras_pct_dict[corpus] = prv

    c_letras_pct_df = pd.DataFrame(c_letras_pct_dict, index = ['u', 'P', 'p', 'A', 'a', 'S','s'])

    ## PREPARA A SAÍDA ##

    saida = {'df': c_letras_pct_df}

    saida['x'] = pd.DataFrame({corpus:c_letras_pct_df.index.values.tolist() for corpus in c_letras_pct_dict.keys()})

    saida['hover_data'] = {corpus: {'u': 'Movimento: Uníssono',
                                    'P': 'Movimento: Passo ascendente',
                                    'p': 'Movimento: Passo descendente',
                                    'A': 'Movimento: Arpejo ascendente',
                                    'a': 'Movimento: Arpejo descendente',
                                    'S': 'Movimento: Salto ascendente',
                                    's': 'Movimento: salto descendente'} for corpus in c_letras_pct_dict.keys()}
    
    saida['graficos_por_linha'] = 4
    
    saida['titulo_do_grafico'] = 'Porcentagem de ocorrência das c-letras em cada corpus selecionado'
    
    return saida

def carrega_r_letras():
    r_letras=[]
    with open('r_letras_corpora.txt', 'r') as file:
        for linha in file:
            r_letras.append(linha)
            
    # normalização
    x=r_letras
    r_letras1=[]

    # Remover as aspas externas de cada elemento
    x = [item.strip("'") for item in x]

    # Converter cada elemento em uma lista usando eval()
    x = [eval(item) for item in x]

    # Imprimir nova lista
    for item in x:
        r_letras1.extend(item)

    r_letras1_dict = {r_letras1[k]:r_letras1[k + 1] for k in range(0, len(r_letras1) - 1, 2)}

    r_letras_pct_dict = {}

    for corpus in r_letras1_dict.keys():
        # estabelecendo o vetor de r-letras zerado (26 posições)
        r_vetor=26*[0]
        for i in r_letras1_dict[corpus]:
            a=ord(i)-97
            r_vetor[a] = r_vetor[a]+1
        
        # atribuindo percentagens
        perc=[]
        tot=sum(r_vetor)
        tx=100/tot

        for i in r_vetor:
            a=i*tx
            perc.append(a)
        
        r_letras_pct_dict[corpus] = perc

    r_letras_pct_df = pd.DataFrame(r_letras_pct_dict, index = ['a', 'b', 'c', 'd', 'e',
                                                               'f', 'g', 'h', 'i', 'j',
                                                               'k', 'l', 'm', 'n', 'o',
                                                               'p', 'q', 'r', 's', 't',
                                                               'u', 'v', 'w', 'x', 'y',
                                                               'z'])

    saida = {'df': r_letras_pct_df}

    ## PREPARA A SAÍDA ##

    saida['x'] = pd.DataFrame({corpus:r_letras_pct_df.index.values.tolist() for corpus in r_letras_pct_dict.keys()})
    
    saida['hover_data'] = {corpus: {'a': 'Pontos de ataque: □□□ □□□ □□□ □□□',
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
                                    'z': 'Pontos de ataque: ■□■ □■□ □■□ □■□'} for corpus in r_letras_pct_dict.keys()}
    
    saida['graficos_por_linha'] = 2
    
    saida['titulo_do_grafico'] = 'Porcentagem de ocorrência das r-letras em cada corpus selecionado'

    return saida

def carrega_genera_tas_acordes():
    ##### GENERICO PARA OS TRES #####
    acordes=[]
    with open('acordes_especificos_corpora.txt', 'r') as file:
        for linha in file:
            acordes.append(linha.replace('\n',''))
    
    ## ABRE LÉXICO E ARMAZENA INFOS ##
    # abrindo o LÉXICO de TAs
    LEX = pd.read_excel('LEXICO TAs - Python.xls', header = None) 
    LEX1=LEX.values.tolist()

    #separando no LÉXICO os tipos das cifras, para permitir a comparação (1) TAs
    tipos=LEX1[1]

    # separando no LÉXICO os tipos das cifras, para permitir a comparação (2) cifras
    cifras=LEX1[2] 

    # *************** MARACUTAIA PARA DAR CERTO!
    #artifício para eviatr "nan" na tríade maior (um vazio resultante da própria convenção adotada, que não emprega 
    #símbolo para denotar uma tríade maior)
    cifras[104]=''

    LEXICO_dict = {tipos[i]: cifras[i] for i in range(len(tipos))}
    ##################################

    # normalização
    x=acordes
    acordes1=[]

    # Remover as aspas externas de cada elemento
    x = [item.strip("'") for item in x]

    # Converter cada elemento em uma lista usando eval()
    x = [eval(item) for item in x]

    # Imprimir nova lista
    for item in x:
        acordes1.extend(item)

    acordes1_dict = {acordes1[k]:acordes1[k + 1] for k in range(0, len(acordes1) - 1, 2)}

    # Converter a lista string em lista numérica
    acordes2_dict = {}
    for corpus in acordes1_dict.keys():
        acordes_codificados = []
        for item in acordes1_dict[corpus]:
            if item.startswith('[') and item.endswith(']'):
                # Remove os colchetes e converte os números separados por vírgula em uma lista
                numbers = list(map(int, item[1:-1].split(', ')))
                acordes_codificados.append(numbers)
            else:
                # Converte o número de string para inteiro
                acordes_codificados.append(int(item))
        acordes2_dict[corpus] = acordes_codificados

    ##### GENERA #####

    genera_dict = {corpus:[x[1] for x in acordes2_dict[corpus]] for corpus in acordes2_dict.keys()}

    genera_dict_pct = {}

    for corpus in genera_dict.keys():
        # estabelecendo as condições de calcular as frequências dos genera no corpus
        contador_g=dict(Counter(genera_dict[corpus])) 
        # frequências dos genera
        # contador_g_freq=contador_g.values() 
        # identificação dos genera
        # contador_g_genus=contador_g.keys()  
        # ordenando decrescentemente
        contador_g_ordenados=sorted(contador_g.items(), key=lambda pair: pair[0], reverse=True)

        #Vetor genus
        v_genus=10*[0]
        
        #convertendo os valores ordenados em lista
        # g_corpus=list(contador_g_ordenados)
        
        #preenchendo o vetor
        for i in contador_g_ordenados:
            a=i[0]
            b=i[1]
            if a==90:
                v_genus[0]=v_genus[0]+b
            elif a==89:
                v_genus[1]=v_genus[1]+b
            elif a==88:
                v_genus[2]=v_genus[2]+b
            elif a==87:
                v_genus[3]=v_genus[3]+b
            elif a==86:
                v_genus[4]=v_genus[4]+b        
            elif a==122:
                v_genus[5]=v_genus[5]+b
            elif a==121:
                v_genus[6]=v_genus[6]+b        
            elif a==120:
                v_genus[7]=v_genus[7]+b
            elif a==119:
                v_genus[8]=v_genus[8]+b
            elif a==118:
                v_genus[9]=v_genus[9]+b
                
        # Estabelecendo percentuais dos 10 genera
        perc=[]
        tot=sum(v_genus)
        tx=100/tot
        
        for i in v_genus:
            perc.append(i*tx)

        genera_dict_pct[corpus] = perc

    genera_dict_pct_df = pd.DataFrame(genera_dict_pct, index = ['Z', 'Y', 'X','W','V','z','y','x','w','v'])

    saida_genera = {'df': genera_dict_pct_df}

    ## PREPARA A SAÍDA (GENERA) ##

    saida_genera['x'] = pd.DataFrame({corpus: genera_dict_pct_df.index.values.tolist() for corpus in genera_dict_pct.keys()})

    saida_genera['hover_data'] = {corpus: {'Z': 'Genera: _M7',
                                           'Y': 'Genera: _7',
                                           'X': 'Genera: _(♭5)7',
                                           'W': 'Genera: _(♯5)7',
                                           'V': 'Genera: _ (tríade maior)',
                                           'z': 'Genera: _m7',
                                           'y': 'Genera: _ø',
                                           'x': 'Genera: _°7',
                                           'w': 'Genera: _m(M7)',
                                           'v': 'Genera: _m',} for corpus in genera_dict_pct.keys()}

    saida_genera['graficos_por_linha'] = 4

    saida_genera['titulo_do_grafico'] = 'Porcentagem de ocorrência dos genera de tipos acordais em cada corpus selecionado'

    ##### TIPOS ACORDAIS #####

    tas_dict = {corpus:[tuple(x[1:3]) for x in acordes2_dict[corpus]] for corpus in acordes2_dict.keys()}

    # total_tas_dict = {corpus:len(tas_dict[corpus]) for corpus in acordes2_dict.keys()}

    tas_dict_pct = {}
    tas_dict_pct_x = {}

    for corpus in tas_dict.keys():
        # estabelecendo as condições de calcular as frequências dos TAs no corpus
        contadorTA=dict(Counter(tas_dict[corpus])) 
        # frequências dos TAs
        # contadorTA_01=contadorTA.values() 
        # identificando os TAs (genus + variantes)
        # contadorTA_02 = contadorTA.keys()
        # ordenando decrescentemente
        TAs_corpus_ordenados=sorted(contadorTA.items(), key=lambda pair: pair[1], reverse=True) 
        
        # desempacotando os TAs do corpus (ordenados)
        TAs_mais_comuns = []
        for item in TAs_corpus_ordenados:
            TAs_mais_comuns.append(item[0])
            
        # TAs distintos
        # total_TAs_distintos=len(TAs_corpus_ordenados) 
        
        # formando vetor número de TAs distintos, para armazenamento
        # TAs_dist = [total_TAs_distintos, total_tas_dict[corpus]]
                
        # traduzindo TAs do corpus
        TAs_traduzidos=[]
        x=''
        for i in TAs_mais_comuns:
            a=chr(i[0])
            b=str(i[1])
            c=a+b
            TAs_traduzidos.append(c)
            
        # desempacotando as frequências (ordenados)
        frequencias = []
        for item in TAs_corpus_ordenados:
            frequencias.append(item[1])
            
        # atribuindo percentuais 
        s=sum(frequencias)
        tx=100/s
        
        perc_freq=[]
        for i in frequencias:
            a=i*tx
            perc_freq.append(a)
        
        # limitando o número de TAs. a 40 para fins de plotagem (quando for o caso)
        if len(TAs_traduzidos)> 40:
            TAs_traduzidos_lim=TAs_traduzidos[0:40]
            frequencias_ordenadas_lim=perc_freq[0:40]
        else:
            TAs_traduzidos_lim=TAs_traduzidos
            frequencias_ordenadas_lim=perc_freq
        
        tas_dict_pct[corpus] = frequencias_ordenadas_lim
        tas_dict_pct_x[corpus] = TAs_traduzidos_lim

    ## PREPARA A SAÍDA (TIPOS ACORDAIS) ##

    # saida_tas = {'df': pd.DataFrame(tas_dict_pct)}
    saida_tas = {'df': pd.DataFrame(dict([(key, pd.Series(value)) for key, value in tas_dict_pct.items()]))} # MARACUTAIA PARA LISTAS DE TAMANHOS DISTINTOS

    # saida_tas['x'] = tas_dict_pct_x
    saida_tas['x'] = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in tas_dict_pct_x.items()])) # MARACUTAIA PARA LISTAS DE TAMANHOS DISTINTOS

    saida_tas['hover_data'] = {corpus: {ta: 'Tipo acordal: _' + LEXICO_dict.get(ta, 'NaN') for ta in saida_tas['x'][corpus]} for corpus in tas_dict_pct.keys()}

    saida_tas['graficos_por_linha'] = 1

    saida_tas['titulo_do_grafico'] = 'Porcentagem de ocorrência dos 40 tipos acordais mais comuns em cada corpus selecionado'

    ##### ACORDES ESPECÍFICOS #####

    ac_espec_dict = {corpus:[tuple(x) for x in acordes2_dict[corpus]] for corpus in acordes2_dict.keys()}

    # total_ac_espec_dict = {corpus:len(ac_espec_dict[corpus]) for corpus in acordes2_dict.keys()}

    ac_espec_dict_pct = {}

    ac_espec_dict_pct_x = {}

    for corpus in ac_espec_dict.keys():
        # estabelecendo as condições de calcular as frequências dos acordes esp. no corpus
        contador_ac=dict(Counter(ac_espec_dict[corpus])) 
        # frequências dos acordes esp.
        # contador_ac_freq=contador_ac.values() 
        #número de ac. esp. distintos no corpus
        # tot_ac_distintos = len(contador_ac)
        # formando veotr de ac. distintos
        # acordes_distintos = [tot_ac_distintos, total_ac_espec_dict[corpus]]

        # identificando os TAs
        # contador_ac_esp = contador_ac.keys() 

        # ordenando decrescentemente
        AC_corpus_ordenados=sorted(contador_ac.items(), key=lambda pair: pair[1], reverse=True) 

        # desempacotando os ac. esp. do corpus (ordenados)
        AC_mais_comuns = []

        for item in AC_corpus_ordenados:
            AC_mais_comuns.append(item[0])
            
        # traduzindo Ac. esp. mais comuns (1a parte)
        AC_traduzidos=[]
        apenas_fundamentais=[]
        apenas_TAs=[]
        x=''
        for i in AC_mais_comuns:
            x=i[0]
            if x==0:
                y='C'
            elif x==1:
                y='C#'
            elif x==2:
                y='D'   
            elif x==3:
                y='Eb'   
            elif x==4:
                y='E'
            elif x==5:
                y='F'   
            elif x==6:
                y='F#'   
            elif x==7:
                y='G'
            elif x==8:
                y='Ab'   
            elif x==9:
                y='A'   
            elif x==10:
                y='Bb'
            elif x==11:
                y='B'                    
            a=chr(i[1])
            b=str(i[2])
            c=y+a+b
            d=a+b
            AC_traduzidos.append(c)
            apenas_fundamentais.append(y)
            apenas_TAs.append(d)

        # tradução dos acordes específicos do corpus em cifras alfanuméricas
        ac_cifrados_mais_comuns=[]  
        conta=0
        for i in apenas_TAs:
            x=tipos.index(i)
            y=cifras[x]
            z=apenas_fundamentais[conta]
            w=z+y
            ac_cifrados_mais_comuns.append(w)
            conta=conta+1
            
        # desempacotando as frequências (ordenados)
        frequencias_ordenadas = []
        for item in AC_corpus_ordenados:
            frequencias_ordenadas.append(item[1])
            
        # limitando o número de acordes esp. a 40 para fins de plotagem (quando for o caso)
        if len(ac_cifrados_mais_comuns)> 40:
            ac_cifrados_mais_comuns_lim=ac_cifrados_mais_comuns[0:40]
            frequencias_ordenadas_lim=frequencias_ordenadas[0:40]
        else: 
            ac_cifrados_mais_comuns_lim=ac_cifrados_mais_comuns
            frequencias_ordenadas_lim=frequencias_ordenadas

        # percentuais
        s=sum(frequencias_ordenadas) 
        tx=100/s

        perc=[] 
        for i in frequencias_ordenadas_lim:
            a=i*tx
            perc.append(a)

        ac_espec_dict_pct[corpus] = perc
        ac_espec_dict_pct_x[corpus] = ac_cifrados_mais_comuns_lim

    ## PREPARA A SAÍDA (ACORDES ESPECÍFICOS) ##

    saida_ac_espec = {'df': pd.DataFrame(ac_espec_dict_pct)}

    saida_ac_espec['x'] = ac_espec_dict_pct_x

    saida_ac_espec['hover_data'] = {corpus: {acorde: 'Acorde: ' + acorde for acorde in ac_espec_dict_pct_x[corpus]} for corpus in ac_espec_dict_pct.keys()}

    saida_ac_espec['graficos_por_linha'] = 1

    saida_ac_espec['titulo_do_grafico'] = 'Porcentagem de ocorrência dos 40 acordes específicos mais comuns em cada corpus selecionado'

    return saida_genera, saida_tas, saida_ac_espec