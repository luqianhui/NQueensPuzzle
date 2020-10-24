# n_queens_puzzle.py
import n_queens_puzzle_gui

QUEEN = 1          # The tile which has a queen
EMPTY_SPOT = 0     # The tile in which Queen can be placed 
CONFLICT_SPOT = 2  # The tile in which Queen can not be placed due to the confliction with other queens
BOARD_SIZE = 0     # Initially the board size is 0

class NQueensPuzzle:
    """
    This class represents the N-Queens problem.
    There is no UI, but its methods and attributes can be used by a GUI.
    """

    def __init__(self, n):
        """
        Instantiate the class N-Queens.
        """
        self._size = n
        self.reset_board()

    def get_size(self):
        """
        Get size of board (square so only one value)
        """
        return self._size

    def reset_new_size(self, value):
        """
        Resets the board with new dimensions (square so only one value).
        """
        self._size = value
        self.reset_board()

    def get_board(self):
        """
        Get game board.
        """
        return self._board

    def reset_board(self):
        """
        Restores board to empty, with current dimensions.
        """
        self._board = [[EMPTY_SPOT] * self._size for _ in range(self._size)]
        self._queen_list =[]                     # during the user play the game, note down the queens' positions on the board 
        self._count_solution = 0                 # count the number of the solutions for size N
        self._solution = [-1] * self.get_size()  # note the solution- the positions of queens, for example, _solution[1]=2: on the second row the third column there is a queen

    def is_winning_position(self):
        """
        Winning position:
        If the solution exists (n ==1 or n >=4), checks whether all queens are placed by counting them. There should be as many as the board size.
        If board size = 2 or 3, all the tiles should be red or queen, should not be empty

        Return status:
        1 -- the user wins
        2 -- there is still available tiles on the board, the user can continue
        0 -- no tiles available but the number of the queens less than the board size N, the user lost
        """

        num_queens = sum(row.count(QUEEN) for row in self._board)
        num_empty = sum(row.count(EMPTY_SPOT) for row in self._board)
        if ( self.get_size()== 2 or self.get_size()== 3) and num_empty == 0: 
            # for board size 2 or 3, there is no solution, when there is no empty tiles except red tiles and queen tiles it wins
            return 1
        elif num_queens == self._size: 
            return 1
        elif num_empty == 0:
            return 0
        else:
            return 2

    def is_queen(self, pos):
        """
        Check whether the given position contains a queen.
        """
        i, j = pos
        return self._board[i][j] == QUEEN

    def place_queen(self, pos):
        """
        Add a queen (represented by 1) at a given (row, col).
        """
        if self.is_legal_move(pos):
            self._board[pos[0]][pos[1]] = QUEEN
            self._queen_list.append([pos[0],pos[1]])
            self.mark_tiles(pos,CONFLICT_SPOT)

            return True  # Return value is useful for GUI 
        return False

    def mark_tiles(self,pos,status):
        """
        Mark the tiles with the corresponding status: Queen tile, Conflict tile, Available/empty tile
        """
        for i in range(self.get_size()):
            if i != pos[0]:
                self._board[i][pos[1]] = status
        for j in range(self.get_size()):
            if j != pos[1]:
                self._board[pos[0]][j] = status
        self.mark_diagonals(pos, status)


    def go_back_one_step(self):
        """
        To delete the previous queen on the board and reset the status of the related tiles on the same row, or the same column, or the diagonals
        """
        if self._queen_list:

            x,y = self._queen_list.pop()      # remove the queen in the list

            self._board[x][y] = EMPTY_SPOT    # reset the status of the tile of the queen 
            
            self.mark_tiles([x,y],EMPTY_SPOT) # reset the status of tiles which this queen can impact as empty spot

            for pos in self._queen_list:
                self.mark_tiles(pos,CONFLICT_SPOT) # reset the status of tiles which other queens can impact as conflict spot
            return True    
        else:
            return False

    def is_legal_move(self, pos):
        """
        Check if position is on board and there are no clashes with existing queens
        """
        return  self._board[pos[0]][pos[1]] == EMPTY_SPOT
    
    def find_a_solution_for_n(self):
        """
        Find a solution for N Queen problem for N <= 12
        """
        if self.get_size() > 12:
            return False
        
        self._count_solution = 0
        self.solve_n_queen(0, self.get_size())
        
        if self._count_solution == 0:
            return False
        else:
            return True
        
    def solve_n_queen(self,k, n):
        """
        Find a solution for N Queen problem using back tracking
        """
        if k == n:
            self._count_solution += 1
            if self._count_solution == 1:
                # Find a solution, return the result
                for i in range(n):  
                    for j in range(n):
                        self._board[i][j]= QUEEN if self._solution[i] == j else EMPTY_SPOT
                

        else:
            for j in range(n): 
                if self.place(k, j, self._solution): # try to place queen in one pssible place of the row
                    self._solution[k] = j
                    self.solve_n_queen(k+1, n)       # call the function to place next queen next row

    def place(self, k, j, q): 
        """
        Check whether the queen can put on the tile 
        """

        for i in range(k):
            if q[i] == j or abs(q[i]-j) == abs(i-k):  # either in the same row, or the same column, or diagonals
                return False
        return True
    
    def mark_diagonals(self, pos, status):
        """
        Marl all 4 diagonals with the status conflict or empty
        """
        num_rows, num_cols = len(self._board), len(self._board[0])
        row_num, col_num = pos

        if status == 2:
            status = CONFLICT_SPOT
        elif status == 0:
            status = EMPTY_SPOT
            
        # Lower-right diagonal from (row_num, col_num)
        i, j = row_num + 1, col_num + 1  # This covers case where spot is already occupied.
        while i < num_rows and j < num_cols:
            self._board[i][j] = status
            i, j = i + 1, j + 1

        # Upper-left diagonal from (row_num, col_num)
        i, j = row_num - 1, col_num - 1
        while i >= 0 and j >= 0:
            self._board[i][j] = status
            i, j = i - 1, j - 1

        # Upper-right diagonal from (row_num, col_num)
        i, j = row_num - 1, col_num + 1
        while i >= 0 and j < num_cols:
            self._board[i][j] = status
            i, j = i - 1, j + 1

        # Lower-left diagonal from (row_num, col_num)
        i, j = row_num + 1, col_num - 1
        while i < num_cols and j >= 0:
            self._board[i][j] = status
            i, j = i + 1, j - 1

    

    def __str__(self):
        """
        String representation of board.
        """
        res = ""
        for row in self._board:
            res += str(row) + "\n"
        return res


n_queens_puzzle_gui.run_gui(NQueensPuzzle(BOARD_SIZE))
