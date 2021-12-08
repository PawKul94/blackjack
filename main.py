import time
import random
import os

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)
                self.deck.append(created_card)

    def __str__(self):
        whole = ''
        for card in self.deck:
            whole += card.__str__() + '\n'
        return whole

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100

    def give(self, give):
        self.total -= give
        return give

    def gain(self, gain):
        self.total += gain


class Pot:

    def __init__(self):
        self.pot = 0

    def __str__(self):
        return f'Currently there\'s ${self.pot} in the pot.'

    def increase(self, amount):
        self.pot += amount

    def cash_out(self):
        return self.pot


def clear_screen():
    os.system('cls')


def hitting(hand):
    hand.add_card(deck.deal())
    if player:
        print(f'{name} draws {hand.cards[-1]}.')
    elif dealer:
        print(f'Dealer draws {hand.cards[-1]}.')
    hand.adjust_for_ace()


def betting():
    print(f'You currently have {player_chips.total} chips.')
    while True:
        try:
            bet = int(input('Place your bet:\n> '))
            if bet <= 0:
                print('You can\'t bet 0 or less!')
                continue
        except ValueError:
            print('That\'s not a valid bet.')
        else:
            break

    if bet > player_chips.total:
        print('You can\'t bet more than you have!')
    else:
        pot.increase((player_chips.give(bet)) * 2)
        print(f'You bet {bet} chips. Currently there are {pot.pot} chips in the pot.')
        print(f'You currently have {player_chips.total} chips.')
        return bet


def show_hand(hand):
    if player:
        print(f'Cards on {name}\'s hand:', *hand.cards, sep='\n')
    elif dealer:
        print(f'Cards on Dealer\'s hand:', *hand.cards, sep='\n')
    print(f'Its value equals {hand.value}.')


game = True
player_chips = Chips()
name = input('What\'s your name?\n> ')
print(f'''Welcome to My Casino, {name}! You can play Blackjack here. You begin with 100 chips. 
Blackjack is paid at 3:2.
If you run out of chips, you won't be able to play anymore. Have fun!\n''')
while game:
    pot = Pot()
    deck = Deck()
    deck.shuffle()
    player = True
    dealer = False

    if player_chips.total <= 0:
        print('Oops, you ran out of chips. Come back when you have them!')
        break

    initial_bet = betting()
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    player_hand.adjust_for_ace()
    show_hand(player_hand)
    if player_hand.value == 21:
        print(f'Blackjack! {name} wins!')
        player_chips.gain((pot.cash_out()) * 1.5)
        again = input('If you want to play another hand just say \'yes\'.\n> ')
        if again[0].lower() == 'y':
            continue
        else:
            game = False
            print(f'Thanks for playing, {name}. Come again soon!')
            break
    print('\n')
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    print(f'Dealer has one hole card and {dealer_hand.cards[1]}.')

    while player:
        choice = input('\nWhat do you want to do:\n1. Hit\n2. Double Down\n3. Stand\n> ')
        if choice.lower() in ['hit', '1']:
            hitting(player_hand)
            if player_hand.value > 21:
                print('Player busts!')
                player = False
            else:
                show_hand(player_hand)

        elif choice.lower() in ['double', '2']:
            if player_chips.total < initial_bet:
                print('You must have enough chips to double down.')
            else:
                pot.increase((player_chips.give(initial_bet)) * 2)
                hitting(player_hand)
                if player_hand.value > 21:
                    print(f'{name} busts!')
                    player = False
                else:
                    show_hand(player_hand)
                    print('Double down. Dealer plays.')
                    player = False
                    dealer = True

        elif choice.lower() in ['stand', '3']:
            print(f'{name} stands. Dealer plays.\n')
            player = False
            dealer = True
        else:
            print('I don\'t understand. Please try again.')

    while dealer:
        show_hand(dealer_hand)
        while dealer_hand.value < 17:
            hitting(dealer_hand)
            show_hand(dealer_hand)
            print(f'Its value is {dealer_hand.value}.\n')
        dealer = False

        if dealer_hand.value > 21:
            print('Dealer busts!')
            print(f'You win {pot.pot} chips.')
            player_chips.gain(pot.cash_out())
            break

        elif dealer_hand.value > player_hand.value:
            print('Dealer wins!')

        elif dealer_hand.value < player_hand.value:
            print(f'{name} wins!')
            print(f'{name} wins {pot.pot} chips.')
            player_chips.gain(pot.cash_out())
        else:
            print('Push!')

    again = input('Do you want to play another one?\n> ')
    if again[0].lower() == 'y':
        clear_screen()
        continue
    else:
        game = False
        print('Thanks for playing. Come again soon!')

time.sleep(5)
