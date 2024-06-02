import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        #1. Check if the length of cells is equal to count.
        #2. If True then return the cell.
        #3. else if the count is less than length of cells return None.
        if (len(self.cells) == self.count and len(self.cells) != 0):
            return self.cells
        elif (len(self.cells)>self.count):
            return None
        else:
            return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        #1. Check if the count is equal to 0.
        #2. If True then return the cells.
        #3. else return None.
        if (self.count == 0):
            return self.cells
        else:
            return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        #1. Check if the cell is present in the sentence that is self.cells.
        #2. If cell is present in the self.cells then remove it from the set using remove function and reduce the self.count by 1.
        #3. Else return None.
        if (cell in self.cells):
            self.cells.remove(cell)
            self.count= self.count-1
        print("after marking", cell, "mine", self)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        #1. Check if the cell is present in the sentence that is self.cells.
        #2. If cell is present in the self.cells then remove it from the set using remove function.
        #3. Else return None.
        if (cell in self.cells):
            self.cells.remove(cell)
        print("after marking", cell, "safe", self)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def is_outof_bounds(self, n_cell):
        if (n_cell[0]<0 or n_cell[1]<0 or n_cell[0]>=self.height or n_cell[1]>=self.width):
            return True

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #1. Update moves_made that is add value of cell by using add function.
        #2. Call mark_safe() to mark the visited cell as a safe cell and update the existing sentences.
        #3. make a list of tuples of each coordinates around the cell named as "cells" using the following points
            #3.1. i-1,j-1
            #3.2. i-1,j
            #3.3. i-1,j+1
            #3.4. i,j+1
            #3.5. i,j-1
            #3.6. i+1,j-1
            #3.6. i+1,j
            #3.7. i+1,j+1
        #4. Go through each tuple of the cell to check if each coordinate is less than height and width and also not less than 0.
        #6. Remove the coordinates that do not exist on grid and check for coordinates of known_mines set in the set if found update count-1.
        #7. Convert cells list into a set.
        #8. Substract self.mines and self.safes from cells.
        #9. Initialize a Sentence class object using cells sentence=Sentence(cells,count) and add the sentence to knowledge.
        #10. knowledge_changed=True
        #11. while knowledge_changed==True 
        #12. knowledge_changed = False
        #13. Call the known_mines function on object of sentence. x=sentence.known_mines
        #14. If x!= None then knowledge_changed=True 
            #14.1. for i in range(len(list(x))):
            #14.2. call mark_mine function and send i as parameter.
        #15. call the known_safes function on object of sentence. x=sentence.known_safes
        #16. If x!=None then knowledge_changed=True
            #16.1. for i in range(len(list(x))):
            #16.2. call mark_safe function and send i as parameter.
        #17. start a loop to visit each object in the knowledge.
        #18. check if the sentence.cells is a subset or superset of one another
        #19. if is subset or superset knowledge_changed=True
        #20. remove subset from superset and update knowledge. XXXXXXXXX
        #21. After updating knowledge check for the count is count of subset is == count of superset then update them as 0
        #22. else if count of subset < superset then count of subset=0 and count of superset= count of superset-count of subset.
        #23
        
        self.moves_made.add(cell)
        print(cell, count)
        self.mark_safe(cell)
        neighbour_cells=[]
        i=cell[0]
        j=cell[1]
        if(not self.is_outof_bounds((i-1,j-1))):
            neighbour_cells.append((i-1,j-1))
        if(not self.is_outof_bounds((i-1,j))):
            neighbour_cells.append((i-1,j))
        if(not self.is_outof_bounds((i-1,j+1))):
            neighbour_cells.append((i-1,j+1))
        if(not self.is_outof_bounds((i,j-1))):
            neighbour_cells.append((i,j-1))
        if(not self.is_outof_bounds((i,j+1))):
            neighbour_cells.append((i,j+1))
        if(not self.is_outof_bounds((i+1,j-1))):
            neighbour_cells.append((i+1,j-1))
        if(not self.is_outof_bounds((i+1,j))):
            neighbour_cells.append((i+1,j))
        if(not self.is_outof_bounds((i+1,j+1))):
            neighbour_cells.append((i+1,j+1))

        for n_cell in neighbour_cells:
            if n_cell in self.mines:
                count-=1
        neighbour_cells=set(neighbour_cells)
        print("neighbour_cells for", cell, neighbour_cells)
        
        neighbour_cells=neighbour_cells-self.mines-self.safes
        sentence=Sentence(neighbour_cells,count)
        self.knowledge.append(sentence)

        knowledge_changed=True
        while(knowledge_changed==True):
            knowledge_changed=False
            
            for sentence_s in self.knowledge:
                ret1=sentence_s.known_mines()
                print("RET1 ::::: ", ret1)
                if (ret1!=None and ret1 != set()):
                    for cell in list(ret1):
                        self.mark_mine(cell)
                    knowledge_changed=True
            
            for sentence_s in self.knowledge:
                ret2=sentence_s.known_safes()
                print("RET2 ::::: ", ret2)
                if (ret2!=None and ret2!=set()):
                    for cell in list(ret2):
                        self.mark_safe(cell)
                    knowledge_changed=True
            
            for sentence_s in self.knowledge:
                for sentence_t in self.knowledge:
                    if sentence_s.cells==sentence_t.cells:
                        continue
                    ret_set=sentence_t.cells.issubset(sentence_s.cells)
                    if (ret_set==True):
                        print("SUBSET:::::", ret_set, sentence_t, sentence_s)
                        sentence_new=Sentence(sentence_s.cells-sentence_t.cells,sentence_s.count-sentence_t.count)
                        if (sentence_new not in self.knowledge):
                            print("Adding", sentence_new, "to our list of knowledge")
                            knowledge_changed=True
                            self.knowledge.append(sentence_new)





    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        #1. Check if the set of safes is empty or not.
        #2. If not empty return(self.safes.pop())
        #3. Else we return None.
        if(self.safes):
            unvisited_safes = self.safes - self.moves_made
            print("unvisited_safes", unvisited_safes)
            if(unvisited_safes):
                return(list(unvisited_safes)[0])
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        #1. Make a set of all the coordinates as a list present in the grid:- grid_coordinates
        #2. Substract the moves_made and mines from the grid_coordinates.
        #3. Choose a random number using random function.
        grid_coordinates=set()
        for i in range(self.height):
            for j in range(self.width):
                grid_coordinates.add((i,j))
        grid_coordinates = grid_coordinates - self.moves_made - self.mines
        if(grid_coordinates == set()):
            print("We should have won!", self.mines)
            return None
        choice_made = random.choice(list(grid_coordinates))
        print(choice_made)
        return choice_made
