import numpy as np
from collections import defaultdict
from board import Board
from copy import deepcopy
from piece import Piece
from greedy import Greedy_AI

"""
Performs MCTS to return the best move
"""

greed = Greedy_AI()


class MCTS_AI:
    def get_best_move(self, board, piece):
        initial_state = State(board, piece, 0)
        root = MonteCarloTreeSearchNode(initial_state)
        selected_node = root.best_action()
        action = selected_node.parent_action
        x, piece = action[1], action[0]
        return x, piece


class State:
    def __init__(self, board, piece, depth, cleared=0):
        self.board = board
        self.piece = piece
        self.depth = depth
        self.cleared = cleared

    def get_legal_actions(self):
        actions = []
        p = self.piece
        for i in range(4):
            p = p.get_next_rotation()
            for x in range(self.board.width):
                try:
                    y = self.board.drop_height(p, x)
                except:
                    continue
                action = (p, x, y)
                actions.append(action)
        return actions

    def move(self, action):
        board_copy = Board()
        arr = deepcopy(self.board.board)
        widths = deepcopy(self.board.widths)
        heights = deepcopy(self.board.heights)
        board_copy.board = arr
        board_copy.widths = widths
        board_copy.heights = heights
        p, x, y = action
        board_copy.place(x, y, p)
        cleared = board_copy.clear_rows()
        return State(board_copy, Piece(), self.depth + 1, self.cleared + cleared)

    def is_game_over(self):
        return False

    def game_result(self):
        return -greed.cost0(self.board)


class MonteCarloTreeSearchNode:
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.simulations = 1
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._score = 0
        self._untried_actions = self.untried_actions()

    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def q(self):
        # wins = self._results[1]
        # loses = self._results[-1]
        # return wins - loses
        return self._score

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action
        )

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        return self.state.game_result()
        current_rollout_state = self.state

        while not current_rollout_state.is_game_over():

            possible_moves = current_rollout_state.get_legal_actions()

            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        self._number_of_visits += 1.0
        # self._results[result] += 1.0
        self._score += result
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):

        choices_weights = [
            (c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n()))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):

        return possible_moves[np.random.randint(len(possible_moves))]

        # return greed.get_best_move(self.state.board, self.state.piece)

    def _tree_policy(self):

        current_node = self
        while not current_node.is_terminal_node():

            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        for i in range(self.simulations):

            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.0)
