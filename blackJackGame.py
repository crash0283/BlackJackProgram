# Blackjack
# From 1-7 players play against dealer

import cards
import games

# BJ_Card class
class BJ_Card(cards.Card):
    """A Blackjack Card."""

    ACE_VALUE = 1

    @property
    def value(self):
        if self.is_face_up:
            v = BJ_Card.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v


# BJ_Deck class
class BJ_Deck(cards.Deck):
    """A Blackjack Deck"""

    def populate(self):
        for rank in BJ_Card.RANKS:
            for suit in BJ_Card.SUITS:
                self.cards.append(BJ_Card(rank, suit))


# BJ_Hand class
class BJ_Hand(cards.Hand):
    """A Blackjack Hand"""

    def __init__(self, name):
        super(BJ_Hand, self).__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super(BJ_Hand, self).__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep

    @property
    def total(self):
        # if a card in the hand has a value of None, than total is None
        for card in self.cards:
            if not card.value:
                return None

        # add up card values, treat each ace as 1
        t = 0
        for card in self.cards:
            t += card.value

        # determine if hand contains an ace
        contains_ace = False
        for card in self.cards:
            if card.value == BJ_Card.ACE_VALUE:
                contains_ace = True

        # if contains ace and total is low enough, treat ace as 11
        if contains_ace and t == 11:
            # add only 10 since we already added 1 to ace
            t += 10
        return t

    def is_busted(self):
        return self.total > 21


# BJ_Player class
class BJ_Player(BJ_Hand):
    """A Blackjack Player"""

    def is_hitting(self):
        response = games.ask_yes_no("\n" + self.name + ",do you want to hit?(y/n):")
        return response == "y"

    def bust(self):
        print self.name, "busts."
        self.lose()

    def lose(self):
        print self.name, "loses."

    def win(self):
        print self.name, "wins."

    def push(self):
        print self.name, "pushes."


# BJ_Dealer class
class BJ_Dealer(BJ_Hand):
    """A Blackjack Dealer"""

    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print self.name, "busts."

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()


# BJ_Game class
class BJ_Game(object):
    """A Blackjack Game"""

    def __init__(self, names):
        self.players = []
        for name in names:
            player = BJ_Player(name)
            self.players.append(player)
        self.dealer = BJ_Dealer("Dealer")
        self.deck = BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
            return sp

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print player
            if player.is_busted():
                player.bust()

    def play(self):
        # deal initial 2 cards to everyone
        self.deck.deal(self.players + [self.dealer], per_hand=2)
        self.dealer.flip_first_card()  # hide dealers first card
        for player in self.players:
            print player
        print self.dealer

        # deal additional cards to players
        for player in self.players:
            self.__additional_cards(player)

        self.dealer.flip_first_card()  # reveal dealers first

        if not self.still_playing:
            # since all players busted, show dealers hand
            print self.dealer

        else:
            # deal additional cards to dealer
            print self.dealer
            self.__additional_cards(self.dealer)

        if self.dealer.is_busted():
            # everyone still playing wins
            for player in self.still_playing:
                player.win()

        else:
            # compare each player still playing to dealer
            for player in self.still_playing:
                if player.total > self.dealer.total:
                    player.win()
                elif player.total < self.dealer.total:
                    player.lose()

                else:
                    player.push()

            # remove everyones cards
        for player in self.players:
            player.clear()
        self.dealer.clear()


def main():
    print "\t\tWelcome To Blackjack!\n"

    names = []

    number = games.ask_number("How many players?(1-7):", low=1, high=8)

    for i in range(number):
        name = raw_input("Enter your name:")
        names.append(name)
    print()
    game = BJ_Game(names)
    again = None
    while again != "n":
        game.play()
        again = games.ask_yes_no("\nDo you want to play again?:")


main()
raw_input("\nPress enter key to exit.")
