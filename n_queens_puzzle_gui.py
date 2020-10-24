# n_queens_puzzle_gui.py

try:
    import simplegui

except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

    simplegui.Frame._hide_status = True
    simplegui.Frame._keep_timers = False

queen_image = simplegui.load_image("https://github.com/luqianhui/NQueensPuzzle/blob/main/queen.png?raw=true")
queen_image_size = (queen_image.get_width(), queen_image.get_height())

FRAME_SIZE = (460, 460)
BOARD_SIZE = 20  # Rows/cols
INPUT_SIZE = ''


class NQueensPuzzleGUI:
    """
    GUI for N-Queens game.
    """

    def __init__(self, game):
        """
        Instantiate the GUI for N-Queens game.
        """
        # Game board
        self._game = game
        self._size = game.get_size()
        try:
            self._square_size = FRAME_SIZE[0] // self._size
        except ZeroDivisionError:
            self._square_size = 0

        # Set up frame
        self.setup_frame()

    def setup_frame(self):
        """
        Create GUI frame and add handlers.
        """
        self._frame = simplegui.create_frame("N Queens puzzle",
                                             FRAME_SIZE[0], FRAME_SIZE[1])
        self._frame.set_canvas_background('Teal')

        # Set handlers
        self._frame.set_draw_handler(self.draw)
        self._frame.set_mouseclick_handler(self.click)
        self._frame.add_label("N Queens puzzle")
        self._frame.add_label("")  # For better spacing.
        msg = "Current board size: " + str(self._size)
        self._size_label = self._frame.add_label(msg)  # For better spacing.
        self._frame.add_label("")  # For better spacing.     
        self._frame.add_input('Please input board size N = :', self.input_size_handler, 100)
        self._frame.add_label("")  # For better spacing.
        self._frame.add_button("Go back one step", self.go_back)
        self._frame.add_label("")  # For better spacing.
        self._frame.add_button("Solution Mode", self.find_solution)        
        self._frame.add_label("")  # For better spacing. 
        self._frame.add_button("Reset", self.reset)
        self._frame.add_label("")  # For better spacing. 
        self._label = self._frame.add_label("")
        

    def input_size_handler(self,text):  # type: (str) -> None
        """
        Get the board size from user input
        """
        try:
            size = int(text)
            if size == 0:
                self._label.set_text("N cannot be 0")
            elif size != self._game.get_size():
                self.board_size_is_n(size)
        except ValueError:
            self._label.set_text("Please input an interger number")

    def board_size_is_n(self,n):
        """
        Resets game with new size.
        """
        new_size = n
        self._game.reset_new_size(new_size)
        self._size = self._game.get_size()
        self._square_size = FRAME_SIZE[0] // self._size
        msg = "Current board size: " + str(self._size)
        self._size_label.set_text(msg)
        self.reset()

    def start(self):
        """
        Start the GUI.
        """
        self._frame.start()

    def reset(self):
        """
        Reset the board
        """
        self._game.reset_board()
        self._label.set_text("")
    
    def go_back(self):
        """
        Go back one step before
        """
        
        if self._game.go_back_one_step():
            self._label.set_text("Go back one step before")
        else:
            self._label.set_text("There is no previsous step")

    def find_solution(self):
        """
        Find a solution
        """ 
        if self._game.get_size() > 12:
            self._label.set_text("According to the requirement, the solution is only provided for N <= 12")
        elif self._game.get_size()  == 0:
            self._label.set_text("The current board size is 0. Please input a new board size.")
        elif self._game.find_a_solution_for_n():
            self._label.set_text("One solution is displayed")
        else:
            self._label.set_text("The solution doesn't exist")

    def draw(self, canvas):
        """
        Draw handler for GUI.
        """
        board = self._game.get_board()
        dimension = self._size
        size = self._square_size

        if queen_image.get_height() == 0:
            image_status = False
        else:
            image_status = True

        # Draw the squares
        for i in range(dimension):
            for j in range(dimension):
                empty_color = "white"
                points = [(j * size, i * size), ((j + 1) * size, i * size), ((j + 1) * size, (i + 1) * size),
                          (j * size, (i + 1) * size)]
                line_color = "black"
                conflict_color = "red"          
                canvas.draw_polygon(points, 1, line_color, empty_color)

                if board[i][j] == 1:
                    
                    if image_status:
                        canvas.draw_image(
                            queen_image,  # The image source
                            (queen_image_size[0] // 2, queen_image_size[1] // 2),
                            # Position of the center of the source image
                            queen_image_size,  # width and height of source
                            ((j * size) + size // 2, (i * size) + size // 2),
                            # Where the center of the image should be drawn on the canvas
                            (size, size)  # Size of how the image should be drawn
                        )
                    else:
                        canvas.draw_polygon(points, 1, line_color, "black")
                elif board[i][j] == 2: 
                    canvas.draw_polygon(points, 1, line_color, conflict_color)

    def click(self, pos):
        """
        Toggles queen if legal position. 
        """
        try:
            i, j = self.get_grid_from_coords(pos)
            if self._game.is_queen((i, j)):
                self._label.set_text("")
            else:
                if not self._game.place_queen((i, j)):
                    self._label.set_text("Illegal move!")
                else:
                    self._label.set_text("")

            if self._game.is_winning_position() == 1:
                self._label.set_text("Well done. You have found a solution :-)")
            elif self._game.is_winning_position() == 0:
                self._label.set_text("You have lost. Don't give up. Please try again.")

        except TypeError:
            self._label.set_text("")

    def get_grid_from_coords(self, position):
        """
        Given coordinates on a canvas, gets the indices of
        the grid.
        """
        try:
            pos_x, pos_y = position
            return (pos_y // self._square_size,  # row
                    pos_x // self._square_size)  # col
        except ZeroDivisionError:
            pos_x, pos_y = 0,0


def run_gui(game):
    """
    Instantiate and run the GUI
    """
    gui = NQueensPuzzleGUI(game)
    gui.start()

