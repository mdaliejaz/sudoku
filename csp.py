###########################################
# you need to implement five funcitons here
###########################################
import random


# Backtracking function
def do_backtracking(game):
    # check if board is complete and valid
    if game.is_complete_board():
        if game.is_valid_sudoku_board():
            return True
        else:
            return False
    # increment consistency check
    game.consistency_check += 1
    for i in xrange(game.N):
        for j in xrange(game.N):
            if game.board[i][j] == 0:
                # get all possible values for the current cell
                # and iterate on them
                for valid_number in game.possible_valid_numbers(i, j):
                    # set cell value
                    game.set_cell_value(i, j, valid_number)
                    if do_backtracking(game):
                        return True
                    # unset cell value as this value did not result in a valid board
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
    # Read the board
    game.read_input_board(filename)
    # call backtracking function and return the solved board
    if do_backtracking(game):
        return game.result()
    return "Error: No Solution", 0


# Backtracking function with MRV and LCV
def do_backtrackingMRV(game):
    # check if board is complete and valid
    if game.is_complete_board():
        if game.is_valid_sudoku_board():
            return True
        else:
            return False
    # increment consistency check
    game.consistency_check += 1
    for i in xrange(game.N):
        for j in xrange(game.N):
            if game.board[i][j] == 0:
                # get the MRV cell
                mrv_pos = get_mrv_cell(game)
                # sort the possible values with LCV for the MRV cell
                sorted_numbers_by_lcv = sort_by_lcv(game, mrv_pos)
                # iterate over all the sorted by LCV values
                for valid_number in sorted_numbers_by_lcv:
                    # set cell value
                    game.set_cell_value(mrv_pos[0], mrv_pos[1], valid_number)
                    if do_backtrackingMRV(game):
                        return True
                    # unset cell value as this value did not result in a valid board
                    game.set_cell_empty(mrv_pos[0], mrv_pos[1])
                return False


# Function to get the MRV cell
def get_mrv_cell(game):
    total_possible = game.N
    min_mrv_value = total_possible
    mrv_pos = None
    for i in xrange(total_possible - 1, -1, -1):
        for j in xrange(total_possible - 1, -1, -1):
            if game.board[i][j] == 0:
                # find possible values for the current cell
                cur_mrv_value = len(game.possible_valid_numbers(i, j))
                # if current cell is better candidate for being MRV cell, set current cell as MRV position
                if cur_mrv_value <= min_mrv_value:
                    min_mrv_value = cur_mrv_value
                    mrv_pos = (i, j)
    return mrv_pos


# Function to sort with LCV heuristic
def sort_by_lcv(game, mrv_pos):
    # get all possible valid numbers for the current cell
    all_possible_numbers = game.possible_valid_numbers(mrv_pos[0], mrv_pos[1])
    # sort the values in decreasing order based on the length of possible values
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
    # Read the board
    game.read_input_board(filename)
    # call backtrackingMRV function and return the solved board
    if do_backtrackingMRV(game):
        return game.result()
    return "Error: No Solution", 0


# Backtracking function with MRV and Forward checking
def do_backtrackingMRVfwd(game):
    # check if board is complete and valid
    if game.is_complete_board():
        if game.is_valid_sudoku_board():
            return True
        else:
            return False
    # increment consistency check
    game.consistency_check += 1
    for i in xrange(game.N):
        for j in xrange(game.N):
            if game.board[i][j] == 0:
                # get the MRV cell
                mrv_pos = get_mrv_cell(game)
                # sort the possible values with MRV and LCV along with forward constraint.
                # forward constraint check removes values from the current cell's domain
                # if that value results in any of it's neighbor getting a zero size domain
                sorted_numbers_by_MrvFwd = sort_by_MrvFwd(game, mrv_pos)
                for valid_number in sorted_numbers_by_MrvFwd:
                    # set cell value
                    game.set_cell_value(mrv_pos[0], mrv_pos[1], valid_number)
                    if do_backtrackingMRV(game):
                        return True
                    # unset cell value as this value did not result in a valid board
                    game.set_cell_empty(mrv_pos[0], mrv_pos[1])
                return False


