import numpy as np
from copy import copy, deepcopy
import random
from genetic_helpers import * 


class Genetic_AI:
    def __init__(self, genotype=None, aggregate='lin', num_features=9, mutate=False,  noise_sd=.2):

        if(genotype is None):
            # randomly init genotype [-1, 1]
            self.genotype = np.array([random.uniform(-1, 1) for _ in range(num_features)])
        else: 
            if(mutate == False):
                self.genotype = genotype
            else: 
                # mutate given genotype
                mutation = np.array([np.random.normal(1, noise_sd) for i in range(num_features)])
                self.genotype = genotype * mutation

        self.fit_score = 0.0
        self.fit_rel = 0.0
        self.aggregate = aggregate


    def __lt__(self, other):
        return (self.fit_score<other.fit_score)
        

    def valuate(self, board, aggregate='lin'):
        """
        """

        peaks = get_peaks(board)
        highest_peak = np.max(peaks)
        holes = get_holes(peaks, board)
        wells = get_wells(peaks)

        rating_funcs = {
            'agg_height': np.sum(peaks),
            'n_holes': np.sum(holes),
            'bumpiness': get_bumpiness(peaks),
            'num_pits': np.count_nonzero(np.count_nonzero(board, axis=0) == 0),
            'max_wells': np.max(wells),
            'n_cols_with_holes': np.count_nonzero(np.array(holes) > 0),
            'row_transitions': get_row_transition(board, highest_peak), 
            'col_transitions': get_col_transition(board, peaks),
            'cleared': np.count_nonzero(np.mean(board, axis=1))
        } 

        # only linear will work right now, need to extend genotype for exponents to add more
        aggregate_funcs = {
            'lin': lambda gene, ratings: np.dot(ratings, gene), 
            'exp': lambda gene, ratings: np.dot(np.array([ratings[i]**gene[i] for i in range(len(ratings))]), gene), 
            'disp': 0 
        }

        ratings = np.array([*rating_funcs.values()], dtype=float)
        aggregate_rating = aggregate_funcs[aggregate](self.genotype, ratings)

        return aggregate_rating


    def get_best_move(self, board, piece):
        """
        Gets the best for move an agents base on board, next piece, and genotype
        """

        best_x = -1000
        max_value = -1000
        best_piece = None
        for i in range(4):
            piece = piece.get_next_rotation()
            for x in range(board.width):
                try:
                    y = board.drop_height(piece, x)
                except:
                    continue

                board_copy = deepcopy(board.board)
                for pos in piece.body:
                    board_copy[y + pos[1]][x + pos[0]] = True
                
                np_board = bool_to_np(board_copy)
                c = self.valuate(np_board)
                
                if c > max_value:
                    max_value = c
                    best_x = x
                    best_piece = piece
        return best_x, best_piece


        
