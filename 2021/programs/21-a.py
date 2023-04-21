#!/usr/bin/python3

import sys

BOARD_SIZE = 10

class Player:
    def __init__(self, position):
        self.pos = position - 1
        self.score = 0

    def move(self, num):
        self.pos += num
        self.pos %= BOARD_SIZE 
        self.score += self.pos + 1

class DeterministicD100:
    def __init__(self):
        self.num = 0
        self.num_rolls = 0

    def roll(self):
        num = self.num + 1
        self.num = num
        self.num %= 100
        self.num_rolls += 1
        return num

def game_over(players):
    return max(player.score for player in players) >= 1000


def main(inputs):
    players = [Player(int(input)) for input in inputs]
    die = DeterministicD100()
    current_player = 0
    while not game_over(players):
        move = sum(die.roll() for _ in range(3))
        players[current_player].move(move)
        # print(f'{current_player} rolls {move} -- score now {players[current_player].score}')
        current_player += 1
        current_player %= len(players)
    
    loser_score = min(player.score for player in players)
    print(f"Loser's score: {loser_score}")
    print(f'{die.num_rolls} rolls')
    print(f'Product {loser_score * die.num_rolls}')
    

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
