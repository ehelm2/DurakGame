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
    """
    A card object.
    
    Values:
    --------
        * rank (str)
        * suit (str)
        * value (int)

    Functions:
    --------
        * __init__(rank, suit, value)
        * __lt__ (card2)
        * __gt__(card2)
        *__repr__
    """
    def __init__(self, rank, suit, value):
        self.rank = rank
        self.suit = suit
        self.value = value
        
    def __lt__(self, card2):
        """
        A function to determine if a card is less than another card.

        Parameters
        ----------
        card2 : OBJ
            A second card to be compared.

        Returns
        -------
        bool
            Returns True if the value of self is less than 
                the value of a second card.
            Otherwise, False is returned.

        """
        if self.value < card2.value:
            return True
        return False
    
    def __gt__(self, card2):
        """
        A function to determine if a card is greater than another card.

        Parameters
        ----------
        card2 : OBJ
            A second card to be compared.

        Returns
        -------
        bool
            Returns True if the value of self is greater than 
                the value of a second card.
            Otherwise, False is returned.

        """
        if self.value > card2.value:
            return True
        return False
        
    def __repr__(self):
        """
        When a card is printed on the command line, 
            it is represented as a readable string.

        Returns
        -------
        card : STR
            The readable description of the card.

        """
        card = '{} of {}'.format(self.rank, self.suit)
        return card


