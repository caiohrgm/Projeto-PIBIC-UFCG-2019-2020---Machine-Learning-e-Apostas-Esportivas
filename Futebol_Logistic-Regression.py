#!/usr/bin/env python
# coding: utf-8

# In[5]:


#import sys
#!pip3 install scikit-learn


# In[6]:


import numpy as np  
import pandas as pd  
from sklearn.linear_model import LogisticRegression
from  sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# # Classificador

# In[7]:


def logisticRegressionFutebol(ano):
    predicao = ["" for x in range(45)]
    relatorio_final = list()
    acuracia = list()
    lp_rodada = list()
    acertos = list()
    total_acertos = 0
    total_erros = 0
    oddsH_total = 0
    entradas_totais = 0
    
    df = pd.read_excel(ano) # Abrindo o arquivo e convertendo em DataFrame
    df['oddsLayH'] = 1 / (1 -1 / df['OddsH']) # cria a coluna com a oddH da aposta contra o mandante;
    df['Resultado'] = df['Resultado'].apply(lambda x: 1 if x == 'S' else 0) # converte S's em 1's e F's em 0's;
    
    df_train = df
    df_test = df.iloc[:,:20] # df_test recebe as 20 primeira colunas (sem a coluna Resultados)
    df_test['OddsH'] = df['OddsH']
    df_test['oddsLayH'] = df['oddsLayH']
    
    lm = LogisticRegression()
    for rodada in range(5,38):
        #jogos_teste = range(jogos_treino , proxima_rodada)
        rodada_treino = rodada * 10
        rodada_teste = rodada_treino + 10
        x_train = df_train.iloc[0:rodada_treino].drop('Resultado', 1) # 
        #x_train = x_train.iloc[0:rodada_treino].drop('oddsLayH',1) # Removendo a coluna de odds contrarias
        x_test = df_test.iloc[rodada_treino: rodada_teste] # define o teste para entre 1º e ultimo jogo da próxima rodada;
        y_train = df_train.iloc[0:rodada_treino]['Resultado'] # y_train recebe so a coluna de resultados do treino;
        y_test = df_train.iloc[rodada_treino:rodada_teste]['Resultado'] # y_test recebe  a coluna Resultado das rodadas de teste;
        lm.fit(x_train, y_train)
        pred = lm.predict(x_test)

        lp = 0
        i = 0
        for p in pred:
            if p == 1:
                entradas_totais = entradas_totais + 1 # controla o total de entradas de apostas como mandante;
                if p == y_test.iloc[i]:
                    acertos.append(True)
                    oddsH_total = oddsH_total + df_train.loc[rodada_treino + i, 'OddsH'] # acrescenta a oddH de entrada quando mandante;
                    lp += 100 * (df_train.loc[rodada_treino + i, 'OddsH'] - 1) # Aposta no mandante;
                else:
                    acertos.append(False)
                    oddsH_total = oddsH_total + df_train.loc[rodada_treino + i, 'OddsH'] # acrescenta a oddH de entrada quando mandante;
                    lp += -100         
            else:
                if p == y_test.iloc[i]:
                    acertos.append(True)
                    lp += 100 * (df_train.loc[rodada_treino + i, 'oddsLayH'] - 1) # Aposta no time de fora;
                else:
                    acertos.append(False)
                    lp += -100
            i = i + 1

        df_rodada =  pd.DataFrame(y_test)
        df_rodada["Previsão"] = pred
        df_rodada["Acertos/Erros"] = acertos
        acuracia_rodada = round((list(df_rodada["Acertos/Erros"]).count(True) / float(len(df_rodada['Acertos/Erros']))),2)
        acuracia.append(acuracia_rodada)  # registra a acurácia da rodada;
        lp_rodada.append(round(lp,2))    # registra o lucro/perda da rodada;

        acertos = list() # reseta a lista de acertos, para adicionar novamente a proxima rodada;

        #dis['Acerto'] = acertos(dis['Resultado'], dis['Pred'])
    
    oddsH_media = round((oddsH_total/float(entradas_totais)),2) 
    relatorio_final.append(oddsH_media)
    
    acuracia_total = 0
    for acc in acuracia:
        acuracia_total += (acc*100)
    acuracia_media = acuracia_total/33
    relatorio_final.append(acuracia_media)
    
    lp_final = 0
    for lp in lp_rodada:
        lp_final += lp
    relatorio_final.append(lp_final)
        
    #relatorio = pd.DataFrame({'Rodadas': [f'Rodada {x}' for x in range(6,39)]})
    #relatorio['Acurácia'] = acuracia
    #relatorio['Lucro/Prejuízo'] = lp_rodada
    #display(relatorio)
    
    return relatorio_final


# # Main

# In[8]:


tables = ['Premier2012x2013.xlsx', 'Premier2013x2014.xlsx', 'Premier2014x2015.xlsx', 'Premier2015x2016.xlsx',
          'Premier2016x2017.xlsx', 'Premier2017x2018.xlsx', 'Premier2018x2019.xlsx']
oddsHMedia = list()
acuraciaMedia = list()
lp_finais = list()

for table in tables:
    lista = logisticRegressionFutebol(table) # [oddsHMedia,Acurácia,L/P];
    oddsHMedia.append(lista[0])
    acc = str(round(lista[1],2))+"%"
    acuraciaMedia.append(acc)
    lp = "R$ "+str(round(lista[2],2))
    lp_finais.append(lp)

df = pd.DataFrame({'Ano': [f'201{x}x201{y}' for x,y in zip(range(2,9),range(3,10))]})
df['Acurácia Média'] = acuraciaMedia
df['OddsH Média'] = oddsHMedia
df['Lucro/Prejuízo Total'] = lp_finais
display(df)
    


# In[ ]:





# In[ ]:




