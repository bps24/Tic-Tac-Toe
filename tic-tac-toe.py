#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7
from tkinter import Tk, Button
from tkinter.font import Font
from copy import deepcopy

class Board(object):
  def __init__(self,other=None):
    self.player, self.opponent, self.empty = 'X', 'O', " "
    self.size = 3
    self.squares = {}
    for x in range(self.size):
      for y in range(self.size):
        self.squares[x,y] = self.empty
    if other:
      self.__dict__ = deepcopy(other.__dict__)
      
  def make_move(self,x,y):
    board = Board(self)
    board.squares[x,y] = board.player
    (board.player,board.opponent) = (board.opponent,board.player)
    return board
  
  def __minimax(self, player):
    if self.won():
      if player:
        return (-1 ,None)
      else:
        return (1 ,None)
    elif self.tied():
      return (0 ,None)
    elif player:
      best = (-2 ,None)
      for x,y in self.squares:
        if self.squares[x,y]==self.empty:
          value = self.make_move(x,y).__minimax(not player)[0]
          if value>best[0]:
            best = (value,(x,y))
      return best
    else:
      best = (2, None)
      for x,y in self.squares:
        if self.squares[x,y]==self.empty:
          value = self.make_move(x,y).__minimax(not player)[0]
          if value<best[0]:
            best = (value,(x,y))
      return best
  
  def best(self):
    return self.__minimax(True)[1]
  
  def tied(self):
    for (x,y) in self.squares:
      if self.squares[x,y]==self.empty:
        return False
    return True
  
  def won(self):
    # horizontal
    for y in range(self.size):
      winning = []
      for x in range(self.size):
        if self.squares[x,y] == self.opponent:
          winning.append((x,y))
      if len(winning) == self.size:
        return winning
    # vertical
    for x in range(self.size):
      winning = []
      for y in range(self.size):
        if self.squares[x,y] == self.opponent:
          winning.append((x,y))
      if len(winning) == self.size:
        return winning
    # diagonal
    winning = []
    for y in range(self.size):
      x = y
      if self.squares[x,y] == self.opponent:
        winning.append((x,y))
    if len(winning) == self.size:
      return winning
    # other diagonal
    winning = []
    for y in range(self.size):
      x = self.size-1-y
      if self.squares[x,y] == self.opponent:
        winning.append((x,y))
    if len(winning) == self.size:
      return winning
    # default
    return None
  
  def __str__(self):
    string = ''
    for y in range(self.size):
      for x in range(self.size):
        string+=self.squares[x,y]
      string+="\n"
    return string
        

class Window(object):

  def __init__(self):
    self.app = Tk()
    self.app.title('Tic-Tac-Toe ')
    self.app.resizable(width=False, height=False)
    self.board = Board()
    self.font = Font(family="Arial", size=50)
    self.font2 = Font(family="Arial", size=30)
    self.createButtons()
    self.update()
    
  def createButtons(self):
    self.buttons = {}
    for x,y in self.board.squares:
      handler = lambda x=x,y=y: self.make_move(x,y)
      button = Button(self.app, command=handler, font=self.font, width=4, height=2)
      button.grid(row=y, column=x)
      self.buttons[x,y] = button
      handler = lambda: self.reset()
      button = Button(self.app, text='Reset Board', command=handler, font=self.font2)
      button.grid(row=self.board.size+1, column=0,  columnspan=self.board.size, sticky="WE")

  def reset(self):
    self.board = Board()
    self.update()
  
  def make_move(self,x,y):
    self.app.config(cursor="watch")
    self.app.update()
    self.board = self.board.make_move(x,y)
    self.update()
    move = self.board.best()
    if move:
      self.board = self.board.make_move(*move)
      self.update()
    self.app.config(cursor="")
            
  def update(self):
    for (x,y) in self.board.squares:
      text = self.board.squares[x,y]
      self.buttons[x,y]['text'] = text
      self.buttons[x,y]['disabledforeground'] = 'black'
      if text==self.board.empty:
        self.buttons[x,y]['state'] = 'normal'
      else:
        self.buttons[x,y]['state'] = 'disabled'
    winning = self.board.won()
    if winning:
      for x,y in winning:
        self.buttons[x,y]['disabledforeground'] = 'red'
      for x,y in self.buttons:
        self.buttons[x,y]['state'] = 'disabled'
    for (x,y) in self.board.squares:
      self.buttons[x,y].update()


if __name__ == '__main__':
  Window().app.mainloop()
