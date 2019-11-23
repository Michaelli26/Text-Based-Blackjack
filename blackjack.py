"""This is a single deck game of Black Jack with human(s) vs one computer dealer.

The goal of Blackjack is to beat the dealer by having a higher hand value without busting by exceeding 21, or allowing
dealer to bust without busting yourself. The dealer starts with one card face up and one card face down. The dealer will
stand on anything 17 (including soft 17) or higher. This game does not include special bets such as double down,
insurance, surrendering, splitting, etc. only a single initial bet. The payouts are 3:2 for a blackjack and 1:1 for all
other wins.
"""
import random

num_players = 2  # this game uses a single deck of 52 cards so the num of players should not exceed 10
hands = list()
banks = [None]
hands_and_banks = {}


class Hand:
    """
    A class used to contain Card objects for every player and the dealer. The dealer is always going to be player 0

    Attributes
    ----------
    player : int
        representing the player number
    lst : list
        contains all the Card objects within the player's hand.

    Methods
    -------
    value()
        returns the the numerical value of all the cards a player has
    bust()
        returns a boolean indicating whether or not the hand has bust. Also reassigns the value of an Ace from 11 to
        1 if the hand containing an Ace has a value over 21
    blackjack()
        returns a boolean indicating whether the hand has a blackjack (two card pair of an Ace and card with a value of
        10)
    """

    def __init__(self, player, lst=None):
        """
        :param player: The player's number
        :type player: int
        :param lst: contains all the Card object the player has
        :type lst: list
        """
        if lst is None:
            lst = []
        self.lst = lst
        self.player = player

    def __add__(self, card):
        """
        :param card: a card from the deck
        :type card: Card
        :return: None
        """
        self.lst.append(card)

    def __str__(self):
        """
        :return: the rank and suit of all the Cards objects a player has
        :rtype: str
        """
        cards = [card.__str__() for card in self.lst]
        return f"\n{', '.join(cards)}"

    def value(self):
        """
        :return: the combined value of every card in the hand
        :rtype: int
        """
        return sum([card.value for card in self.lst])

    def bust(self):
        """
        Reassigns the value of an Ace from 11 to 1 if the hand has a value over 21

        :return: whether or not a hand has bust by having a value over 21
        :rtype: boolean
        """
        if self.value() > 21:
            for card in self.lst:
                if card.value == 11:
                    card.value = 1
                    return False
            else:
                return True
        else:
            return False

    def blackjack(self):
        """
        :return: whether the hand is a blackjack
        :rtype: boolean
        """
        return (
                len(self.lst) == 2  # only two card hand
                and self.value() == 21  # value is 21
                )


class Deck:
    """
    A class representing a standard deck of 52 cards

    Attributes
    ----------
    lst: a list of 52 Card objects

    Methods
    -------
    shuffle()
        randomizes the deck of cards
    deal()
        gives two cards to each dealer and sets one of the dealers cards to be hidden, face down
    hit()
        gives another card to a player if they want to hit
    """

    def __init__(self, lst=None):
        """ Instantiates all 52 Card objects

        :param lst: contains all 52 Card objects
        :type lst: list
        """
        if lst is None:
            lst = []
        self.lst = lst
        ranks = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
        for rank in ranks:
            for suit in ['Diamonds', 'Clubs', 'Hearts', 'Spades']:
                # set values for Ace
                if rank == 'Ace':
                    lst.append(Card(rank, suit, 11))
                # set values for Two through Ten
                elif ranks.index(rank) + 1 < 11:
                    lst.append(Card(rank, suit, ranks.index(rank) + 1))
                # set values for Jack, Queen and King
                else:
                    lst.append(Card(rank, suit, 10))

    def shuffle(self):
        """
        randomizes the deck of cards
        :return: None
        """
        random.shuffle(self.lst)

    def deal(self):
        """
        gives two cards to each dealer and sets one of the dealers cards to be hidden, face down
        :return: None
        """
        for hand in hands:
            hand.__add__(self.hit())
            hand.__add__(self.hit())
            if hand.player == 0:  # if player is the dealer
                hand.lst[0].show = False  # set the first card as face down

    def hit(self):
        """
        gives another card to a player if they want to hit
        :return: first card object in the deck
        """
        return self.lst.pop(0)

    def __len__(self):
        return len(self.lst)


