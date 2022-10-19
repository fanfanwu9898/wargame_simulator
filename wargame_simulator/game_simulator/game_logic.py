from collections import deque
import random

# define the card as an class
class Card:
    def __init__(self, id_num, name, pattern, rank):
        self._id_num = id_num
        self.name = name
        self.pattern = pattern
        self.rank = rank
    
    def __repr__(self):
        return self.pattern + '_' + self.name
    
    def __lt__(self, other):
        return self.rank < other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __eq__(self, other):
        return self.rank == other.rank

class OutOfCardError(Exception): pass

class WarGame:
    def __init__(self, player_name_1, player_name_2, card_names, 
                card_patterns, card_ranks = None, random_seed = None):
        self.player_1, self.player_2  = player_name_1, player_name_2
        self.card_names = card_names
        self.card_patterns = card_patterns
        self.card_ranks = card_ranks
        self._rounds = -1
        self._number_of_war_rounds = 0
        self._game_history = dict()

        if random_seed != None:
            random.seed(random_seed)

    @staticmethod    
    def generate_card_deck(names, patterns, ranks = None):
        deck = []

        if ranks == None:
            ranks = [i for i in range(len(names))]

        id_num = 0
        for rank, name in zip(ranks, names):
            for pattern in patterns:
                deck.append(Card(id_num, name, pattern, rank))
                id_num += 1
        return deck

    @staticmethod
    def distribute_card(deck):
        random.shuffle(deck)
        return deque(deck[:len(deck)//2 + 1]), deque(deck[len(deck)//2 + 1:])

    def _one_round(self, cards_for_winner):
        self._rounds += 1
        self._game_history[self._rounds] = {
            "round_num": self._rounds,
            self.player_1:'->'.join([str(card) for card in list(self.player_1_deck)]),
            self.player_2:'->'.join([str(card) for card in list(self.player_2_deck)]),
            "war_round":False
        }

        card_player_1 = self.player_1_deck.popleft()
        card_player_2 = self.player_2_deck.popleft()
        cards_for_winner.extend([card_player_1, card_player_2])

        #shuffle the card in order to avoid never-ending game
        random.shuffle(cards_for_winner)

        if card_player_1 > card_player_2:
            self.player_1_deck.extend(cards_for_winner)
            
        elif card_player_1 < card_player_2:
            self.player_2_deck.extend(cards_for_winner)

        else:
            self._game_history[self._rounds]["war_round"] = True
            self._number_of_war_rounds += 1

            if len(self.player_1_deck) <= 1 or \
                len(self.player_2_deck) <= 1:
                raise OutOfCardError()

            cards_for_winner.extend([self.player_1_deck.popleft(), 
                            self.player_2_deck.popleft()])

            #use recursion for cases that two cards have the same rank
            self._one_round(cards_for_winner)

    def run_game_simulation(self):
        card_deck = WarGame.generate_card_deck(self.card_names, 
                        self.card_patterns, ranks = self.card_ranks)

        self.player_1_deck, self.player_2_deck = WarGame.distribute_card(card_deck)
        

        while len(self.player_1_deck) != 0 and \
                len(self.player_2_deck) != 0 :
            self._one_round([])

        
        winner = self.player_2 if len(self.player_1_deck) == 0 else self.player_1

        return winner, self._rounds, self._number_of_war_rounds, self._game_history



if __name__ == "__main__":
    card_names = [str(i) for i in range(2, 11)] + ['J', 'Q', 'k', 'A']
    card_patterns = ['black-spades', 'black-clubs', 'red-hearts', 'red-diamonds']

    player_name_1, player_name_2 = 'Alex', 'Iris'
    game = WarGame(player_name_1, player_name_2, card_names, card_patterns)
    winner, rounds, number_of_war_rounds, game_history = game.run_game_simulation()

    print("Winner", winner)
    print("Rounds", rounds)
    print("Number_of_war_rounds", number_of_war_rounds)
    print("Game History", game_history)