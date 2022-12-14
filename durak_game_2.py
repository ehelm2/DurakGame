# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 09:32:21 2022

@author: emily
"""
from random import shuffle
from time import sleep

class Card:
    def __init__(self, rank, suit, value):
        self.rank = rank
        self.suit = suit
        self.value = value
        
    def __lt__(self, card2):
        if self.value < card2.value:
            return True
        elif self.value == card2.value:
            print('Play again')
        return False
    
    def __gt__(self, card2):
        if self.value > card2.value:
            return True
        elif self.value == card2.value:
            print('Play again')
        return False
        
    def __repr__(self):
        card = '{} of {}'.format(self.rank, self.suit)
        return card
        
class Deck:
    def __init__(self):
        self.new_deck = []
        rank = ['Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
        suit = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        value = [6, 7, 8, 9, 10, 11, 12, 13, 14]
        
        for i in range(len(rank)):
            for j in range(len(suit)):
                self.new_deck.append(Card(rank[i], suit[j], value[i]))
                
        shuffle(self.new_deck)
    
    def pick_card(self):
        if len(self.new_deck) == 0:
            return
        return self.new_deck.pop()
    
    def set_trump(self):
        trump = self.pick_card()
        return trump
    
    def compare(self, card1, card2, trump):

        if card1.suit == trump.suit and card2.suit != trump.suit:
            winner = card1
            return winner
        
        if card1.suit != trump.suit and card2.suit == trump.suit:
            winner = card2
            return winner

        elif card1 > card2:
            winner = card1
            return winner

        elif card1 < card2:
            winner = card2
            return winner

class Player:
    def __init__(self, name = None):
        self.name = name
        self.wins = 0
        self.hand = []
        self.card = None
        
class DurakGame:
    
    def __init__(self):
        self.p1 = input('Enter Player 1\'s Name: ')
        self.p2 = input('Enter Player 2\'s Name: ')

    def setup(self):
        self.deck = Deck()
        self.players = []
        
        self.players.append(Player(self.p1))
        self.players.append(Player(self.p2))

        trump_card = self.deck.set_trump()
        print('The trump card is {}, so the trump suit is {}.\n'.format(trump_card, trump_card.suit))

        dealt_trumps = []
        for p in range(len(self.players)):
            for c in range(0,6):
                card = self.deck.pick_card()
                self.players[p-1].hand.append(card)
                if card.suit == trump_card.suit:
                    dealt_trumps.append(card)

        print('The player with the lowest trump card goes first...')

        dealt_trumps.sort(key=lambda x: x.value)

        if dealt_trumps[0] in self.players[0].hand:
            print('{} has {} and is the first attacker!'.format(self.players[0].name, dealt_trumps[0]))
        
        elif dealt_trumps[0] in self.players[1].hand:
            print('{} has {} and is the first attacker!'.format(self.players[1].name, dealt_trumps[0]))
            self.players.reverse()
        elif len(dealt_trumps) == 0:
            print('Oops, no one has a trump card! Shuffle and try again.')

        return self.players, trump_card
        
    def wins(self, winner):
        w = '{} wins this round!'.format(winner.name)
        winner.wins += 1
        print(w)
        
    def deal(self, player, num = 1):
        for c in range(0, num):
            if len(self.deck.new_deck) == 0:
                break
            player.hand.append(self.deck.pick_card())

    def play_a_card(self, player, card):
        ## I need to refine this so that I can make sure I can account for misspellings
        for c in player.hand:
            if str(c) == card:
                active_card = player.hand.remove(c)
                return active_card

    def play(self, beginner = False):        
        
        game_on = True

        while game_on:

            players, trump_card = self.setup()

            # Round level
            while len(players[0].hand) > 0 and len(players[1].hand) > 0:
                out_of_cards = False

                if not out_of_cards:
                    for p in players:
                        self.deal(p, (6-len(p.hand)))
                if len(self.deck.new_deck) <= 0:
                    out_of_cards = True
                    print('Out of cards in the deck!')
                
                # turn level
                for turn in range(1, 100):
                    
                    attacker = players[0]
                    defender = players[1]

                    # To store all cards up for grabs
                    battle_cards = []

                    print('The attacker is {}. {}, look away!'.format(attacker.name, defender.name))
                    print('Cards in {}\'s hand: {}'.format(attacker.name, attacker.hand))
            
                    attack_card = str(input('Which card would you like to play? '))
                    self.play_a_card(attacker, attack_card)

                    battle_cards.append(attack_card)

                    print('The defender is {}. {}, look away!\n'.format(defender.name, attacker.name))
                    print('Cards in {}\'s hand: {}\n'.format(defender.name, defender.hand))
                    print('The defender may accept the attack, ending the round,')
                    print('or they may defend with a better card.\n')
                    
                    move = input('What would you like to do? Take or Play? ')
                    
                    valid_cards = []
                    for c in defender.hand:
                        if c > battle_cards[-1]:
                            valid_cards.append(c)
                    
                    if len(valid_cards) == 0:
                        print('No valid card to play. Must take the attack.')
                        defender.hand.append(battle_cards.pop())
                        continue

                    elif move.lower() == 'take':
                        defender.hand.append(battle_cards.pop())
                        print('Attack succeeded! The card has been added to {}\'s hand'.format(defender.name))
                        continue

                    elif move.lower() == 'play':
                        print('You can play any of these cards from your hand: {}'.format(valid_cards))

                        defender_card = str(input('Which card will you play? '))
                        #need to insert here an error/retry if not from valid_cards

                        self.play_a_card(defender, defender_card)
                        battle_cards.append(defender_card)

                        print('{} has defended with {}'.format(defender.name, defender_card))
                    
                        #attacker must pass or can attack again

                        #compare to see which card wins

                    if len(players[0].hand) == 0:
                        self.wins(players[0])
                        break
                    if len(players[1].hand) == 0:
                        self.wins(players[1])
                        break
            
            if players[0].wins == 5:
                print('{} wins the game!'.format(players[0].name))
                game_on = False
            if players[1].wins == 5:
                print('{} wins the game!'.format(players[1].name))
                game_on = False
start = DurakGame()
start.play()