# Sort all possible values with MRV+LCV along with Forward checking
def sort_by_MrvFwd(game, mrv_pos):
    # unset count of values to be removed from list lest it contains stale data from previous runs
    game.values_to_be_removed_for_MrvFwd = set()
    # sort the values with MRV+LCV
    sorted_list_for_MrvFwd = sort_by_lcv(game, mrv_pos)
    # iterate over the values to be removed and remove them from the current cell's domain
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
    # read the board
    game.read_input_board(filename)
    # call backtrackingMRVFwd function and return the solved board
    if do_backtrackingMRVfwd(game):
        return game.result()
    return "Error: No Solution", 0


def do_backtrackingMRVcp(game):
    # check if board is complete and valid
    if game.is_complete_board():
        if game.is_valid_sudoku_board():
            return True
        else:
            return False
    # increment consistency check
    game.consistency_check += 1
    for i in xrange(game.N):
        for j in xrange(game.N):
            if game.board[i][j] == 0:
                # get the MRV cell
                mrv_pos = get_mrv_cell(game)
                # sort the values based on MRV+LCV along with doing constraint propagation
                sorted_numbers_by_MRVcp = sort_by_MRVcp(game, mrv_pos)
                for valid_number in sorted_numbers_by_MRVcp:
                    # set cell value
                    game.set_cell_value(mrv_pos[0], mrv_pos[1], valid_number)
                    if do_backtrackingMRV(game):
                        return True
                    # unset cell value as this value did not result in a valid board
                    game.set_cell_empty(mrv_pos[0], mrv_pos[1])
                return False
    return False


# sort all possible values for current cell using MRV+LCV along with constraint propagation
def sort_by_MRVcp(game, mrv_pos):
    pos = mrv_pos
    # Do domain check of current cell by looking at all of it's neighboring/children cells
    sorted_list_for_MRVcp = sort_by_MrvFwd(game, pos)
    # iterate over the valid values of current cell
    # valid values at this point = values that won't make the neighboring cells zero if set
    for value in sorted_list_for_MRVcp:
        # set cell value
        game.set_cell_value(pos[0], pos[1], value)
        # iterate over all neighbors/children of current cell
        for affected_cell in game.get_cells_affected(pos[0], pos[1]):
            # Do domain check of current child's cell by looking at all of it's
            # neighboring/children cells (grand children of main cell)
            new_array = sort_by_MrvFwd(game, affected_cell)
            if not new_array:
                # if domain length of any of the grand children is of size zero, remove the value from parent
                sorted_list_for_MRVcp.remove(value)
                break
        # unset the cell value as the cell value and check with a different one
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
    # read the board
    game.read_input_board(filename)
    # call backtrackingMRV with constraint propagation function and return the solved board
    if do_backtrackingMRVcp(game):
        return game.result()
    return "Error: No Solution", 0


# min confict function
def do_minConflict(game):
    max_counter = 10000
    conflict_set = []

    # Fill the board with random numbers. Fill only in cells which don't have any value
    for i in xrange(game.N):
        for j in xrange(game.N):
            if game.board[i][j] == 0:
                game.board[i][j] = random.randint(1, game.N)

    for counter in xrange(max_counter):
        # increment consistency check
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
    # read the board
    game.read_input_board(filename)
    # call min conflict function and return the solved board
    if do_minConflict(game):
        return game.result()
    return "Error: No Solution", 0


