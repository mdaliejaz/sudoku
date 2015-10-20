###########################################
# you need to implement five funcitons here
###########################################
import random


def do_backtracking(game):
    if game.is_complete_board():
        return True
    game.consistency_check += 1
    for i in xrange(game.N):
        for j in xrange(game.N):
            if game.board[i][j] == 0:
                for valid_number in game.possible_valid_numbers(i, j):
                    game.set_cell_value(i, j, valid_number)
                    if do_backtracking(game):
                        return True
                    game.set_cell_empty(i, j)
                return False


def backtracking(filename):
    ###
    # use backtracking to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###

    game = sudoku()
    game.read_input_board(filename)
    if do_backtracking(game):
        return game.result()
    return "Error: No Solution", 0


def do_backtrackingMRV(game):
    if game.is_complete_board():
        return True
    game.consistency_check += 1
    for i in xrange(game.N):
        for j in xrange(game.N):
            if game.board[i][j] == 0:
                mrv_pos = get_mrv_cell(game)
                sorted_numbers_by_lcv = sort_by_lcv(game, mrv_pos)
                for valid_number in sorted_numbers_by_lcv:
                    game.set_cell_value(mrv_pos[0], mrv_pos[1], valid_number)
                    if do_backtrackingMRV(game):
                        return True
                    game.set_cell_empty(mrv_pos[0], mrv_pos[1])
                return False


def get_mrv_cell(game):
    total_possible = game.N
    min_mrv_value = total_possible
    mrv_pos = None
    for i in xrange(total_possible - 1, -1, -1):
        for j in xrange(total_possible - 1, -1, -1):
            if game.board[i][j] == 0:
                cur_mrv_value = len(game.possible_valid_numbers(i, j))
                if cur_mrv_value <= min_mrv_value:
                    min_mrv_value = cur_mrv_value
                    mrv_pos = (i, j)
    return mrv_pos


def sort_by_lcv(game, mrv_pos):
    all_possible_numbers = game.possible_valid_numbers(mrv_pos[0], mrv_pos[1])
    sorted_numbers_by_lcv = sorted(all_possible_numbers,
                                   key=lambda x: game.total_constraints(mrv_pos[0], mrv_pos[1], x))
    return sorted_numbers_by_lcv


def backtrackingMRV(filename):
    ###
    # use backtracking + MRV to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###

    game = sudoku()
    game.read_input_board(filename)
    if do_backtrackingMRV(game):
        return game.result()
    return "Error: No Solution", 0


def do_backtrackingMRVfwd(game):
    if game.is_complete_board():
        return True
    game.consistency_check += 1
    for i in xrange(game.N):
        for j in xrange(game.N):
            if game.board[i][j] == 0:
                mrv_pos = get_mrv_cell(game)
                sorted_numbers_by_MrvFwd = sort_by_MrvFwd(game, mrv_pos)
                for valid_number in sorted_numbers_by_MrvFwd:
                    game.set_cell_value(mrv_pos[0], mrv_pos[1], valid_number)
                    if do_backtrackingMRV(game):
                        return True
                    game.set_cell_empty(mrv_pos[0], mrv_pos[1])
                return False


def sort_by_MrvFwd(game, mrv_pos):
    sorted_list_for_MrvFwd = sort_by_lcv(game, mrv_pos)
    for values in game.values_to_be_removed_for_MrvFwd:
        sorted_list_for_MrvFwd.remove(values)
    return sorted_list_for_MrvFwd


def backtrackingMRVfwd(filename):
    ###
    # use backtracking +MRV + forward propogation
    # to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###

    game = sudoku()
    game.read_input_board(filename)
    if do_backtrackingMRVfwd(game):
        return game.result()
    return "Error: No Solution", 0


def do_backtrackingMRVcp(game):
    return False


def backtrackingMRVcp(filename):
    ###
    # use backtracking + MRV + cp to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###

    game = sudoku()
    game.read_input_board(filename)
    if do_backtrackingMRVcp(game):
        return game.result()
    return "Error: No Solution", 0


