import pygame
import os


b_bishop    = pygame.image.load(os.path.join("img", "b_bishop.png"))
b_king      = pygame.image.load(os.path.join("img", "b_king.png"))
b_knight    = pygame.image.load(os.path.join("img", "b_knight.png"))
b_pawn      = pygame.image.load(os.path.join("img", "b_pawn.png"))
b_queen     = pygame.image.load(os.path.join("img", "b_queen.png"))
b_rook      = pygame.image.load(os.path.join("img", "b_rook.png"))

w_bishop    = pygame.image.load(os.path.join("img", "w_bishop.png"))
w_king      = pygame.image.load(os.path.join("img", "w_king.png"))
w_knight    = pygame.image.load(os.path.join("img", "w_knight.png"))
w_pawn      = pygame.image.load(os.path.join("img", "w_pawn.png"))
w_queen     = pygame.image.load(os.path.join("img", "w_queen.png"))
w_rook      = pygame.image.load(os.path.join("img", "w_rook.png"))

b_pieces = [b_bishop, b_king, b_knight, b_pawn, b_queen, b_rook]
w_pieces = [w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook]

#B_pieces = []
#W_pieces = []

#for img in b_pieces:
#    B_pieces.append(pygame.transform.scale2x(img))

#for img in w_pieces:
#    W_pieces.append(pygame.transform.scale2x(img))
class Piece:
    rect = (118, 118, 515, 515)
    startX = rect[0]
    startY = rect[1]
    width = round( (rect[2] - startX) / 8 ) + 10
    height = round( (rect[3] - startY) / 8 ) + 10

    def __init__(self, row, col, img):
        self.row = row
        self.col = col
        self.img = img
        self.selected = False

    def move(self):
        pass

    def click(self):
        pass

    def isSelected(self):
        return self.selected

    def draw(self, win):
        drawThis = pygame.transform.scale(self.img, (self.width, self.height) )

        x = round( self.startX + (self.col * self.rect[2]/8) )
        y = round( self.startY + (self.row * self.rect[3]/8) )

        win.blit(drawThis, (x, y))

class Bishop:
    img = pygame.image.load(os.path.join("img", "b_bishop.png"))
    piece = Piece

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

        if (self.color == "w"):
            self.img = pygame.image.load(os.path.join("img", "w_bishop.png"))

        self.piece(self.row, self.col, self.img)

    def draw(self, board):
        print(board)
        self.piece.draw(self, board)

class King(Piece):
    imgindex = 1

class Knight(Piece):
    imgindex = 2

class Pawn(Piece):
    imgindex = 3

class Queen(Piece):
    imgindex = 4

class Rook(Piece):
    imgindex = 5
