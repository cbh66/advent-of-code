#!/usr/bin/python3

import sys
from pprint import pprint
import functools
import itertools

BOARD_SIZE = 10

class Player:
    def __init__(self, score, pos):
        self.score = score
        self.pos = pos - 1

    def move(self, num):
        pos = (self.pos + num) % BOARD_SIZE
        score = self.score + self.pos + 1
        return Player(score, pos)

quantum_rolls = [
    0,
    0,
    0,
    1,
    3,
    6,
    7,
    6,
    3,
    1
]

def game_over(all_scores):
    return max(
        max(
            max(score for score in pos)
            for pos in player_positions
        ) for player_positions in all_scores
    ) == 0

# returns [num_wins, new_player_scores]
def next_quantum_move(player_scores):
    num_wins = 0
    new_player_scores = [[0] * 22 for _ in range(BOARD_SIZE)]
    for current_space in range(len(player_scores)):
        for roll in range(len(quantum_rolls)):
            new_space = current_space + roll
            new_space %= BOARD_SIZE
            for current_score in range(len(player_scores[current_space])):
                new_score = current_score + new_space + 1
                num_universes = player_scores[current_space][current_score] * quantum_rolls[roll]
                if new_score >= 21:
                    num_wins += num_universes
                else:
                    new_player_scores[new_space][new_score] += num_universes
    return [num_wins, new_player_scores]

# indexed as cache[p1_pos][p2_pos][p1_score][p2_score][current_move]
#       == [p1_wins, p2_wins] or None
cache = [
    [
        [
            [[None] * 2 for _ in range(22)]
            for _ in range(22)
        ] for _ in range(BOARD_SIZE)
    ] for _ in range(BOARD_SIZE)
]

def wins(players, current_move=0):
    if players[0].score >= 21:
        return [1, 0]
    if players[1].score >= 21:
        return [0, 1]
    maybe_cached_val = cache[players[0].pos][players[1].pos][players[0].score][players[1].score]
    if maybe_cached_val[current_move] is not None:
        return maybe_cached_val[current_move]
    total_wins = [0] * 2
    for roll in range(len(quantum_rolls)):
        if quantum_rolls[roll] > 0:
            next_players = [
                players[i].move(roll) if i == current_move else players[i]
                for i in range(len(players))
            ]
            [p1_wins, p2_wins] = wins(next_players, (current_move + 1) % 2)
            total_wins[0] += (p1_wins * quantum_rolls[roll])
            total_wins[1] += (p2_wins * quantum_rolls[roll])

    maybe_cached_val[current_move] = total_wins
    return total_wins



dirac_die = [1, 2, 3]
 
 
@functools.lru_cache(maxsize=None)
def play_round(current_score, other_score, current_pos, other_pos):
    if current_score >= 21:
        return 1, 0
    if other_score >= 21:
        return 0, 1
    score = (0, 0)
    for (d1, d2, d3) in itertools.product(dirac_die, dirac_die, dirac_die):
        new_current_pos = (current_pos + d1 + d2 + d3) % 10
        new_current_pos = new_current_pos % 10
        new_current_score = current_score + new_current_pos + 1
        p2_wins, p1_wins = play_round(
            other_score,
            new_current_score,
            other_pos,
            new_current_pos,
        )
        score = (score[0] + p1_wins, score[1] + p2_wins)
    return score


def main(inputs):
    # indexed like player_scores[p][m][s] where p is player, m is what space
    # they're on, and s is the score on that space. Contains a num representing
    # number of universes where that player is on that space with that score
    # player_scores = [[[0] * 22 for _ in range(BOARD_SIZE)] for _ in range(2)]
    # player_wins = [0] * 2
    # for i in range(len(inputs)):
    #     player_scores[i][int(inputs[i]) - 1][0] = 1
    players = [Player(0, int(inputs[i])) for i in range(len(inputs))]

    current_player = 0
    current_move = 0
    # for _ in range(10):
    print(play_round(0, 0, int(inputs[0]) - 1, int(inputs[1]) - 1))
    # while not game_over(player_scores):
    #     [wins, new_scores] = next_quantum_move(player_scores[current_player])
    #     player_wins[current_player] += wins
    #     player_scores[current_player] = new_scores
    #     print(f'Move {current_move}')
    #     print(f'Player {current_player} has {player_wins[current_player]} wins')
    #     pprint(player_scores[current_player])
    #     current_move += 1
    #     current_player += 1
    #     current_player %= len(player_scores)
    
    # print(player_wins)
    # loser_score = min(player.score for player in players)
    # print(f"Loser's score: {loser_score}")
    # print(f'{die.num_rolls} rolls')
    # print(f'Product {loser_score * die.num_rolls}')
    

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
