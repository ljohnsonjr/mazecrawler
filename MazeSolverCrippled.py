# This code creates a maze off parameters, draws, and solves it.


from graphics import *
import random
import sys

M = 40
N = 20
CELL_SIZE = 30
MARGIN = 10
screen_x = M*CELL_SIZE + 2*MARGIN
screen_y = N*CELL_SIZE + 2*MARGIN

class Cell:
    def __init__(self):
        self.l = self.t = self.r = self.b = True
        self.visited = False

    def Draw(self, win, i,j):
        x1 = MARGIN + i*CELL_SIZE
        y1 = MARGIN + j*CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        if self.l:
            line = Line( Point(x1,y1), Point(x1,y2) )
            line.draw(win)
        if self.t:
            line = Line( Point(x1,y1), Point(x2,y1) )
            line.draw(win)
        if self.r:
            line = Line( Point(x2,y1), Point(x2,y2) )
            line.draw(win)
        if self.b:
            line = Line( Point(x1,y2), Point(x2,y2) )
            line.draw(win)
class Maze:
    
    def __init__(self):
        self.cells = []
        for i in range(M):
            cellColumn = []
            for j in range(N):
                cellColumn.append(Cell())
            self.cells.append(cellColumn)
        self.VisitR(0,0)
        self.cells[0][0].t = False
        self.cells[M-1][N-1].b = False
        
    def VisitR(self, i,j):
        self.cells[i][j].visited = True
        while True:
            nexti = []
            nextj = []
            # determine which cells we could move to next
            if i>0 and not self.cells[i-1][j].visited: # left
                nexti.append(i-1)
                nextj.append(j)
            if i<M-1 and not self.cells[i+1][j].visited: # right
                nexti.append(i+1)
                nextj.append(j)
            if j>0 and not self.cells[i][j-1].visited: # up
                nexti.append(i)
                nextj.append(j-1)
            if j<N-1 and not self.cells[i][j+1].visited: # down
                nexti.append(i)
                nextj.append(j+1)

            if len(nexti) == 0:
                return # nowhere to go from here

            # randomly choose 1 direction to go
            index = random.randrange(len(nexti))
            ni = nexti[index]
            nj = nextj[index]

            # knock out walls between this cell and the next cell
            # Time to become a software engineer
            if ni == i+1: # right move
                self.cells[i][j].r = self.cells[i+1][j].l = False
            if ni == i-1: # left move
                self.cells[i][j].l = self.cells[i-1][j].r = False
            if nj == j+1: # down move
                self.cells[i][j].b = self.cells[i][j+1].t = False
            if nj == j-1: # up move
                self.cells[i][j].t = self.cells[i][j-1].b = False

            # recursively visit the next cell
            self.VisitR(ni,nj)
        
    def Draw(self, win):
        for i in range(M):
            for j in range(N):
                self.cells[i][j].Draw(win,i,j)
            

    # Write this method.
    # It should return True if this is the end cell, OR if it leads to the end cell.
    # It should return False if this is a loser cell.
    def SolveR( self, i,  j):
            
        # Mark this cell as visited.
        self.cells[i][j].visited = True

        # Get index number of this cell
        index = j*M + i

        # Record the index in the class variable mMoves.
        self.mMoves.append(index)
        # If we are at the end cell, return true.
        if i == M-1 and j == N-1:
            return True
        
        # move left if there is no wall, and it hasn't been visited. Return true if it returns true.
        if not self.cells[i][j].l and not self.cells[i - 1][j].visited:
            if self.SolveR(i-1,j):
                return True

        # move right if there is no wall, and it hasn't been visited. Return true if it returns true.
        if not self.cells[i][j].r and not self.cells[i + 1][j].visited:
            if self.SolveR(i+1,j):
                return True

        # move down if there is no wall, and it hasn't been visited. Return true if it returns true.
        if not self.cells[i][j].b and not self.cells[i][j+1].visited:
            if self.SolveR(i,j+1):
                return True

        # move up if there is no wall, and it hasn't been visited. Return true if it returns true.
        if not self.cells[i][j].t and not self.cells[i][j-1].visited:
            if self.SolveR(i,j-1):
                return True

        # This is a loser cell, so undo the move from self.mMoves, and return false to the previous cell.
        self.mMoves.pop()
        return False

    # Write this method.
    # Use a depth first search.
    def Solve(self):
        # Initialize mMoves array
        self.mMoves = []

        # Initialize all cells to not visited
        #bruh bart writes fast couldn't keep up
        #somehow got it working
        for i in range(M):
            for j in range(N):
                self.cells[i][j].visited = False
        
        # Start searching recursively from 0,0
        self.SolveR(0,0)

        # Write this method.
    def DrawSolution(self, win):
        print (self.mMoves)
                
        # Now draw it graphically! YEET!
        for i in range(len(self.mMoves)-1):
            index1 = self.mMoves[i]
            index2 = self.mMoves[i+1]
            si = index1 % M     #si = start index ei = end index
            sj = index1 // M
            ei = index2 % M
            ej = index2 // M
            x1 = MARGIN + CELL_SIZE//2 + si*CELL_SIZE
            y1 = MARGIN + CELL_SIZE//2 + sj*CELL_SIZE
            x2 = MARGIN + CELL_SIZE//2 + ei*CELL_SIZE
            y2 = MARGIN + CELL_SIZE//2 + ej*CELL_SIZE
            line = Line( Point(x1,y1), Point(x2,y2))
            line.setOutline("red")
            line.draw(win)
            
               


def main():
    sys.setrecursionlimit(10000)
    win = GraphWin("Maze Solver", screen_x, screen_y)

    theMaze = Maze()
    theMaze.Draw(win)
    theMaze.Solve()
    theMaze.DrawSolution(win)
    
    mouseClick = win.getMouse()                   # get mouse click
    win.close()

main()

    
