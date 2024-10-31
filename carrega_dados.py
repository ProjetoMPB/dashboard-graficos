import pandas as pd

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

    c_palavras_pct_dict = {}

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
        
        c_palavras_pct_dict[corpus] = prv

    c_palavras_pct_df = pd.DataFrame(c_palavras_pct_dict, index = ['u', 'P', 'p', 'A', 'a', 'S','s'])

    return c_palavras_pct_df

def carrega_r_letras():
    # abrir a lista acumulada de c-palavras
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
        # Iniciar a contabilização de r-letras
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
            
        # criar legenda do r-alfabeto para plotagem
        leg=[]
        
        for i in range(0,26,1):
            a=chr(i+97)
            leg.append(a)
        
        vetor_r_letras=[]
        x=len(perc)
        #prv=[]       
        for i in range(0,x):
            a=leg[i]
            b=perc[i]
            #print(b)
            #prv.append(a)
            #prv.extend(b)
            vetor_r_letras.append(b)
        dados.append(vetor_r_letras)
        #print(dados)