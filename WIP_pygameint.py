# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 13:53:32 2022

@author: emily
"""
import pygame
from card_dictionary import card_files
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
        return False
    
    def __gt__(self, card2):
        if self.value > card2.value:
            return True
        return False
        
    def __repr__(self):
        card = '{} of {}'.format(self.rank, self.suit)
        return card
        
class Deck:
    
    def __init__(self):
        self.new_deck = []
        self.rank = ['Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
        self.suit = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        self.value = [6, 7, 8, 9, 10, 11, 12, 13, 14]
        
        for i in range(len(self.rank)):
            for j in range(len(self.suit)):
                self.new_deck.append(Card(self.rank[i], self.suit[j], self.value[i]))
                
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

# class InputBox:

#     def __init__(self, x, y, w, h, text=''):
#         self.rect = pg.Rect(x, y, w, h)
#         self.color = COLOR_INACTIVE
#         self.text = text
#         self.txt_surface = FONT.render(text, True, self.color)
#         self.active = False

#     def handle_event(self, event):
#         if event.type == pg.MOUSEBUTTONDOWN:
#             # If the user clicked on the input_box rect.
#             if self.rect.collidepoint(event.pos):
#                 # Toggle the active variable.
#                 self.active = not self.active
#             else:
#                 self.active = False
#             # Change the current color of the input box.
#             self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
#         if event.type == pg.KEYDOWN:
#             if self.active:
#                 if event.key == pg.K_RETURN:
#                     print(self.text)
#                     self.text = ''
#                 elif event.key == pg.K_BACKSPACE:
#                     self.text = self.text[:-1]
#                 else:
#                     self.text += event.unicode
#                 # Re-render the text.
#                 self.txt_surface = FONT.render(self.text, True, self.color)

#     def update(self):
#         # Resize the box if the text is too long.
#         width = max(200, self.txt_surface.get_width()+10)
#         self.rect.w = width

#     def draw(self, screen):
#         # Blit the text.
#         screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
#         # Blit the rect.
#         pg.draw.rect(screen, self.color, self.rect, 2)

class Interface:
    pass
    
class cmdLine(Interface):
    def __init__(self):
        pass

    def getnames(self):
        self.p1 = input('Enter Player 1\'s Name: ')
        self.p2 = input('Enter Player 2\'s Name: ')
        
        return self.p1, self.p2
    
    def getcard(self, deck_obj):
        selected_card = str(input('Which card would you like to play? '))
        
        check_string = selected_card.split(' ')
        
        while not len(check_string) == 3:
            print('Please type as seen on screen. Try again!')
            selected_card = str(input('Which card would you like to play? '))
            check_string = selected_card.split(' ')            

        while not check_string[0] in deck_obj.rank and not check_string[2] in deck_obj.suit:
            print('Please check spelling and capitalization. Try again!')
            selected_card = str(input('Which card would you like to play? '))
            check_string = selected_card.split(' ')

        return selected_card
    
    def getmove(self):
        
        selected_move = input('What would you like to do? Pass or Play? ')
        
        available_moves = ['pass', 'play']
        
        while not selected_move.lower() in available_moves:
            print('Oops try typing \'pass\' or \'play\'')
            selected_move = input('What would you like to do? Pass or Play? ')
        
        return selected_move.lower()
    
    def getvalid(self, trump_suit, list_of_cards, hand, position):
        
        valid_cards = []
        
        if position == 'attacker':
            for c1 in list_of_cards[-2:]:
                for c2 in hand:
                    if c1.rank == c2.rank:
                        valid_cards.append(c2)               
        
        if position == 'defender':
            for c in hand:
                if c.suit == trump_suit:
                    if c > list_of_cards[-1]:
                        valid_cards.append(c)
                if c.suit == list_of_cards[-1].suit and c > list_of_cards[-1]:
                    valid_cards.append(c)
        
        return valid_cards
      
class pyGame(Interface):
    
    def __init__(self):
        pass
    def render_interface(self, window):
        window.fill((25, 130, 56))

        cardBack = pygame.image.load('icons/design1.png')
        window.blit(cardBack, (300, 100))
        
        font = pygame.font.SysFont('rockwell', 20, True)
        text = font.render('players hand:', True, (255, 255, 255))
        window.blit(text,(100, 500))
        pygame.display.update()

    def getnames(self):
        p1 = input('Enter Player 1\'s Name: ')
        p2 = input('Enter Player 2\'s Name: ')
        
        return p1, p2

    def getcard(self):
        pass
    def getmove(self):
        pass
    def getvalid(self):
        pass
   
class DurakGame:

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
        
        if len(dealt_trumps) == 0:
            print('Oops, no one has a trump card! Player with lowest card value goes first.')
            p1_lowest = self.players[0].hand.sort(key = lambda x: x.value)
            p2_lowest = self.players[1].hand.sort(key = lambda x: x.value)
            
            if p1_lowest[0] > p2_lowest[0]:
                print('{} has {} and is the first attacker!'.format(self.players[1].name, p2_lowest[0]))
                self.players.reverse()
        elif dealt_trumps[0] in self.players[0].hand:
            print('{} has {} and is the first attacker!'.format(self.players[0].name, dealt_trumps[0]))
        
        elif dealt_trumps[0] in self.players[1].hand:
            print('{} has {} and is the first attacker!'.format(self.players[1].name, dealt_trumps[0]))
            self.players.reverse()

        return self.players, trump_card
        
    def wins(self, winner):
        w = '{} wins this round!'.format(winner.name)
        winner.wins += 1
        print(w)
        
    def deal(self, player, num = 1):
        if num <= 0:
            return
        for c in range(0, num):
            if len(self.deck.new_deck) == 0:
                break
            player.hand.append(self.deck.pick_card())

    def play_a_card(self, player, card):
        for c in player.hand:
            if str(c) == card:
                player.hand.remove(c)
                return c

    def play(self, interface, key = None):
        
        game_on = True
        
        # if key == None:
        #     return

        self.p1, self.p2 = interface.getnames()

        while game_on:

            players, trump_card = self.setup()

            # Round level
            while len(players[0].hand) > 0 and len(players[1].hand) > 0:
                
                # turn level
                for turn in range(1, 100):
                    
                    out_of_cards = False
                                
                    if not out_of_cards:
                        for p in players:
                            self.deal(p, (6-len(p.hand)))
                            if len(self.deck.new_deck) <= 0:
                                out_of_cards = True
                                print('Out of cards in the deck!')

                    for p in players:
                        p.hand.sort(key=lambda x: x.value)

                    end_turn = False
                    
                    print('~~~~~~~~~')
                    print('TURN %i' % turn)
                    print('~~~~~~~~~')
                    
                    attacker = players[0]
                    defender = players[1]

                    # To store all cards up for grabs
                    battle_cards = []

                    current_player = attacker
                    print('The attacker is {}. {}, look away!'.format(attacker.name, defender.name))
                    print('Cards in {}\'s hand: {}'.format(attacker.name, attacker.hand))
                    
                    attack_card = interface.getcard(self.deck)
                    battle_cards.append(self.play_a_card(attacker, attack_card))

                    current_player = defender
                    print('The defender is {}. {}, look away!\n'.format(defender.name, attacker.name))
                    print('Cards in {}\'s hand: {}\n'.format(defender.name, defender.hand))
                    print('The defender may accept the attack, ending their turn,')
                    print('or they may defend with a better card.\n')

                    while not end_turn:
                        # getting move from defender
                        current_player = defender
                        valid_cards = interface.getvalid(
                                trump_card.suit, battle_cards, defender.hand, 'defender')
                        print('You can play any of these cards from your hand: {}'.format(valid_cards))
                        
                        d_move = interface.getmove()
                    
                        if d_move == 'pass':
                            for c in battle_cards:
                                    defender.hand.append(c)
                            print('Very well then. The card has been added to {}\'s hand.'.format(defender.name))
                            # Attacker gets to attack again if defender takes card on the first round
                            if not len(battle_cards) == 1:
                                players.reverse()
                            end_turn = True
                            continue
                        
                        if d_move == 'play':
                            
                            if len(valid_cards) == 0:
                                print('No valid card to play. Must take the attack.')
                                for c in battle_cards:
                                    defender.hand.append(c)
                                end_turn = True
                                continue

                            defender_card = interface.getcard(self.deck)
                            battle_cards.append(self.play_a_card(defender, defender_card))
    
                            print('{} has defended with {}'.format(defender.name, defender_card))                            
                        
                        print('{} may choose to pass or attack again.'.format(attacker.name))
                        
                        current_player = attacker
                        # Getting move from attacker
                        valid_cards = interface.getvalid(
                                trump_card.suit, battle_cards, attacker.hand, 'attacker')
                        print('You can play any of these cards from your hand: {}'.format(valid_cards))
                        a_move = interface.getmove()
                        
                        if a_move == 'pass':
                            # Cards on table are discarded, not added to attacker's hand
                            for c in battle_cards:
                                battle_cards.pop()
                            print('Very well then. The cards have been discarded.')
                            players.reverse()
                            end_turn = True
                            continue
                        
                        if a_move == 'play':
                            
                            if len(valid_cards) == 0:
                                print('No valid card to play. Must pass.')
                                for c in battle_cards:
                                    battle_cards.pop()
                                players.reverse()
                                end_turn = True
                                continue

                            attacker_card = interface.getcard(self.deck)
                            battle_cards.append(self.play_a_card(attacker, attacker_card))
    
                            print('{} has attacked with {}'.format(attacker.name, attacker_card))

                    if len(players[0].hand) == 0:
                        self.wins(players[0])
                        print('{} wins this round!'.format(players[0].name))
                        print('{} has {} wins.'.format(
                            players[0].name, players[0].wins))
                        print('{} has {} wins. First to 5 is the big winner!'.format(
                            players[1].name, players[1].wins))
                        break
                    elif len(players[1].hand) == 0:
                        self.wins(players[1])
                        print('{} wins this round!'.format(players[1].name))
                        print('{} has {} wins.'.format(
                            players[1].name, players[1].wins))
                        print('{} has {} wins. First to 5 is the big winner!'.format(
                            players[0].name, players[0].wins))
                        break
            
            if players[0].wins == 5:
                print('{} wins the game!'.format(players[0].name))
                game_on = False
            if players[1].wins == 5:
                print('{} wins the game!'.format(players[1].name))
                game_on = False

    def run_game(self, interface):
        # pygame.init()
        bounds = (1000, 600)
        window = pygame.display.set_mode(bounds)
        pygame.display.set_caption('Durak')
        icon = pygame.image.load('icons/poker.png')
        pygame.display.set_icon(icon)

        running = True
        while running:
            key = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    key = event.key
            
            interface.render_interface(window)
            self.play(interface,key)

if __name__ == "__main__":
        pygame.init()
        gamelogic = DurakGame()
        intObj = pyGame()
        gamelogic.run_game(intObj)
        # gamelogic.play(intObj)
