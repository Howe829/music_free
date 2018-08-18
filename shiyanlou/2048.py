import curses
from random import randrange,choice
from collections import defaultdict

actions = ['Up','Left','Down','Right','Restart','Exit']

letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']

actions_dict = dict(zip(letter_codes,actions*2))

def main(stdscr):

    def init():
        return 'Game'

    def not_game(state):

        responses = defaultdict(lambda :state)
        responses ['Restart'],responses['Exit'] = 'Init','Exit'
        responses[action]