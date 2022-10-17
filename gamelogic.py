# define deck of the card as an class
class Card:
    def __init__(self, id_num, name, pattern, rank):
        self._id_num = id_num
        self.name = name
        self.pattern = pattern
        self.rank = rank
    
    def __repr__(self):
        return self.pattern + ' ' + self.name
    
    def __lt__(self, other):
        return self.rank < other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __eq__(self, other):
        return self.rank == other.rank




# for card in enumerate(deck):
#     print(card)


# assert(deck[0] == deck[1])
# assert(deck[1] == deck[2])
# assert(deck[2] == deck[3])

# assert(deck[4] > deck[1])
# assert(deck[50] > deck[32])

from collections import deque
import random


class OutOfCardError(Exception): pass

class WarGame:
    def __init__(self, player_name_1, player_name_2, card_names, 
                card_patterns, card_ranks = None, random_seed = None):
        self.player_1, self.player_2  = player_name_1, player_name_2
        self.card_names = card_names
        self.card_patterns = card_patterns
        self.card_ranks = card_ranks
        
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
        card_player_1 = self.player_1_deck.popleft()
        card_player_2 = self.player_2_deck.popleft()
        cards_for_winner.extend([card_player_1, card_player_2])

        if card_player_1 > card_player_2:
            self.player_1_deck.extend(cards_for_winner)
        elif card_player_1 < card_player_2:
            self.player_2_deck.extend(cards_for_winner)
        else:
            if len(self.player_1_deck) <= 1 or \
                len(self.player_2_deck) <= 1:
                raise OutOfCardError()
            cards_for_winner.extend([self.player_1_deck.popleft(), 
                            self.player_2_deck.popleft()])
            self._one_round(cards_for_winner)

    def run_game_simulation(self):
        card_deck = WarGame.generate_card_deck(self.card_names, 
                        self.card_patterns, ranks = self.card_ranks)
        self.player_1_deck, self.player_2_deck = WarGame.distribute_card(card_deck)
        
        while len(self.player_1_deck) != 0 and \
                len(self.player_2_deck) != 0 :
            self._one_round([])
            print(self.player_1_deck)
            print(self.player_2_deck)
            print(len(self.player_1_deck), len(self.player_2_deck))
            print("---------------------------------")
        
        if len(self.player_1_deck) == 0:
            return self.player_2
        else:
            return self.player_1

# generate deck of 52 card
card_names = [str(i) for i in range(2, 11)] + ['J', 'Q', 'k', 'A']
card_patterns = ['black spades', 'black clubs', 'red hearts', 'red diamonds']

player_name_1, player_name_2 = 'Alex', 'Iris'
game = WarGame(player_name_1, player_name_2, card_names, card_patterns)
winner = game.run_game_simulation()

print(winner)