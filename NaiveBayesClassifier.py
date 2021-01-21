import baseFunctions as bf


class NaiveBayesClassifier:

    def __init__(self):
        self.boss_win_prob = []
        self.out_win_prob = []

    def train(self, training_set, rounds):
        lista_boss = bf.treinaIndiceMandante(rounds, training_set)

        victory_list = bf.boss_victory_prob(lista_boss)
        defeat_list = bf.boss_defeat_prob(lista_boss)

        self.boss_win_prob = bf.boss_win_probability(victory_list,defeat_list)  # Probabilidade de ganhar jogos em casa.

    def classify(self, test_data,round):
        return bf.winner_boss_probability_10rounds(self.boss_win_prob, test_data, round)

    def classify02(self, test_data,round):
        return bf.odd_rates(self.boss_win_prob, test_data, round)

    def classify03(self, test_data,round,bet):
        return bf.bets(self.boss_win_prob, test_data, round,bet)


