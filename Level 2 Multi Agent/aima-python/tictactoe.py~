"""
 Example illustrating use of minimax algorithm
 adapted by Eugene Agichtein for CS325: Artificial Intelligence
 Last update: 2/10/2014
"""


from games import TicTacToe # use class TicTacToe from games module
import random
from games import minimax_decision
from utils import *


class TicTacToeR(TicTacToe):
    'Subclass of TicTacToe that has X or O star at at random'

    def __init__(self, h=3, v=3, k=3):
        update(self, h=h, v=v, k=k)
        moves = [(x, y) for x in range(1, h+1)
                 for y in range(1, v+1)]
        self.initial = Struct(to_move='X', utility=0, board={}, moves=moves)
    
    def utility(self, state,player):
        "Return the value to X; 1 for win,- 1 for loss, 0 otherwise."
        if player == 'X':
            return state.utility
        else:
            return -state.utility

    
def play_game(game, *players):
    """Play an n-person, move-alternating game.
    this is modified from aima class to show the after each move and
    correcly call the utility method and game result"""
    state = game.initial
    while True:
        for player in players:
            print "now move for player ", player
            move = player(game, state) # update move
            state = game.make_move(move, state) # update game state
            print '---'
            game.display(state) # display board
            print '---'
            
            if move == None or game.terminal_test(state): #check game end
                if game.utility(state,'X')==1:
                    print 'X has won!'
                elif game.utility(state,'O')==1:
                    print 'O has won!'
                else:
                    print 'Its A Draw!'
                return #exit


def minimax_player(game, state):
    'a minimax player'
    if not game.terminal_test(state):
        move = minimax_decision(state, game)
        print "computer move: ", move
        return move
    else:
        return
    
def human_player(game, state):
    #read move from stdin
    print "Enter your move as row,column (range: 1-3,1-3)"
    legal=False
    while not legal:        
        move = tuple(int(x.strip()) for x in raw_input().split(','))
        if move in game.legal_moves(state): #must check whether move is legal
            legal=True
        else:
            print "Illegal move. Try again"
            
    print "Human moved: ", move
    return move



def main():
    'the main program'
    
    game = TicTacToeR() # create a new game object
    
    #print 'Machine vs Machine MiniMax TicTacToe - sit back and enjoy the ride'
    #play_game(game,minimax_player,minimax_player) # play the game

    print 'Machine vs. Human'
    play_game(game,minimax_player,human_player) # play the game
    print 'Now Human vs. Machine'
    play_game(game,human_player,minimax_player) # play the game



if __name__ == '__main__':
    main() # main() will be run if this py file is the top - level program and not imported as a module




