# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 13:53:32 2022

@author: emily
"""
from random import shuffle
from time import sleep
import pygame
from card_dictionary import card_files


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
                self.new_deck.append(Card(
                    self.rank[i], self.suit[j], self.value[i]))

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


class CmdLine():
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

        # These steps are to check that the player has typed in a valid card
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
            Attacker or defender. The valid cards vary depending on position
            of the player.

        Returns
        -------
        valid_cards : LIST
            Card objects that can be played.

        """
        valid_cards = []

        # If the attacker has a chance to attack a second time, they can only
        # play a card of the same rank as the last two cards on the table.
        if position == 'attacker':
            for c1 in list_of_cards[-2:]:
                for c2 in hand:
                    if c1.rank == c2.rank:
                        valid_cards.append(c2)

        # The defender may play any card with a higher rank but same suit than
        # the last card on the table or any card with the trump suit. If the
        # card on the table has the trump suit, the player can only play cards
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


class PyGame():
    """
    Unfinished object to host the pygame interface. When complete, this class
    will have corrollary functions to the command line version of the game.

    Functions:
    --------
        * render_interface(window)

    """
    def __init__(self):
        pass
    def render_interface(self, window):
        """
        Currently, this function displays a window where the game will take
        place when the GUI is created.

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
        window.blit(cardBack, (450, 100))

        # Text display
        font = pygame.font.SysFont('rockwell', 72, True)
        text = font.render('DUR         !', True, (255, 255, 255))
        window.blit(text, (350, 300))

        font = pygame.font.SysFont('rockwell', 24, True)
        text = font.render('Sorry, I can\'t finish the GUI!!', True, (255, 255, 255))
        window.blit(text, (350, 450))

        # Cards loaded
        cardImg1 = pygame.image.load('icons/ace-of-spades.png')
        window.blit(cardImg1, (485, 275))

        cardImg2 = pygame.image.load('icons/king-of-diamonds.png')
        window.blit(cardImg2, (570, 275))

        # Update window
        pygame.display.update()


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
        This function deals cards, picks the trump card, and determines who
        the first attacker is.

        Returns
        -------
        LIST
            The players in the order the turns will go.
        trump_card : OBJ
            Card object that determines the trump suit.

        """

        # First, the deck object is instantiated to create a shuffled deck
        self.deck = Deck()

        # Players are added to a list as objects
        self.players = []
        self.players.append(Player(self.p1))
        self.players.append(Player(self.p2))

        # A trump card is picked from the deck.
        trump_card = self.deck.set_trump()
        print('The trump card is {}, so the trump suit is {}.\n'.format(
            trump_card, trump_card.suit))
        sleep(3)

        # Six cards are dealt to each player. Meanwhile, if any of the cards
        # are of the trump suit, they are appended to the dealt_trumps list.
        dealt_trumps = []

        for p in range(len(self.players)):
            for c in range(0,6):
                card = self.deck.pick_card()
                self.players[p-1].hand.append(card)
                if card.suit == trump_card.suit:
                    dealt_trumps.append(card)

        # Players hands are sorted from lowest value to highest.
        self.players[0].hand.sort(key = lambda x: x.value)
        self.players[1].hand.sort(key = lambda x: x.value)

        print('The player with the lowest trump card goes first...')
        sleep(3)

        # The dealt_trumps list is sorted from lowest value to highest.
        dealt_trumps.sort(key=lambda x: x.value)

        # if neither player was dealt a trump, the player with the lowest card
        # over all goes first.
        if len(dealt_trumps) == 0:
            print('Oops, no one has a trump card!')
            print('Player with lowest card value goes first.')
            p1_lowest = self.players[0].hand
            p2_lowest = self.players[1].hand

            # The lowest card in player 1's hand is compared to the lowest
            # card in player 2's hand
            if p1_lowest[0] > p2_lowest[0]:
                print('{} has {} and is the first attacker!'.format(
                    self.players[1].name, p2_lowest[0]))

                # If player 1 has a larger lowest card than player 2, the list
                # is reversed so that player[1] becomes player[0]
                self.players.reverse()

            # Otherwise, the order of the list stays the same
            else:
                print('{} has {} and is the first attacker!'.format(
                    self.players[0].name, p2_lowest[0]))

            # If the lowest cards are equal, the next two are compared
            if p1_lowest[0] == p2_lowest[0]:
                print('Lowest cards are equal... checking next lowest card.')
                sleep(1)

                if p1_lowest[1] > p2_lowest[1]:
                    print('{} has {} and is the first attacker!'.format(
                        self.players[1].name, p2_lowest[1]))

                    # If player 1 has a larger second lowest card than player2,
                    # the list is reversed so that player[1] becomes player[0]
                    self.players.reverse()

                # Otherwise, the order of the list stays the same
                else:
                    print('{} has {} and is the first attacker!'.format(
                        self.players[0].name, p2_lowest[0]))

                # This is a final check just in case the next lowest cards were
                # also identical
                if p1_lowest[1] == p2_lowest[1]:
                    print('NEXT lowest cards are equal too! ')
                    print('Checking next lowest card...')
                    sleep(1)

                    if p1_lowest[2] > p2_lowest[2]:
                        print('{} has {} and is the first attacker!'.format(
                            self.players[1].name, p2_lowest[2]))

                        # If player 1 has a larger second lowest card than
                        # player 2, the list is reversed
                        self.players.reverse()

                    # Otherwise, the order of the list stays the same
                    else:
                        print('{} has {} and is the first attacker!'.format(
                            self.players[0].name, p2_lowest[0]))

        # If the lowest value trump suit card is in players[0]'s hand, they are
        # the first attacker
        elif dealt_trumps[0] in self.players[0].hand:
            print('{} has {} and is the first attacker!'.format(
                self.players[0].name, dealt_trumps[0]))

        # If the lowest value trump suit card is in player[1]'s hand, the order
        # of the list is reversed so that they are the first attacker
        elif dealt_trumps[0] in self.players[1].hand:
            print('{} has {} and is the first attacker!'.format(
                self.players[1].name, dealt_trumps[0]))
            self.players.reverse()

        return self.players, trump_card

    def wins(self, winner):
        """
        This function adds a win to a player object value 'wins'.

        Parameters
        ----------
        winner : OBJ
            Player who wins a round.

        Returns
        -------
        None.

        """
        w = '{} wins this round!'.format(winner.name)
        winner.wins += 1
        print(w)

    def deal(self, player, num = 1):
        """
        This function deals cards to a player from the deck. The default is 1.

        Parameters
        ----------
        player : OBJ
            Player receiving the card.
        num : INT, optional
            Number of cards to be dealt. The default is 1.

        Returns
        -------
        None.

        """
        # Card objects are removed from the deck and added to a player's hand
        # as long as there are cards in the deck
        for c in range(0, num):
            if len(self.deck.new_deck) == 0:
                break
            player.hand.append(self.deck.pick_card())

    def play_a_card(self, player, card):
        """
        This function removes a card from a player's hand to play

        Parameters
        ----------
        player : OBJ
            Player to play a card.
        card : STR
            User-defined card to play.

        Returns
        -------
        c : OBJ
            Card from player's hand

        """
        # If the string matches a card object in the player's hand, the
        # matching card object is played
        for c in player.hand:
            if str(c) == card:
                player.hand.remove(c)
                return c

    def play(self, interface, key = None, class_demo = False):
        """
        The main game engine.

        Parameters
        ----------
        interface : OBJ
            Can be a command line game (CmdLine) or a GUI (PyGame). The GUI has
            not been created.
        key : OBJ, optional
            Pygame event. The default is None.
        class_demo : BOOL, optional
            This allows the game to be ended early to make the class
            demonstration shorter. The default is False.

        Returns
        -------
        None.

        """
        # Game ends when game_on = False
        game_on = True

        # Names are retrieved depending on the interface
        self.p1, self.p2 = interface.getnames()

        while game_on:

            # The setup function returns the order of players and the trump
            # suit for the round.
            players, trump_card = self.setup()

            # Round level: round ends when a player runs out of cards
            while len(players[0].hand) > 0 and len(players[1].hand) > 0:

                # Turn level: turn ends if a player cannot or chooses not to
                # play a card
                for turn in range(1, 100):

                    # If the deck runs out of cards, players will not be dealt
                    # more. Otherwise, they will be dealt
                    # enough cards to start every turn with 6 cards.
                    out_of_cards = False

                    if not out_of_cards:
                        for p in players:
                            self.deal(p, (6-len(p.hand)))
                            if len(self.deck.new_deck) <= 0:
                                out_of_cards = True
                                print('Out of cards in the deck! Round ending soon.')

                    # Hands are sorted
                    for p in players:
                        p.hand.sort(key=lambda x: x.value)

                    # If this is a class demo, the round or game can be ended at the beginning
                    # of a turn to speed it up. If the answer is 'yes', the game will continue.
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

                    # When a player runs out of cards, they win the round and
                    # wins are added to that player object.
                    # The turn loop breaks.
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

                    # The attacker is the player listed first in the list.
                    attacker = players[0]
                    defender = players[1]

                    # To store all cards up for grabs on the table
                    battle_cards = []

                    # Attacker goes first. Defender is asked to look away from screen.
                    current_player = attacker
                    print('The attacker is {}. {}, look away!'.format(
                        attacker.name, defender.name))
                    sleep(5)
                    print('Cards in attacker {}\'s hand: {}'.format(
                        attacker.name, attacker.hand))

                    print('>>>Trump suit: {}<<<'.format(trump_card.suit))

                    # Player chooses card to attack.
                    attack_card = interface.getcard(self.deck)

                    # The card is added to the list to keep track of played cards
                    battle_cards.append(self.play_a_card(attacker, attack_card))

                    print('__________________________________________')
                    print('\nAttacker {} has played {}'.format(attacker.name, attack_card))
                    print('__________________________________________')
                    print('__________________________________________')
                    print('__________________________________________')
                    print('__________________________________________')
                    print('__________________________________________')
                    print('__________________________________________')

                    end_turn = False

                    while not end_turn:

                        # Defender's turn (attacker must look away)
                        # current_player = defender
                        print('\nThe defender is {}. {}, look away!\n'.format(
                            defender.name, attacker.name))
                        sleep(5)
                        print('Cards in {}\'s hand: {}\n'.format(
                            defender.name, defender.hand))
                        print('\nThe defender may accept the attack, ending their turn,')
                        print('or they may defend with a better card if they have one.\n')
                        sleep(2)

                        # Valid defender cards are collected
                        valid_cards = interface.getvalid(
                                trump_card.suit, battle_cards, defender.hand,
                                'defender')

                        # If there are no valid cards, the defender must add the
                        # battle cards to their hand
                        if len(valid_cards) == 0:
                            print('No valid card to play.')
                            print('{} must take the attack and add cards to their hand.'
                                  .format(defender.name))
                            sleep(3)

                            for c in battle_cards:
                                defender.hand.append(c)

                            # This ends the current turn and moves to the next one.
                            end_turn = True
                            continue

                        # If there are valid cards to play, they will be shown here.
                        print('{}, you can play any of these cards from your hand: {}'.format(
                            current_player.name, valid_cards))
                        print('>>>Trump suit: {}<<<'.format(trump_card.suit))

                        # User decides whether to pass on the defense or play a defense
                        d_move = interface.getmove()

                        if d_move == 'pass':

                            # If pass, the defender must add battle card(s) to their hand.
                            for c in battle_cards:
                                defender.hand.append(c)
                            print('The card has been added to {}\'s hand.'.format(defender.name))
                            sleep(3)

                            # Attacker gets to attack again for the next turn
                            # if defender takes card on the first card.
                            # If more cards have been played, the defender is
                            # the next attacker.
                            if len(battle_cards) != 1:
                                players.reverse()

                            # This ends turn and moves to the next
                            end_turn = True
                            continue

                        if d_move == 'play':

                            # If the defender decides to play, they provide
                            # which card to play.
                            defender_card = interface.getcard(self.deck)
                            battle_cards.append(self.play_a_card(
                                defender, defender_card))

                            print('__________________________________________')
                            print('\nDefender {} has defended with {}'.format(
                                defender.name, defender_card))
                            print('__________________________________________')
                            print('__________________________________________')
                            print('__________________________________________')
                            print('__________________________________________')
                            print('__________________________________________')
                            print('__________________________________________')
                            print('__________________________________________')
                            sleep(3)

                        # The attacker's turn. They may attack again or pass.
                        current_player = attacker

                        print('\nThe attacker may choose to pass or attack again.')
                        print('The attacker is {}. {}, look away!'.format(
                            attacker.name, defender.name))
                        sleep(5)
                        print('Cards in {}\'s hand: {}\n'.format(
                            attacker.name, attacker.hand))

                        # Getting move from attacker
                        valid_cards = interface.getvalid(
                                trump_card.suit, battle_cards, attacker.hand,
                                'attacker')

                        # If there are no valid cards, the cards on the table
                        # are discarded and the turn is over
                        if len(valid_cards) == 0:
                            print('No valid card to play. Must pass and discard cards.')
                            sleep(3)
                            for c in battle_cards:
                                battle_cards.pop()

                            # The defender becomes the next attacker
                            players.reverse()
                            end_turn = True
                            continue

                        print('{}, you can play any of these cards from your hand: {}'
                              .format(attacker.name, valid_cards))
                        print('>>>Trump suit: {}<<<'.format(trump_card.suit))

                        # Attacker decides which move to make
                        a_move = interface.getmove()

                        if a_move == 'pass':

                            # Cards on table are discarded, not added to attacker's hand
                            for c in battle_cards:
                                battle_cards.pop()
                            print('Very well then. The cards have been discarded.')
                            sleep(3)

                            # The defender is the next attacker, and the turn is over.
                            players.reverse()
                            end_turn = True
                            continue

                        if a_move == 'play':

                            # If the attacker decides to play, they provide
                            # which card they wish to play
                            attacker_card = interface.getcard(self.deck)
                            battle_cards.append(self.play_a_card(attacker, attacker_card))

                            print('__________________________________________')
                            print('\n{} has attacked with {}'.format(
                                attacker.name, attacker_card))
                            print('__________________________________________')
                            print('__________________________________________')
                            print('__________________________________________')
                            print('__________________________________________')
                            print('__________________________________________')
                            print('__________________________________________')
                            print('__________________________________________')

            # The first player to 5 wins, wins the entire game
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
        """
        This function runs the engine through the GUI only if the interface = PyGame()

        Parameters
        ----------
        interface : OBJ
            must be PyGame.

        Returns
        -------
        None.

        """
        # Pygame package is initiated
        pygame.init()

        # Size of window and title are set
        bounds = (1000, 600)
        window = pygame.display.set_mode(bounds)
        pygame.display.set_caption('Durak')
        icon = pygame.image.load('icons/poker.png')
        pygame.display.set_icon(icon)

        # The game loop. While running, the GUI is active.
        running = True
        while running:
            key = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    key = event.key

            interface.render_interface(window)
            pygame.display.update()

if __name__ == "__main__":
    gamelogic = DurakGame()
    intObj = CmdLine()
    
    # Run if intObj = PyGame()
    # gamelogic.run_game(intObj)

    # Run if intObj = CmdLine()
    gamelogic.play(intObj, class_demo = True)
