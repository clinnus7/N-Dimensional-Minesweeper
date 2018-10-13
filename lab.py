"""6.009 Lab 4 -- HyperMines"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS


class HyperMinesGame:
    def __init__(self, dims, bombs): #Ex of dimensions [4,3,2]
        """Start a new game.

        This method should properly initialize the "board", "mask",
        "dimensions", and "state" attributes.

        Args:
           dimensions (list): Dimensions of the board
           bombs (list): Bomb locations as a list of lists, each an
                         N-dimensional coordinate

        >>> g = HyperMinesGame([2, 4, 2], [[0, 0, 1], [1, 0, 0], [1, 1, 1]])
        >>> g.dump()
        dimensions: [2, 4, 2]
        board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
               [['.', 3], [3, '.'], [1, 1], [0, 0]]
        mask:  [[False, False], [False, False], [False, False], [False, False]]
               [[False, False], [False, False], [False, False], [False, False]]
        state: ongoing
        """
        self.dimensions = dims
        self.bombs = bombs
        self.state = "ongoing"

        #Creates template mask and board using helper function
        self.board = self.make_array(self.dimensions,0)
        self.mask = self.make_array(self.dimensions,False)
        
        #Fills board with bombs in correct locations
        for bomb in bombs:
            self.set_value(self.board,bomb,'.')

        """
        Goes through every space on the board. If its a '.' it stays. If not it 
        uses get_neighbors to get the positions of all its neighbors that are in
        the board. It checks through the values at those positions and counts the 
        bombs.
        """
        all_coordinates = self.get_allcoords(self.dimensions)
        for coord in all_coordinates:
            if self.get_value(self.board, coord) == '.':
                pass
            else:
                neighboring_bombs = 0
                neighbors = self.get_neighbors(self.dimensions,coord)
                for neighbor in neighbors:
                    if self.get_value(self.board,neighbor) == '.':
                        neighboring_bombs += 1
                self.set_value(self.board,coord,neighboring_bombs)


    def make_array(self, dimensions, value): # FOR [4,3,2]: Makes a list of 4 lists then makes 3 lists in each of those then fills each with 2 values 
        """
        Recursively makes an array of n dimesnions filled with given value. 
        
        >>> game = HyperMinesGame([4,3,2],[])
        >>> game.make_array(game.dimensions,0)
        [[[0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0]]]
        
        """
        if len(dimensions[0:]) == 1: # BASE CASE, fills the bottom with value
            return [value] * dimensions[0]
        else:
            return [self.make_array(dimensions[1:],value) for i in range(dimensions[0])] #4 times, 3 times, 2 times

    def get_value(self, board, coord):
        """
        Recursively gets the value of a specific coordinate in a n dimensional board.
        Until we reach the final value of the coordinate, we keep calling get_value.
        The board becomes board[coord[0]] and the coord is coord[1:] for the next call.
        
        >>> g = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
        ...                  [[False, False], [False, False], [False, False], [False, False]]],
        ...         "state": "ongoing"})
        >>> g.get_value(g.board,[0,0,0])
        3

        """

        if len(coord[0:]) == 1: # BASE CASE, returns value of the last coordnate
            return board[coord[0]]
        else:
            return self.get_value(board[coord[0]],coord[1:]) # Board is cut down each time, since we only want a part of it 

    def set_value(self, board, coord, value):
        """
        Recursively replaces the old value of the board at the coordinate with this new value.
        Works the same way as get_value except we change the value on the board instead of returning.
        
        >>> game = HyperMinesGame([3,3,2],[[1,2,0]])
        >>> game.get_value(game.board,[0,1,1])
        1
        >>> game.set_value(game.board,[0,1,1],3)
        >>> game.get_value(game.board,[0,1,1])
        3
        """


        if len(coord[0:]) == 1:
            board[coord[0]] = value
        else:
            return self.set_value(board[coord[0]],coord[1:],value)

    def get_neighbors(self, dimensions, coord): # dimensions[3,3] coord[1,1]
        """
        Recursively gets the neighbors of a certain coordinate. We approach it 
        by getting the neighbors for each singular dimension. Then putting them
        back together.
        For a 3D board with dim[3,3,3] and coord [1,2,3] it will create
        for each in range(0,3):
            for next_dim in ([1,2],[1,3],[1,4],[2,2],[2,3],[2,4],[3,2],[3,3],[3,4])
                all_neighbors.append([each]+next_dim)
        which will then return all the neighbors. 

        >>> game = HyperMinesGame([10,20,3],[])
        >>> game.get_neighbors(game.dimensions,[5,13,0])
        [[4, 12, 0], [4, 12, 1], [4, 13, 0], [4, 13, 1], [4, 14, 0], [4, 14, 1], [5, 12, 0], [5, 12, 1], [5, 13, 0], [5, 13, 1], [5, 14, 0], [5, 14, 1], [6, 12, 0], [6, 12, 1], [6, 13, 0], [6, 13, 1], [6, 14, 0], [6, 14, 1]]

        """
        if len(coord) == 1: #BASE CASE, returns the neighbors of the last dimension
            last_dim_neigh = []
            for neighbor in range(coord[0]-1, coord[0]+2):
                if self.in_range(neighbor,dimensions[0]):
                    last_dim_neigh.append([neighbor])
            return last_dim_neigh 
        else:
            all_neighbors = []
            for each in range(coord[0]-1, coord[0]+2):
                if self.in_range(each,dimensions[0]):
                    for next_dim in self.get_neighbors(dimensions[1:],coord[1:]): # Sets up for loops for the neighbors of each dimension, adds the neighbors of the current dimension to neighbors of the previous dimension
                        all_neighbors.append([each]+next_dim) 
            return all_neighbors


    def get_allcoords(self, dimensions): #[3,3,3]
        """
        Need to:
        list = []
        for x in range(dimensions[0]):
            for y in range(dimensions[1]):
                for z in range(dimensions[2]):
                    ....
                    list.append([x,y,z])
        
        Recursively gets all the possible coordinates for an n dimensional space.
        Uses the same process as get_neighbors but the range of the for loops 
        are from 0 to the length of the dimension. 

        >>> game = HyperMinesGame([3,3],[])
        >>> game.get_allcoords(game.dimensions)
        [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

        """
        if len(dimensions[0:]) == 1: #BASE CASE, returns the all the possible points in the final dimension as a list of single item lists
            last_dim = []
            for place in range(dimensions[0]):
                last_dim.append([place])
            return last_dim

        else:
            all_coords = []
            for each in range(dimensions[0]):
                for next_dim in self.get_allcoords(dimensions[1:]): # Sets up for loops for the range of each dimension, adds the range of the current dimension to the range of the previous dimension
                    all_coords.append([each]+next_dim)
            return all_coords

    
    def in_range(self,coord,dim):
        """
        Coord: A single coordinate of one dimension
        Dim: The dimension you are checking if the coordinate is in range of

        Returns True if the coordinate is in the range of the dimension and if not
        returns false.

        >>> game = HyperMinesGame([3,3],[])
        >>> game.in_range(4,3)
        False
        """
        if coord < 0 or coord >= dim:
            return False
        return True

    def check_gamestate(self):
        """
        Takes in no parameters and goes through the current values for 
        self.board and self.mask to check if either below condition has been met.
        Victory condition: 0 covered squares that are not mines
        Defeat condition: A revealed bomb
        
        >>> game = HyperMinesGame.from_dict({
        ...         "dimensions": [2, 4],
        ...         "board": [[".", 3, 1, 0],
        ...                   [".", ".", 1, 0]],
        ...         "mask": [[False, True, False, False],
        ...                  [False, False, False, False]],
        ...         "state": "ongoing"})
        >>> game.mask[0][0] = True
        >>> game.check_gamestate()
        >>> game.dump()
        dimensions: [2, 4]
        board: ['.', 3, 1, 0]
               ['.', '.', 1, 0]
        mask:  [True, True, False, False]
               [False, False, False, False]
        state: defeat
        """
        #Gets all the possible coordinates
        all_coordinates = self.get_allcoords(self.dimensions)
        bombs = 0
        covered_squares = 0

        #Goes through all the coordinates and counts all the revealed bombs  
        for coord in all_coordinates:
            if self.get_value(self.board,coord) == '.':
                if self.get_value(self.mask,coord) == True:
                    bombs += 1
            elif self.get_value(self.mask,coord) == False:
                covered_squares += 1
            
        if bombs != 0: # If a bomb is revealed, defeat
            self.state = "defeat"
        elif covered_squares == 0:  #If all squares that should be revealed are, victory
            self.state = "victory"

        

    def dump(self):
        """Print a human-readable representation of this game."""
        lines = ["dimensions: %s" % (self.dimensions, ),
                 "board: %s" % ("\n       ".join(map(str, self.board)), ),
                 "mask:  %s" % ("\n       ".join(map(str, self.mask)), ),
                 "state: %s" % (self.state, )]
        print("\n".join(lines))


    def dig(self, coord):
        """Recursively dig up square at coords and neighboring squares.

        Update the mask to reveal square at coords; then recursively reveal its
        neighbors, as long as coords does not contain and is not adjacent to a
        bomb.  Return a number indicating how many squares were revealed.  No
        action should be taken and 0 returned if the incoming state of the game
        is not "ongoing".

        The updated state is "defeat" when at least one bomb is visible on the
        board after digging, "victory" when all safe squares (squares that do
        not contain a bomb) and no bombs are visible, and "ongoing" otherwise.

        Args:
           coords (list): Where to start digging

        Returns:
           int: number of squares revealed

        >>> g = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
        ...                  [[False, False], [False, False], [False, False], [False, False]]],
        ...         "state": "ongoing"})
        >>> g.dig([0, 3, 0])
        8
        >>> g.dump()
        dimensions: [2, 4, 2]
        board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
               [['.', 3], [3, '.'], [1, 1], [0, 0]]
        mask:  [[False, False], [False, True], [True, True], [True, True]]
               [[False, False], [False, False], [True, True], [True, True]]
        state: ongoing
        >>> g = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
        ...                  [[False, False], [False, False], [False, False], [False, False]]],
        ...         "state": "ongoing"})
        >>> g.dig([0, 0, 1])
        1
        >>> g.dump()
        dimensions: [2, 4, 2]
        board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
               [['.', 3], [3, '.'], [1, 1], [0, 0]]
        mask:  [[False, True], [False, True], [False, False], [False, False]]
               [[False, False], [False, False], [False, False], [False, False]]
        state: defeat
        """
        state = self.state
        if state == "defeat" or state == "victory": #Checks if already won or lost
            state = self.state
            return 0
        else:
            revealed = self.reveal_spaces(coord) # calls helper function on [coord] which reveals tiles and counts the number revealed 
            self.check_gamestate() # Updates the gamestate after a dig
        return revealed # returns the number of tiles revealed after a dig 

    def reveal_spaces(self,coord):
        """
        Recursively reveals spaces on the board and returns the amount revealed.
        Does this recursively by checking neighbors and adding those that are 0 
        to a list that needs this function called on them again.


        >>> game = HyperMinesGame.from_dict({
        ...         "dimensions": [2, 4],
        ...         "board": [[".", 3, 1, 0],
        ...                   [".", ".", 1, 0]],
        ...         "mask": [[False, True, False, False],
        ...                  [False, False, False, False]],
        ...         "state": "ongoing"})
        >>> game.reveal_spaces([0,3])
        4
        """
        to_dig = []

        #If the space is a bomb or numbered space besides 0
        # Will return 1 if its not been dug before, which adds to count
        if self.get_value(self.board,coord) != 0:
            if self.get_value(self.mask,coord) == False:
                self.set_value(self.mask,coord,True)
                return 1 
            else: # If already revealed
                return 0
        
        else:
            neighbors = self.get_neighbors(self.dimensions,coord)
            for neighbor in neighbors: # Goes through each neighbor
                if self.get_value(self.board,neighbor) != '.' and self.get_value(self.mask,neighbor) == False:
                    self.set_value(self.mask,neighbor,True)
                    to_dig.append(neighbor) # Is appended if this value is a 0 that hasn't been dug before, these values will have this function
                                             # called on them again to dig recursively.
        count = len(to_dig)
        for space in to_dig:  # Goes through each space that needs to be recursively dug on
            count = count + self.reveal_spaces(space) # Adds all the times 1 is returned to the count. The count will be all the single squares returned plus all the zeroes kept track in the list. 

        return count 

    def render(self, xray=False):
        """Prepare the game for display.

        Returns an N-dimensional array (nested lists) of "_" (hidden squares),
        "." (bombs), " " (empty squares), or "1", "2", etc. (squares
        neighboring bombs).  The mask indicates which squares should be
        visible.  If xray is True (the default is False), the mask is ignored
        and all cells are shown.

        Args:
           xray (bool): Whether to reveal all tiles or just the ones allowed by
                        the mask

        Returns:
           An n-dimensional array (nested lists)

        >>> g = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...            "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                      [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...            "mask": [[[False, False], [False, True], [True, True], [True, True]],
        ...                     [[False, False], [False, False], [True, True], [True, True]]],
        ...            "state": "ongoing"})
        >>> g.render(False)
        [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
         [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

        >>> g.render(True)
        [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
         [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
        """
        board_copy = list(self.board)
        render_map = self.make_array(self.dimensions,0)
        all_coordinates = self.get_allcoords(self.dimensions)

        if xray == False:
            for coord in all_coordinates:
                if self.get_value(self.mask,coord) == False: # Fills places where mask is False as '_'. 
                    self.set_value(render_map,coord,'_')
                else:
                    if self.get_value(self.board,coord) == ".":
                        self.set_value(render_map,coord,".")
                    if self.get_value(self.board,coord) == 0:  # If mask is true 0s become spaces
                        self.set_value(render_map,coord," ")
                    else:
                        self.set_value(render_map,coord,str(self.get_value(self.board,coord)))# Otherwise the space becomes the string of the amount of neighboring bombs
        
        # Board is as if the mask is true for everything
        else:
            for coord in all_coordinates:
                if self.get_value(self.board,coord) == ".":
                    self.set_value(render_map,coord,".")
                if self.get_value(self.board,coord) == 0:
                    self.set_value(render_map,coord," ")
                else:
                    self.set_value(render_map,coord,str(self.get_value(self.board,coord)))
        return render_map


    @classmethod
    def from_dict(cls, d):
        """Create a new instance of the class with attributes initialized to
        match those in the given dictionary."""
        game = cls.__new__(cls)
        for i in ('dimensions', 'board', 'state', 'mask'):
            setattr(game, i, d[i])
        return game


if __name__ == '__main__':
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)

    

