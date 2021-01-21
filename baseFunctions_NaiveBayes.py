import pandas as pd
import xlrd

def createDataFrame():
    colunas = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11',
               'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20']
    df = pd.DataFrame(columns=colunas)
    return df

def treinaIndiceMandante(rodadas,dataSet):
    list = []
    rounds = rodadas
    tempDf = dataSet

    for j in range(20):
        boss = 0
        out = 0
        wins = 0
        for i in range(rounds):
            if tempDf.iloc[i, j] == 1:
                boss = boss + 1
                if tempDf.iloc[i, 20] == "S":
                    wins = wins + 1
            elif tempDf.iloc[i, j] == -1:
                out = out + 1

        losses = boss + out - wins
        teamstat = [boss, out, wins, losses]
        list.append(teamstat)

    return list

def boss_victory_prob(list1): #Probabilidade de ganhar como mandante;
    boss_victory_frequency = []
    for elm in list1:
        prob = round((float(elm[2]) / float(elm[0])), 4)
        boss_victory_frequency.append(prob)
    return boss_victory_frequency

def boss_defeat_prob(list1): #Probabilidade de perder como mandante;
    boss_defeat_frequency = []
    for elm in list1:
        prob = round((float(elm[0] - elm[2]) / float(elm[1])),
                     4)  # Atenção: pode dar zero. Talvez usar um suavizador de numero baixo.
        '''if prob == 0:
            prob = 0.001'''  # ajuste,se necessário;
        boss_defeat_frequency.append(prob)
    return boss_defeat_frequency

def boss_win_probability(vitorias, derrotas): #Probabilidade total de um time ganhar, caso seja mandante;
    win_probabilities = []

    '''Calculo da probabilidade, usando o teorema:
    P(S / V) = P(V/S) x 0.33 / P(V/S) x 0.33 + P(V/~S) x 0.67
    P(V/S):prob de ser mandante e ganhar;
    P(V/~S: prob de ser mandante e não ganhar;'''

    for elm1, elm2 in zip(vitorias, derrotas):
        prob_boss_winner = float(elm1 * 0.33) / float(elm1 * 0.33 + elm2 * 0.67)
        win_probabilities.append(prob_boss_winner)
    return win_probabilities

def winner_boss_probability_10rounds(listBoss,testData,round):
    df = testData
    beg = round
    end = beg + 10

    results = []

    for j in range(20):
        foreseen = ""
        list = []
        for i in range(380):
            if i > beg and i <= end:                
                if df.iloc[i,j]  == 1:
                    real = df.iloc[i,20]
                    if listBoss[j] > 0.65:
                        foreseen = "S"              # Atribui a "previsao" sucesso (aposta na vitoria);
                        if foreseen == real:        # Checa se a previsao é igual à realidade;
                            list.append(True)
                        else:
                            list.append(False)
        results.append(list)
    return results

def odd_rates(listBoss,testData,round):
    df = testData
    beg = round
    end = beg + 10

    results = []

    for j in range(20):
        foreseen = ""
        list = []
        for i in range(380):
            if i > beg and i <= end:                # Está lendo 9 a acada 9 jogos;
                if df.iloc[i,j]  == 1:
                    real = df.iloc[i,20]
                    if listBoss[j] > 0.65:
                        foreseen = "S"
                        odd = df.iloc[i,21]
                        list.append(odd)
                        if foreseen == real:
                            list.append("Vitoria")
                        else:
                            list.append("Derrota")
        results.append(list)
    return results

def bets(listBoss,testData,rodada,bet):
    df = testData
    beg = rodada
    end = beg + 10

    results = []

    for j in range(20):
        foreseen = ""
        for i in range(380):
            if i > beg and i <= end:                # Lendo de 10 em 10
                if df.iloc[i,j]  == 1:
                    real = df.iloc[i,20]
                    if listBoss[j] > 0.5:
                        foreseen = "S"
                        odd = df.iloc[i,21]

                        if foreseen == real:
                            profit = round(bet*(odd-1),2)
                            tupla = ("G",profit)
                            results.append((tupla))
                        else:
                            tupla = ("P",-bet)
                            results.append((tupla))
                    else:
                        odd = 1/(1-float(1/float(df.iloc[i,21])))
                        foreseen = "F"
                        if foreseen == real:
                            profit = round(bet * (odd - 1), 2)
                            tupla = ("G",profit)
                            results.append((tupla))
                        else:
                            tupla = ("P",-bet)
                            results.append(tupla)
    return results