class Deck:
    """
    A card object.

    Functions:
    --------
        * __init__
        * pick_card
        * set_trump
        * compare(card1, card2, trump)
    """
    
    def __init__(self):
        """
        When Deck is initialized, it is filled with Card objects and shuffled.

        Returns
        -------
        None.

        """
        self.new_deck = []
        self.rank = ['Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
        self.suit = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        self.value = [6, 7, 8, 9, 10, 11, 12, 13, 14]
        
        # A deck is created from the possible ranks and suits and then shuffled.
        for i in range(len(self.rank)):
            for j in range(len(self.suit)):
                self.new_deck.append(Card(self.rank[i], self.suit[j], self.value[i]))
                
        shuffle(self.new_deck)
    
    def pick_card(self):
        """
        This function picks a card from the deck.

        Returns
        -------
        OBJ
            Last card in deck is removed and returned.

        """
        # If the deck is empty, no cards are returned.
        if len(self.new_deck) == 0:
            return
        
        # Otherwise, the last card in the deck is popped out.
        return self.new_deck.pop()
    
    def set_trump(self):
        """
        A card is picked from the deck that becomes the trump card.
        The suit of this card beats all other cards not of that suit.

        Returns
        -------
        trump : OBJ
            Card object.

        """
        trump = self.pick_card()
        
        return trump


class Player:
    """
    A Player object.
    
    Values:
    --------
        * name
        * wins
        * hand
        * card
        
    Functions:
    --------
        * __init__(name)

    """
    def __init__(self, name = None):
        
        # Each player object contains the player's name, the number of wins, 
        # and their hand of cards.
        
        self.name = name
        self.wins = 0
        self.hand = []


class Interface:
    """
    This Interface object is currently a placeholder for any functions that might be
    shared between the command line version of the game and the unfinished GUI version.
    
    """
    pass

    
class CmdLine(Interface):
    """
    An object that holds functions for the command line version of the game.
        
    Functions:
    --------
        * getnames
        * getcard(deck_obj)
        * getmove
        * getvalid(trump_suit, list_of_cards, hand, position))

    """
    def getnames(self):
        """
        Have players enter their names in the command line.

        Returns
        -------
        OBJ
            Player 1 object.
        OBJ
            Player 2 object.

        """
        self.p1 = input('Enter Player 1\'s Name: ')
        self.p2 = input('Enter Player 2\'s Name: ')
        
        return self.p1, self.p2
    
    def getcard(self, deck_obj):
        """
        Have player type card they wish to play in command line

        Parameters
        ----------
        deck_obj : OBJ
            Deck object.

        Returns
        -------
        selected_card : STR
            A string that describes the card that the player wants to play.

        """
        selected_card = str(input('Which card would you like to play? '))
        
        # The following steps are to check that the player has typed in a valid card
        check_string = selected_card.split(' ')
        
        # The string must follow the form "{Rank} of {Suit}"
        while not len(check_string) == 3:
            print('Please type as seen on screen. Try again!')
            selected_card = str(input('Which card would you like to play? '))
            check_string = selected_card.split(' ')            
        
        # The rank and suit must be found in the deck object
        while not check_string[0] in deck_obj.rank and not check_string[2] in deck_obj.suit:
            print('Please check spelling and capitalization. Try again!')
            selected_card = str(input('Which card would you like to play? '))
            check_string = selected_card.split(' ')

        return selected_card
    
    def getmove(self):
        """
        Have user decide whether to skip their turn (pass) or play a card

        Returns
        -------
        STR
            The move the player wants to make.

        """
        selected_move = input('What would you like to do? Pass or Play? ')
        
        available_moves = ['pass', 'play']
        
        # The spelling must be correct, but case does not matter
        while not selected_move.lower() in available_moves:
            print('Oops try typing \'pass\' or \'play\'')
            selected_move = input('What would you like to do? Pass or Play? ')
        
        return selected_move.lower()
    
    def getvalid(self, trump_suit, list_of_cards, hand, position):
        """
        Find the cards that can be played

        Parameters
        ----------
        trump_suit : STR
            Suit of trump card object.
        list_of_cards : LIST
            Card objects on the table.
        hand : LIST
            Player's hand of cards. Stored in player object.
        position : STR
            Attacker or defender. The valid cards vary depending on position of the player.

        Returns
        -------
        valid_cards : LIST
            Card objects that can be played.

        """
        valid_cards = []
        
        # If the attacker has a chance to attack a second time, they can only play a card of
        # the same rank as the last two cards on the table.
        if position == 'attacker':
            for c1 in list_of_cards[-2:]:
                for c2 in hand:
                    if c1.rank == c2.rank:
                        valid_cards.append(c2)             
        
        # The defender may play any card with a higher rank but same suit than the last card on the table or any
        # card with the trump suit. If the card on the table has the trump suit, the player can only play cards 
        # of the trump suit that have a higher rank.
        if position == 'defender':
            for c in hand:
                if c.suit == list_of_cards[-1].suit and c > list_of_cards[-1]:
                    valid_cards.append(c)
                if c.suit == trump_suit and list_of_cards[-1] != trump_suit:
                    valid_cards.append(c)
                if c.suit == trump_suit and list_of_cards[-1].suit == trump_suit:
                    if c > list_of_cards[-1]:
                        valid_cards.append(c)
            
            # Any duplicates are removed from the valid cards list.
            valid_cards = [*set(valid_cards)]
        
        # The list of valid cards is sorted by value
        valid_cards.sort(key = lambda x: x.value)
        
        return valid_cards
      
class PyGame(Interface):
    """
    Unfinished object to host the pygame interface. All functions are placeholders 
    that will be the GUI corrollary to the command line version of the game.
        
    Functions:
    --------
        * __init__
        * render_interface(window)
        * getnames
        * getcard
        * getmove
        * getvalid(trump_suit, list_of_cards, hand, position))

    """    
    def __init__(self):
        pass
    
    def render_interface(self, window):
        """
        Currently, this function displays a window where the game will take place when the GUI is created.

        Parameters
        ----------
        window : OBJ
            Pygame game window.

        Returns
        -------
        None.

        """
        # Green background
        window.fill((25, 130, 56))
        
        # Card design loaded
        cardBack = pygame.image.load('icons/design1.png')
        window.blit(cardBack, (300, 100))
        
        # Text display
        font = pygame.font.SysFont('rockwell', 48, True)
        text = font.render('Work in progress!', True, (255, 255, 255))
        window.blit(text,(100, 500))
        
        # Update window
        pygame.display.update()

    def getnames(self):
        pass
    
    def getcard(self):
        pass
    
    def getmove(self):
        pass
    
    def getvalid(self):
        pass
   
class DurakGame:
    """
    The main game object.
    
    Functions:
    --------
        * setup
        * wins(winner)
        * deal(player, num = 1)
        * play_a_card(player, card)
        * play(interface, key = None, class_demo = False)
        * run_game(interface)

    """
    def setup(self):
        """
        

        Returns
        -------
        TYPE
            DESCRIPTION.
        trump_card : TYPE
            DESCRIPTION.

        """
        
        self.deck = Deck()
        self.players = []
        
        self.players.append(Player(self.p1))
        self.players.append(Player(self.p2))

        trump_card = self.deck.set_trump()
        print('The trump card is {}, so the trump suit is {}.\n'.format(trump_card, trump_card.suit))
        sleep(3)

        dealt_trumps = []
        for p in range(len(self.players)):
            for c in range(0,6):
                card = self.deck.pick_card()
                self.players[p-1].hand.append(card)
                if card.suit == trump_card.suit:
                    dealt_trumps.append(card)

        self.players[0].hand.sort(key = lambda x: x.value)
        self.players[1].hand.sort(key = lambda x: x.value)

        print('The player with the lowest trump card goes first...')
        sleep(3)

        dealt_trumps.sort(key=lambda x: x.value)
        
        if len(dealt_trumps) == 0:
            print('Oops, no one has a trump card! Player with lowest card value goes first.')
            p1_lowest = self.players[0].hand
            p2_lowest = self.players[1].hand
            
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

    def play(self, interface, key = None, class_demo = False):
        
        game_on = True

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

                    if class_demo:
                        valid_response = False

                        while not valid_response:
                            stopping_point = input('Continue? ')

                            if stopping_point.lower() == 'yes':
                                valid_response = True
                            if stopping_point.lower() == 'end round':
                                valid_response = True
                            if stopping_point.lower() == 'end game':
                                players[0].wins = 5
                                valid_response = True
                                
                        if stopping_point == 'end round':
                            for c in players[0].hand:
                                    print(c)
                                    players[0].hand = []

                        if stopping_point == 'end game':
                            players[0].hand = []
                            players[0].wins = 4                            
                    
                    if len(players[0].hand) == 0:
                        self.wins(players[0])
                        sleep(2)
                        print('{} wins this round!'.format(players[0].name))
                        print('{} has {} wins.'.format(
                            players[0].name, players[0].wins))
                        print('{} has {} wins. First to 5 wins the game!'.format(
                            players[1].name, players[1].wins))
                        sleep(2)
                        break

                    elif len(players[1].hand) == 0:
                        self.wins(players[1])
                        sleep(2)
                        print('{} wins this round!'.format(players[1].name))
                        print('{} has {} wins.'.format(
                            players[1].name, players[1].wins))
                        print('{} has {} wins. First to 5 wins the game!'.format(
                            players[0].name, players[0].wins))
                        sleep(2)
                        break
                    
                    print('~~~~~~~~~')
                    print('TURN %i' % turn)
                    print('~~~~~~~~~')
                    
                    attacker = players[0]
                    defender = players[1]

                    # To store all cards up for grabs
                    battle_cards = []

                    current_player = attacker
                    print('The attacker is {}. {}, look away!'.format(attacker.name, defender.name))
                    sleep(5)
                    print('Cards in attacker {}\'s hand: {}'.format(attacker.name, attacker.hand))
                    
                    print('Trump suit: {}'.format(trump_card.suit))
                    attack_card = interface.getcard(self.deck)
                    battle_cards.append(self.play_a_card(attacker, attack_card))
                    print('__________________________________________')
                    print('\nAttacker {} has played {}'.format(attacker.name, attack_card))
                    print('__________________________________________')

                    current_player = defender
                    print('\nThe defender is {}. {}, look away!\n'.format(defender.name, attacker.name))
                    sleep(5)
                    print('Cards in {}\'s hand: {}\n'.format(defender.name, defender.hand))
                    print('\nThe defender may accept the attack, ending their turn,')
                    print('or they may defend with a better card if they have one.\n')
                    sleep(2)
                    
                    end_turn = False
                    
                    while not end_turn:
                        # getting move from defender
                        current_player = defender
                        valid_cards = interface.getvalid(
                                trump_card.suit, battle_cards, defender.hand, 'defender')
                        
                        if len(valid_cards) == 0:
                                print('No valid card to play.') 
                                print('{} must take the attack and add cards to their hand.'.format(defender.name))
                                
                                sleep(3)
                                for c in battle_cards:
                                    defender.hand.append(c)
                                end_turn = True
                                continue
                        
                        print('{}, you can play any of these cards from your hand: {}'.format(current_player.name, valid_cards))
                        print('Trump suit: {}'.format(trump_card.suit))
                        
                        d_move = interface.getmove()
                    
                        if d_move == 'pass':

                            for c in battle_cards:
                                    defender.hand.append(c)
                            print('Very well then. The card has been added to {}\'s hand.'.format(defender.name))
                            sleep(3)
                            
                            # Attacker gets to attack again if defender takes card on the first round
                            if not len(battle_cards) == 1:
                                players.reverse()
                            end_turn = True
                            continue
                        
                        if d_move == 'play':

                            defender_card = interface.getcard(self.deck)
                            battle_cards.append(self.play_a_card(defender, defender_card))
                            
                            print('__________________________________________')
                            print('\nDefender {} has defended with {}'.format(defender.name, defender_card))
                            print('__________________________________________')
                            sleep(3)

                        current_player = attacker

                        print('\nThe attacker may choose to pass or attack again.')
                        print('The attacker is {}. {}, look away!'.format(attacker.name, defender.name))
                        sleep(5)
                        print('Cards in {}\'s hand: {}\n'.format(attacker.name, attacker.hand))
                        # Getting move from attacker
                        valid_cards = interface.getvalid(
                                trump_card.suit, battle_cards, attacker.hand, 'attacker')

                        if len(valid_cards) == 0:
                                print('No valid card to play. Must pass and discard cards.')
                                sleep(3)
                                for c in battle_cards:
                                    battle_cards.pop()
                                players.reverse()
                                end_turn = True
                                continue

                        print('{}, you can play any of these cards from your hand: {}'.format(attacker.name, valid_cards))
                        print('Trump suit: {}'.format(trump_card.suit))
                        a_move = interface.getmove()
                        
                        if a_move == 'pass':

                            # Cards on table are discarded, not added to attacker's hand
                            for c in battle_cards:
                                battle_cards.pop()
                            print('Very well then. The cards have been discarded.')
                            sleep(3)
                            players.reverse()
                            end_turn = True
                            continue
                        
                        if a_move == 'play':

                            attacker_card = interface.getcard(self.deck)
                            battle_cards.append(self.play_a_card(attacker, attacker_card))

                            print('__________________________________________')
                            print('\n{} has attacked with {}'.format(attacker.name, attacker_card))
                            print('__________________________________________')

            if players[0].wins == 5:
                print('***********************')
                print('\n{} wins!'.format(players[0].name))
                print('\n***********************')
                game_on = False
            if players[1].wins == 5:
                print('***********************')
                print('\n{} wins!'.format(players[1].name))
                print('\n***********************')
                game_on = False

    def run_game(self, interface):
        pygame.init()
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
            # self.play(interface,key)

if __name__ == "__main__":
        gamelogic = DurakGame()
        intObj = CmdLine()
        if intObj == PyGame():
            gamelogic.run_game(intObj)
        else:
            gamelogic.play(intObj, class_demo = True)