class Card:
    """
    A class used to represent a single card

    Attributes
    ----------
    rank: Ace through King
    suit: representing a diamond, club, heart or spade
    show: a boolean defaulted as True indicating whether a card is face up or hidden as face down
    value: the actual value of a playing card as opposed to the rank
    """

    def __init__(self, rank, suit, value, show=True):
        """
        :param rank: Ace through King
        :type rank: str
        :param suit: representing a diamond, club, heart or spade
        :type suit: str
        :param value: the actual value of a playing card as opposed to the rank
        :type value: int
        :param show: indicates whether a card is face up or hidden as face down (default = True)
        :type show: boolean
        """
        self.rank = rank
        self.suit = suit
        self.show = show
        self.value = value

    def __str__(self):
        if self.show:
            return self.rank + ' of ' + self.suit
        else:
            return 'Face Down'


class Bank:
    """
    A class used to represent each players' (excluding dealer) chips

    Attributes
    ----------
    player: int
        the player number
    balance: int
        current amount of chips (default 100)
    Methods
    -------
    deposit(amount)
        adds amount to a player's current balance of chips
    withdraw(amount)
        subtracts amount from a player's current balance of chips as long as the amount does not exceed the balance
    """

    def __init__(self, player, balance=100):
        self.player = player
        self.balance = balance

    def deposit(self, amount):
        """
        adds amount to a player's current balance of chips

        :param amount: value of chips to add to the balance
        :type amount: int
        :return: None
        """
        self.balance += amount

    def withdraw(self, amount):
        """
        subtracts amount from a player's current balance of chips as long as the amount does not exceed the balance

        :param amount: value of chips to remove from the balance
        :type amount: int
        :return: whether the amount to withdraw was accepted
        :rtype: boolean
        """
        if self.balance < amount:
            print('Bet exceeds balance.')
            return False
        else:
            self.balance -= amount
            return True


def setup():
    """
    Creates tne Hand objects for each player including the dealer and each player's bank account representing their
    chips. The dealer does not have a bank account.

    :return: None
    """
    for player in range(num_players + 1):
        hands.append(Hand(player))
        # create each player's bank
        if player > 0:
            banks.append(Bank(player))
    hands_and_banks.update(dict(zip(hands, banks)))


def reset_round():
    """
    removes the cards in each player's hand from the previous round. If any player went bankrupt(<$1), they must deposit
    a minimum of $1

    :return: None
    """
    hands.clear()
    hands_and_banks.clear()
    for player in range(num_players + 1):
        hands.append(Hand(player))
        # check to see if any player's (dealer excluded) chips went below $1, if so they have to deposit more
        if player > 0 and banks[player].balance < 1:
            while True:
                try:
                    deposit_amount = int(
                                        input(f"Player {player} is out of chips, please enter an amount to deposit.\n")
                                        )
                    if deposit_amount < 1:
                        print(f"Player {player} must deposit at least $1")
                        continue
                    banks[player].deposit(deposit_amount)
                    break
                except ValueError:
                    print('Invalid, enter an integer of 1 or more.')
    hands_and_banks.update(dict(zip(hands, banks)))


def take_bets():
    """
    Asks every player to input a numerical value they would like to bet for the round and withdraws that amount of chips
    from their bank balance

    :return: bets of all the players
    :rtype: list
    """
    bets = [None]  # index 0  is considered the dealer which does not make any bets
    for hand, bank in hands_and_banks.items():
        if hand.player == 0:
            continue
        else:
            while True:
                try:
                    print(f"Player {hand.player}'s balance: {bank.balance}")
                    while True:
                        bet = int(
                                input(f'Player {hand.player}, enter the amount you would like to bet\n')
                                )
                        if bet == 0:
                            print('The minimum bet is $1')
                            continue
                        elif bank.withdraw(bet):
                            print(f'Bet of ${bet} accepted.')
                            bets.append(bet)
                            break
                except ValueError:
                    print('Invalid input, enter an integer of 1 or more.')
                else:
                    break
    return bets


