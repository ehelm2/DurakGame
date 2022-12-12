# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 09:32:21 2022

@author: emily
"""
from random import shuffle

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
    
    # def __init__(self):
        
        
    def set_players(self):
        num_to_play = int(input('How many players? '))
        if num_to_play > 4:
            return print('Sorry, only a max of 4 people can play!')
        if num_to_play < 2:
            return print('Sorry, you need a minimum of 2 people to play!')
        
        self.players = []
        
        for p in range(1, num_to_play + 1):
            name = input('Enter Player %i Name: ' %p)
            self.players.append(Player(name))
            
            for c in range(0,6):
                self.players[p-1].hand.append(self.deck.pick_card())
                
        return self.players
        
    def wins(self, winner):
        w = '{} wins this round!'.format(winner)
        winner.wins += 1
        print(w)
        
    def single_deal(self, player, num):
        for c in range(0,num):
            player.hand.append(self.deck.pick_card())
            
            if len(self.deck.new_deck) == 0:
                break
            
    def play(self):
        self.deck = Deck()
        trump_card = self.deck.set_trump()
        
        players = self.set_players()

        print('Begin attack!')
        
        while len(self.deck.new_deck) > -1:
            for turn in range(1,100):
                if turn % 2 == 0:
                    attacker = players[0]
                    defender = players[1]
                else:
                    attacker = players[1]
                    defender = players[0]
            
                self.single_deal(attacker, 3)
            
            # if len(self.deck.new_deck) == 0:
            #     print('end of deck')
            #     break
        
        

                
        
start = DurakGame()
start.play()

        
''' 
newDeck = Deck()
hand = []
for i in range(0,6):
    hand.append(newDeck.pick_card())
    
trump = newDeck.set_trump()

print(trump)
print(hand)
print(hand[0], hand[4])
wins = newDeck.compare(hand[0], hand[4], trump)
print('The winner is {}!'.format(wins))
'''
