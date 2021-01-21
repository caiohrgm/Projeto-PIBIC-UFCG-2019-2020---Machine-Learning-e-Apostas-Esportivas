import BasicFunctions as bf

lista_tabelas = ['Premier2012x2013.xlsx', 'Premier2013x2014.xlsx', 'Premier2014x2015.xlsx', 'Premier2015x2016.xlsx',
          'Premier2016x2017.xlsx', 'Premier2017x2018.xlsx', 'Premier2018x2019.xlsx']
ano = 2012
bet = 100
k = 3
for elm in lista_tabelas:
    acertos_total = 0
    erros_total = 0
    entradas_total = 0
    oddH_soma_total = 0
    lucro_rodada_total = 0

    for i in range(50,371,10):
        lista_temp = bf.geral(elm,i,k,bet)          # Classificador Geral

        acertos_total = acertos_total+ lista_temp[0]
        erros_total = erros_total + lista_temp[1]
        entradas_total = entradas_total + lista_temp[2]
        oddH_soma_total = oddH_soma_total + lista_temp[3]
        lucro_rodada_total = lucro_rodada_total + lista_temp[4]

    acuracia = (acertos_total/float(acertos_total + erros_total))*100
    oddh_media = oddH_soma_total/float(entradas_total)
    lucro_final =lucro_rodada_total

    print("--------------------Estatísticas do Campeonato [%d]-[%d]--------------------" % (ano, ano + 1))
    print("Acurácia: %.2f%%" % acuracia)
    print("oddH Média: %.2f" % oddh_media)
    print("Lucro final: R$%2.f" % lucro_final)
    ano = ano + 1