def turns(deck):
    """
    Asks every player whether or not they want to hit or stay and determines whether or not they bust after a hit

    :param deck: a deck object consisting of 52 card objects
    :return: None
    """
    print(f"Dealer's hand: {hands[0]}")
    for hand in hands[1:]:
        print(f"Player {hand.player}: {hands[hand.player]}")
        while True:
            action = input('Enter hit or stay.\n')
            if action.lower() == 'hit':
                hand.__add__(deck.hit())
                print(f"Player {hand.player}: {hands[hand.player]}")
                if hand.bust():
                    print(f"Player {hand.player} busted!")
                    break
            elif action.lower() == 'stay':
                break
            else:
                print('Invalid input.')


def dealer(deck):
    """
    controls the actions of the dealer once it has reached their turn. The dealer must reach a hand value of 17 or
    higher and will stand once it reaches a sufficient value. The dealer will stand on a soft 17 (ace and 6 off the
    deal)

    :param deck: a deck object consisting of 52 card objects
    :return: None
    """
    hands[0].lst[0].show = True  # reveal face down card
    print(f"Dealer's hand {hands[0]}")
    # if all the players bust, the dealer does not need to play
    for hand in hands[1:]:
        if hand.bust() is False:
            break
        elif hand == hands[-1]:
            return
    while not hands[0].bust() and hands[0].value() < 17:
        hands[0].__add__(deck.hit())
        print(f"Dealer's hand {hands[0]}")


def payout(bets):
    """
    compares each player's hand to the hand of the dealer and either pays out the player 1:1 for a normal win, 3:2 for
    a blackjack or returns the player's initial bet in the case of a push. If both the player and the dealer bust, the
    player loses their bet.

    :param bets: each player's bet for the round taken by the take_bets() method
    :type bets: list of integers
    :return: None
    """
    dealers_hand = hands[0]
    dealers_value = dealers_hand.value()
    for hand, bank in hands_and_banks.items():
        if hand == dealers_hand:  # skip the dealer that does not have a bank
            continue
        else:
            print(f"Player {hand.player}'s balance before round: ${bank.balance + bets[hand.player]}.")
            if hand.bust():  # if the player busts
                print(f'Player {hand.player} bust! \nLost ${bets[hand.player]}')
            # if the dealer got a blackjack
            elif dealers_hand.blackjack():
                if hand.blackjack():  # a player can only tie if the player also got a blackjack
                    print(f'Tie, both the dealer and  player {hand.player} got blackjacks. Player {hand.player}\n'
                          f"get's their bet back.")
                    bank.deposit((bets[hand.player]))
                else:  # otherwise they lost
                    print(f"Dealer's blackjack beats a {hand.value()}. Lost ${bets[hand.player]} bet.")
            # in the case that only player got a blackjack
            elif hand.blackjack():
                print(f"Player {hand.player} got a blackjack!")
                bank.deposit(2.5 * bets[hand.player])
            # if the dealer busts, everyone who didn't bust wins
            elif dealers_hand.bust():
                print(f'The dealer has bust.\nPlayer {hand.player} has won with ${bets[hand.player]} bet.')
                bank.deposit(2 * bets[hand.player])
            # normal play, no one bust or got a blackjack
            else:
                if hand.value() > dealers_value:
                    print(f"Player {hand.player}'s {hand.value()} beats Dealer's {dealers_value}. "
                          f"Won {bets[hand.player]}")
                    bank.deposit(2 * bets[hand.player])
                elif hand.value() == dealers_value:
                    print(f'A push. Player {hand.player} has {hand.value()}, Dealer also has {dealers_value}.'
                          f' Player {hand.player} gets their ${bets[hand.player]} bet back')
                    bank.deposit(bets[hand.player])
                else:
                    print(f"Dealer's {dealers_value} beats Player {hand.player}'s {hand.value()}. "
                          f"Lost ${bets[hand.player]}")
        print(f"Player {hand.player}'s balance after round: ${bank.balance}.")


def main():
    setup()
    while True:
        bets = take_bets()
        deck = Deck()
        deck.shuffle()
        deck.deal()
        turns(deck)
        dealer(deck)
        payout(bets)
        reset_round()


if __name__ == '__main__':
    main()
