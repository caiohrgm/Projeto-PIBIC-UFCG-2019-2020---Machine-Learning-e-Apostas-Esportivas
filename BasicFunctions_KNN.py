import pandas as pd
import collections as cl

'''Define qual for o resultado mais comum (S ou F) dentre os k vizinhos anteriores'''
def selecionaMaioria(lista):
    c = cl.Counter(lista)
    maisComum, maisComum_count = c.most_common(1)[0]
    num_winners = len([count
                       for count in c.values()
                       if count == maisComum_count])
    if num_winners == 1:
        return maisComum
    else:
        return selecionaMaioria(lista[:-1])

'''Realiza o proceso de andar na tabela 10 a 10 jogos, identifica os k vizinhos anteriores e prediz o resultado e as apostas'''
def geral(table,trainSet,k,bet):  #trainset = 50,60,70,80,90...
    df = pd.read_excel(table)
    beg = trainSet - 1
    end = beg + 10

    acertos = 0
    erros = 0
    entradas = 0
    lucro_rodada = 0
    oddH_soma = 0

    for j in range(20):
            for i in range(380):
                if i > beg and i <= end:                      # Anda pra frente na tabela;
                    if df.iloc[i,j] == 1:
                        oddH = df.iloc[i,21]
                        resultado_real = df.iloc[i,20]
                        tempResults = []
                        count = 0
                        '''Anda para trás na tabela, buscando so k vizinhos mais próximos'''
                        for n in range(i-1,-1,-1):          # Anda para trás, procurando os "k vizinhos", na tabela;
                            if count >= k:
                                break
                            if df.iloc[n,j] == 1 and count <= k:
                                tempResults.append(df.iloc[n,20])
                                count = count + 1
                        mais_comum = selecionaMaioria(tempResults)  # Função que verifica qual o mais comum dos resultados dos vizinhos anteriores;
                        resultado_previsto = mais_comum
                        '''Verifica numero de Acertos e Erros'''
                        if resultado_previsto == resultado_real:
                            acertos = acertos + 1
                        else:
                            erros = erros +1
                        '''Contabiliza o somatorio das oddH em cada entrada'''
                        if resultado_previsto == "S":
                            oddH_soma = oddH_soma + oddH
                            entradas = entradas + 1
                        '''Realiza o cáculo dos ganhos e eprdas nas apostas na rodada'''
                        if (resultado_previsto == "S") and (resultado_previsto == resultado_real):
                            lucro_rodada = lucro_rodada + round(bet * (oddH - 1), 2)
                        elif (resultado_previsto == "S") and(resultado_previsto != resultado_real):
                            lucro_rodada = lucro_rodada - bet
                        elif (resultado_previsto == "F") and (resultado_previsto == resultado_real):
                            lose_odd = 1/(1-float(1/float(oddH)))
                            lucro_rodada = lucro_rodada + round(bet * (lose_odd - 1), 2)
                        elif (resultado_previsto == "F") and (resultado_previsto != resultado_real):
                            lucro_rodada = lucro_rodada - bet

    return [acertos,erros,entradas,round(oddH_soma,2),round(lucro_rodada,2)]