def do_minConflict(game):
    # initial complete assignment
    # greedy minimal-conflict values for each variable

    max_steps = 1000
    for i in xrange(game.N):
        for j in xrange(game.N):

    for pos in game.get_positions():
        if not game.is_given(pos):
            game[pos] = min(game.get_values(),
                            key=lambda m: game.count_conflicts(pos, m))
    for _ in xrange(max_steps):
        if game.solved():
            return True
        con_pos = random.choice(game.get_conflicted_positions())
        lcv_move = min(game.get_values(),
                       key=lambda m: game.count_conflicts(con_pos, m))
        game[con_pos] = lcv_move
    return False


def minConflict(filename):
    ###
    # use minConflict to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###

    game = sudoku()
    game.read_input_board(filename)
    if do_minConflict(game):
        return game.result()
    return "Error: No Solution", 0


class sudoku():
    def __init__(self):
        self.board = None
        self.consistency_check = 0
        self.N = 0
        self.M = 0
        self.K = 0
        self.values_to_be_removed_for_MrvFwd = set()

    # def __str__(self):
    #     return '\n'.join(' '.join(str(x).rjust(2) for x in self.board[i])
    #                      for i in xrange(self.N))

    def read_input_board(self, filename):
        self.board = []
        f = open(filename, 'r')
        board_details = f.readline().strip().rstrip(';').split(',')
        self.N = int(board_details[0])
        self.M = int(board_details[1])
        self.K = int(board_details[2])
        for i in xrange(self.N):
            line = f.readline()
            row = line.strip().rstrip(';').split(',')
            for i in xrange(self.N):
                if row[i] == '-':
                    row[i] = 0
                else:
                    row[i] = int(row[i])
            self.board.append(row)
        f.close()

    def is_complete_board(self):
        for i in xrange(self.N):
            for j in xrange(self.N):
                if self.board[i][j] == 0:
                    return False
        return True

    def has_load_game(self):
        return self.board is not None

    def possible_valid_numbers(self, i, j):
        # self.consistency_check += 1
        invalid_numbers = set()
        valid_numbers = set()
        block_start_row = i / self.M * self.M
        block_start_column = j / self.K * self.K
        for counter in xrange(self.N):
            invalid_numbers.add(self.board[i][counter])
            invalid_numbers.add(self.board[counter][j])
            invalid_numbers.add(self.board[block_start_row + counter / self.K][block_start_column + counter % self.K])
        for numbers in xrange(1, self.N + 1):
            if numbers not in invalid_numbers:
                valid_numbers.add(numbers)
        return valid_numbers

    def set_cell_value(self, i, j, number):
        self.board[i][j] = number

    def set_cell_empty(self, i, j):
        self.board[i][j] = 0

    def result(self):
        return self.board, self.consistency_check

    def get_cells_affected(self, i, j):
        cells_affected = set()
        block_start_row = i / self.M * self.M
        block_start_column = j / self.K * self.K
        for counter in xrange(self.N):
            if self.board[i][counter] == 0:
                cells_affected.add((i, counter))
            if self.board[counter][j] == 0:
                cells_affected.add((counter, j))
            if self.board[block_start_row + counter / self.K][block_start_column + counter % self.K] == 0:
                cells_affected.add((block_start_row + counter / self.K, block_start_column + counter % self.K))
        cells_affected.discard((i, j))
        return cells_affected

    def total_constraints(self, i, j, affecting_value):
        total_possible_numbers = 0
        cells_affected = self.get_cells_affected(i, j)
        self.set_cell_value(i, j, affecting_value)
        for affected_cell in cells_affected:
            current_length = len(self.possible_valid_numbers(affected_cell[0], affected_cell[1]))
            if current_length == 0:
                self.values_to_be_removed_for_MrvFwd.add(affecting_value)
            total_possible_numbers += current_length
        self.set_cell_empty(i, j)
        return total_possible_numbers
