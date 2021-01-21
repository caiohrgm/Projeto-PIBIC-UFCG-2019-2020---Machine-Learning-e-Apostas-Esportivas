import baseFunctions as bf
import pandas as pd
import NaiveBayesClassifier

tables = ['Premier2012x2013.xlsx', 'Premier2013x2014.xlsx', 'Premier2014x2015.xlsx', 'Premier2015x2016.xlsx',
          'Premier2016x2017.xlsx', 'Premier2017x2018.xlsx', 'Premier2018x2019.xlsx']
i = 2012
for elm in tables:

    xlsx = elm

    dataSet = pd.read_excel(xlsx)

    roundsTrain = 50
    total_entradas = 0
    total_acertos = 0
    total_erros = 0
    oddH_total = 0

    ganhos = 0
    perdas = 0

    while roundsTrain <= 370:
        indice_acertos_round = []
        classifier = NaiveBayesClassifier.NaiveBayesClassifier()
        classifier.train(dataSet, roundsTrain)
        classified = classifier.classify(dataSet, roundsTrain)

        for elm in classified:
            if elm != []:
                for e in elm:
                    if e == True:
                        total_acertos = total_acertos + 1
                        total_entradas = total_entradas + 1
                    elif e == False:
                        total_erros = total_erros + 1
                        total_entradas = total_entradas + 1

                '''tripla = (acertos,erros,acertos+erros)
                qtd_entradas.append(tripla)'''

        '''if qtd_entradas != []:
            for elm in qtd_entradas:
                rights = rights + elm[0]
                total_entradas = total_entradas + elm[2]
            acuracia_10rounds = (float(rights)/float(total_entradas))*100'''

        # ---------------------------------Coletar odds-------------------------------------#
        classified = classifier.classify02(dataSet, roundsTrain)

        for elm in classified:
            if elm != []:
                oddH_total = oddH_total + elm[0]

        # --------------------------------Apostando-----------------------------------------#
        classified = classifier.classify03(dataSet, roundsTrain, 100)

        for elm in classified:
            if elm[0] == "G" or elm[0] == "N":
                ganhos = ganhos + elm[1]
            elif elm[0] == "P":
                perdas = perdas + elm[1]

        roundsTrain = roundsTrain + 10

    accuracy = round((float(total_acertos) / float(total_entradas)) * 100, 4)
    oddH_media = round((float(oddH_total) / float(total_entradas)), 2)
    profit = ganhos + perdas

    print("--------------------Estatísticas do Campeonato [%d]-[%d]--------------------" % (i,i+1))
    print("Acurácia: %.2f%%" % accuracy)
    print("OddH Média: %.2f" % oddH_media)
    print("Ganhos: R$%.2f " % ganhos)
    print("Perdas: R$%.2f " % perdas)
    print("Lucro final: R$%.2f" % profit)
    print()
    i = i + 1
