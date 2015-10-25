###########################################
# you need to implement five funcitons here
###########################################
import random


def do_backtracking(game):
    if game.is_complete_board():
        if game.is_valid_sudoku_board():
            return True
        else:
            return False
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
        if game.is_valid_sudoku_board():
            return True
        else:
            return False
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
                                   key=lambda x: game.total_constraints(mrv_pos[0], mrv_pos[1], x), reverse=True)
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
        if game.is_valid_sudoku_board():
            return True
        else:
            return False
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
    game.values_to_be_removed_for_MrvFwd = set()
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
    if game.is_complete_board():
        return True
    game.consistency_check += 1
    for i in xrange(game.N):
        for j in xrange(game.N):
            if game.board[i][j] == 0:
                mrv_pos = get_mrv_cell(game)
                sorted_numbers_by_MRVcp = sort_by_MRVcp(game, mrv_pos)
                for valid_number in sorted_numbers_by_MRVcp:
                    game.set_cell_value(mrv_pos[0], mrv_pos[1], valid_number)
                    if do_backtrackingMRV(game):
                        return True
                    game.set_cell_empty(mrv_pos[0], mrv_pos[1])
                return False
    return False


def sort_by_MRVcp(game, mrv_pos):
    pos = mrv_pos
    sorted_list_for_MRVcp = sort_by_MrvFwd(game, pos)
    for value in sorted_list_for_MRVcp:
        game.set_cell_value(pos[0], pos[1], value)
        for affected_cell in game.get_cells_affected(pos[0], pos[1]):
            new_array = sort_by_MrvFwd(game, affected_cell)
            if not new_array:
                sorted_list_for_MRVcp.remove(value)
                break
        game.set_cell_empty(pos[0], pos[1])
    return sorted_list_for_MRVcp


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
    max_counter = 10000
    conflict_set = []

    # Fill the board with random numbers
    for i in xrange(game.N):
        for j in xrange(game.N):
            if game.board[i][j] == 0:
                game.board[i][j] = random.randint(1, game.N)

    for counter in xrange(max_counter):
        game.consistency_check = counter + 1
        # Check if the current board is the solution or not. If yes then return TRUE.
        if game.is_valid_sudoku_board():
            return True
        # Find the set of conflicting cells
        for i in xrange(game.N):
            for j in xrange(game.N):
                if game.is_conflicting(i, j):
                    conflict_set.append([i, j])
        # Randomly choose a conflicting cell from the conflicting set
        conflicting_cell = random.choice(conflict_set)
        # Find the number for that cell that minimizes the conflict
        min_conflicting_num = game.find_min_conflicting_num(conflicting_cell[0], conflicting_cell[1])
        # Set that number to the cell
        game.board[conflicting_cell[0]][conflicting_cell[1]] = min_conflicting_num

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

    def is_valid_sudoku_board(self):
        valid_row = set()
        valid_column = set()
        valid_matrix = set()
        # Check duplicity in the rows and columns
        for row in xrange(self.N):
            valid_row.clear()
            valid_column.clear()
            for column in xrange(self.N):
                if self.board[row][column] == 0 or self.board[column][row] == 0:
                    return False
                valid_row.add(self.board[row][column])
                valid_column.add(self.board[column][row])
            if self.N != len(valid_row) or self.N != len(valid_column):
                return False

        # Check duplicity in the smaller matrix
        for i in xrange(self.N / self.M):
            for j in xrange(self.N / self.K):
                row = i * self.M
                column = j * self.K
                valid_matrix.clear()
                for counter in xrange(self.N):
                    if self.board[row + counter / self.K][column + counter % self.K] == 0:
                        return False
                    valid_matrix.add(self.board[row + counter / self.K][column + counter % self.K])
                if self.N != len(valid_matrix):
                    return False

        return True

    def is_conflicting(self, i, j):
        block_start_row = i / self.M * self.M
        block_start_column = j / self.K * self.K
        for counter in xrange(self.N):
            if counter != j:
                if self.board[i][counter] == self.board[i][j]:
                    return True
            if counter != i:
                if self.board[counter][j] == self.board[i][j]:
                    return True
            if (block_start_row + counter / self.K) != i and (block_start_column + counter % self.K) != j:
                if self.board[block_start_row + counter / self.K][block_start_column + counter % self.K] == \
                        self.board[i][j]:
                    return True
        return False

    def find_min_conflicting_num(self, i, j):
        # find the frequency of each number from 1 to N in the relevant row, column and submatrix
        block_start_row = i / self.M * self.M
        block_start_column = j / self.K * self.K
        master_list = []
        master_list.append(self.board[i][j])
        for counter in xrange(self.N):
            if counter != j:
                master_list.append(self.board[i][counter])
            if counter != i:
                master_list.append(self.board[counter][j])
            if (block_start_row + counter / self.K) != i and (block_start_column + counter % self.K) != j:
                master_list.append(
                    self.board[block_start_row + counter / self.K][block_start_column + counter % self.K])
        # Build a dictionary
        dict_list = {x: master_list.count(x) for x in master_list}
        # If there are numbers between 1 to N which are not assigned in any of the relevant row, column or submatrix
        # then return a random value out of those numbers
        if len(dict_list.keys()) != self.N:
            return random.choice(list(set(range(1, self.N + 1)) - set(dict_list.keys())))
        else:
            # Return the number with the least frequency
            return dict_list.keys()[dict_list.values().index(min(dict_list.values()))]