# object to represent board state
class sudoku():
    def __init__(self):
        self.board = None
        self.consistency_check = 0
        self.N = 0
        self.M = 0
        self.K = 0
        self.values_to_be_removed_for_MrvFwd = set()

    def read_input_board(self, filename):
        self.board = []
        f = open(filename, 'r')
        # read the line following by stripping the ; and splitting on ,
        board_details = f.readline().strip().rstrip(';').split(',')
        # Read board details from the first line
        self.N = int(board_details[0])
        self.M = int(board_details[1])
        self.K = int(board_details[2])
        # read consecutive lines and generate the initial game board
        for i in xrange(self.N):
            line = f.readline()
            row = line.strip().rstrip(';').split(',')
            # iterate over the read row and assign 0 if empty
            for i in xrange(self.N):
                if row[i] == '-':
                    row[i] = 0
                else:
                    row[i] = int(row[i])
            self.board.append(row)
        f.close()

    # check if the board is full
    def is_complete_board(self):
        for i in xrange(self.N):
            for j in xrange(self.N):
                if self.board[i][j] == 0:
                    return False
        return True

    def possible_valid_numbers(self, i, j):
        invalid_numbers = set()
        valid_numbers = set()
        # find start row of smaller grid
        block_start_row = i / self.M * self.M
        # find start column of smaller grid
        block_start_column = j / self.K * self.K
        # collect all the numbers that should not be allowed in the current cell
        for counter in xrange(self.N):
            invalid_numbers.add(self.board[i][counter])
            invalid_numbers.add(self.board[counter][j])
            invalid_numbers.add(self.board[block_start_row + counter / self.K][block_start_column + counter % self.K])
        # collect all the numbers that could be added to the current cell
        for numbers in xrange(1, self.N + 1):
            if numbers not in invalid_numbers:
                valid_numbers.add(numbers)
        return valid_numbers

    # set the current cell with given value
    def set_cell_value(self, i, j, number):
        self.board[i][j] = number

    # remove the value from the given cell
    def set_cell_empty(self, i, j):
        self.board[i][j] = 0

    # format output for each heuristic
    def result(self):
        return self.board, self.consistency_check

    # find all the neighbors/children of the current cell
    def get_cells_affected(self, i, j):
        cells_affected = set()
        block_start_row = i / self.M * self.M
        block_start_column = j / self.K * self.K
        for counter in xrange(self.N):
            # neighbors in row
            if self.board[i][counter] == 0:
                cells_affected.add((i, counter))
            # neighbors in column
            if self.board[counter][j] == 0:
                cells_affected.add((counter, j))
            # neighbors in current small grid
            if self.board[block_start_row + counter / self.K][block_start_column + counter % self.K] == 0:
                cells_affected.add((block_start_row + counter / self.K, block_start_column + counter % self.K))
        # discard self from the neighbors
        cells_affected.discard((i, j))
        return cells_affected

    # find number of constraints for the current cell's value on all its neighbors
    def total_constraints(self, i, j, affecting_value):
        total_possible_numbers = 0
        cells_affected = self.get_cells_affected(i, j)
        self.set_cell_value(i, j, affecting_value)
        for affected_cell in cells_affected:
            current_length = len(self.possible_valid_numbers(affected_cell[0], affected_cell[1]))
            # record values that might have to be removed for Forward checking heuristic
            if current_length == 0:
                self.values_to_be_removed_for_MrvFwd.add(affecting_value)
            total_possible_numbers += current_length
        self.set_cell_empty(i, j)
        return total_possible_numbers

    # check if the current board is a valid solution
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

        # Check duplicity in the smaller grid/matrix
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

    # check if the current cell has a conflicting value
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

    # function to find minimum conflicting value
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
        # If there are numbers between 1 to N which are not assigned in any of the relevant row, column or sub matrix
        # then return a random value out of those numbers
        if len(dict_list.keys()) != self.N:
            return random.choice(list(set(range(1, self.N + 1)) - set(dict_list.keys())))
        else:
            # Return the number with the least frequency
            return dict_list.keys()[dict_list.values().index(min(dict_list.values()))]
