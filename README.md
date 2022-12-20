# DurakGame
Emily Helm (@ehelm2)
Final project: A card game that can be played on the command line (with future capability to play on a GUI!)

# General Information
Durak means 'Idiot!' in Russian. A player is the durak if they lose all of their cards. The game is set up with a 36-card deck of playing cards (all cards above 6, and 
Ace is the highest). A card is pulled from the deck that is called the trump card. The suit of this card trumps cards of other suits. The player with the lowest card 
with the trump suit is the attacker. The attacker can play any card (but it is best to avoid trump cards at the beginning). If the played card is not a trump card, the 
defender may play any card higher than the played card to defend against the attack. The attacker may choose to play again, but they can only play a card with the same 
value of one that has already been played. The defender must defend against that card the same way. If at any point the defender cannot play or chooses not to play, they 
must add the played cards to their hand. If the attacker cannot play or chooses not to play at any point, the played cards get discarded. The turn ends, and the defender 
becomes an attacker. If the defender couldn't play after the first card, the attacker gets to attack again on the next turn. At the beginning of each turn, each player 
must have at least 6 cards. The first player to get rid of their cards wins the round, and the first player to 5 wins, wins the game (and is NOT the durak!).

This game requires two players to play on the same computer. Prompts are given so that players have time to turn away before the other player sees their cards.

# Usage
- Whether or not the user wishes to use the GUI part of the game, the pygame package must be installed.

`pip install pygame`

- Clone all files from this repository
- The entire game engine is in DurakGame.py. The file card_dictionary.py is used to store card images for the GUI.
- To run the game, type the following into the terminal:

`python DurakGame.py`

or

`python3 DurakGame.py`

- The default of this game is to be run on the command line, which is also the only interface that works. Since I had hoped to have a GUI for this project,
  I allow the GUI interface to run, but only a window pops up. To see this window, make the following changes in the main block at the bottom of the script:
  
  `if __name__: '__main__':`
      `gamelogic = DurakGame()`
      `intObj = PyGame()`

      `# gamelogic.run_game(intObj)`
      `gamelogic.play(intObj, class_demo = True)`
      
    Otherwise, keep intObj = PyGame(), run gamelogic.run_game(intObj), and comment out gamelogic.play(intObj, class_demo = True).
    
 - class_demo = True is to help in presenting the game for the final presentation. The game can be ended early when prompted.


# Icon References
Game Icon: <a href="https://www.flaticon.com/free-icons/playing-cards" title="playing cards icons">Playing cards icons created by bearicons - Flaticon</a>

Cards: <a href="https://www.flaticon.com/free-icons/poker-cards" title="poker cards icons">Poker cards icons created by rizal2109 - Flaticon</a>
Card design: <a href="https://www.flaticon.com/free-icons/pattern" title="pattern icons">Pattern icons created by Freepik - Flaticon</a>
