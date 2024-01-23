import pygame
import os

class Piece:
    img_index = -1
    rect = (118, 118, 515, 515)
    startX = rect[0]
    startY = rect[1]
    width = round((rect[2] - startX) / 8) + 10
    height = round((rect[3] - startY) / 8) + 10

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.rook = False
        self.king = False
        self.pawn = False
        self.img  = None
        self.move_list = [[], []]

    def update_valid_moves(self, board):
        self.move_list = self.valid_moves(board)

    def click(self):
        pass

    def isSelected(self):
        return self.selected

    def draw(self, win):
        if self.img != None:
            img_piece = self.img

            draw_this = pygame.transform.scale(img_piece, (self.width, self.height))

            w = (self.col * self.rect[2] / 8)
            h = (self.row * self.rect[3] / 8)
            x = round(self.startX + w + 2)
            y = round(self.startY + h + 2)

            win.blit(draw_this, (x, y))
            if self.selected:
                pygame.draw.rect(win, (255, 0, 0), (x - 2, y - 2, 64, 64), 2)

            if self.selected:
                movesattack = self.move_list
                for move in movesattack[0]:
                    x1 = 33 + round(self.startX + (move[0] * self.rect[2] / 8))
                    y1 = 33 + round(self.startY + (move[1] * self.rect[3] / 8))
                    pygame.draw.circle(win, (255, 0, 0), (x1, y1), 10)

                for attack in movesattack[1]:
                    pygame.draw.rect(win, (0, 0, 255), (
                    (self.startX + (attack[0] * self.rect[2] / 8)), (self.startY + (attack[1] * self.rect[3] / 8)), 64, 64),
                                 2)

    def change_pos(self, pos):
        self.row = pos[0]
        self.col = pos[1]

    def getPos(self):
        return (self.col, self.row)



class Bishop(Piece):
    img_index = 0

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.img = getPieceImage(color, "bishop")

    def valid_moves(self, board):
        return diagonal(self, board)


class King(Piece):
    img_index = 1

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.king = True
        self.img = getPieceImage(color, "king")

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []
        attack = []

        canCastling = self.can_Castling(board)

        # RIGHT
        if 0 <= j < 7:
            right = j + 1
            if board[i][right] == 0:
                moves.append((right, i))
                if canCastling[0]:
                    moves.append((right + 1, i))

            elif self.color != board[i][right].color:
                attack.append((right, i))

            # RIGTHDOWN diagnal
            if 0 <= i < 7:
                if board[i + 1][right] == 0:
                    moves.append((right, i + 1))
                elif self.color != board[i + 1][right].color:
                    attack.append((right, i + 1))

            # RIGTHUP diagnal
            if 7 >= i > 0:
                if board[i - 1][right] == 0:
                    moves.append((right, i - 1))
                elif self.color != board[i - 1][right].color:
                    attack.append((right, i - 1))

        # LEFT
        if 7 >= j > 0:
            left = j - 1

            if board[i][left] == 0:
                moves.append((left, i))
                if canCastling[0]:
                    moves.append((left - 1, i))

            elif self.color != board[i][left].color:
                attack.append((left, i))

            #LEFTDOWN diagnal
            if 0 <= i < 7:
                if board[i + 1][left] == 0:
                    moves.append((left, i + 1))
                elif self.color != board[i + 1][left].color:
                    attack.append((left, i + 1))

            # LEFTUP diagnal
            if 7 >= i > 0:
                if board[i - 1][left] == 0:
                    moves.append((left, i - 1))
                elif self.color != board[i - 1][left].color:
                    attack.append((left, i - 1))

        # DOWN
        if 0 <= i < 7:
            if board[i + 1][j] == 0:
                moves.append((j, i + 1))

            elif self.color != board[i + 1][j].color:
                attack.append((j, i + 1))

        # UP
        if 7 >= i > 0:
            if board[i - 1][j] == 0:
                moves.append((j, i - 1))

            elif self.color != board[i - 1][j].color:
                attack.append((j, i - 1))

        return [moves, attack]

    def can_Castling(self, board):
        i = self.row
        j = self.col

        left_count = 0
        right_count = 0

        left_col = self.col
        right_col = self.col

        rookR_col = 8
        rookL_col = 0

        castlingR = False
        castlingL = False
        left_yn = False
        right_yn = False

        print(self.color)

        # Left
        while left_col < 8:
            if left_col != j:
                if board[i][left_col] != 0 :
                    if left_count > 1 and board[i][left_col].rook and self.color == board[i][left_col].color:
                        rookL_col = left_col
                        castlingL = True
                        left_yn = True
                    else:
                        left_yn = True

            left_count += 1
            if left_yn:
                break
            else:
                left_col += 1


        # RIGHT
        while right_col > -1:
            if right_col != j:
                if board[i][right_col] != 0:
                    if right_count > 1 and board[i][right_col].rook and self.color == board[i][right_col].color:
                        rookR_col = right_col
                        castlingR = True
                    else:
                        right_yn = True

            right_count += 1
            if right_yn:
                break
            else:
                right_col -= 1


        return (castlingL, castlingR, rookR_col, rookL_col)

class Knight(Piece):
    img_index = 2

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.img = getPieceImage(color, "knight")

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []
        attack = []

        down = i + 2
        up = i - 2
        right = j + 2
        left = j - 2

        if 0 <= down <= 7:

            if j + 1 <= 7:
                if board[down][j + 1] == 0:
                    moves.append((j + 1, down))
                elif self.color != board[down][j + 1].color:
                    attack.append((j + 1, down))

            if j - 1 >= 0:
                if board[down][j - 1] == 0:
                    moves.append((j - 1, down))
                elif self.color != board[down][j - 1].color:
                    attack.append((j - 1, down))

        if 0 <= up <= 7:

            if j + 1 <= 7:
                if board[up][j + 1] == 0:
                    moves.append((j + 1, up))
                elif self.color != board[up][j + 1].color:
                    attack.append((j + 1, up))

            if j - 1 >= 0:
                if board[up][j - 1] == 0:
                    moves.append((j - 1, up))
                elif self.color != board[up][j - 1].color:
                    attack.append((j - 1, up))

        if 0 <= right <= 7:
            if i + 1 <= 7:
                if board[i + 1][right] == 0:
                    moves.append((right, i + 1))
                elif self.color != board[i + 1][right].color:
                    attack.append((right, i + 1))

            if i - 1 >= 0:
                if board[i - 1][right] == 0:
                    moves.append((right, i - 1))
                elif self.color != board[i - 1][right].color:
                    attack.append((right, i - 1))

        if 0 <= left <= 7:
            if i + 1 <= 7:
                if board[i + 1][left] == 0:
                    moves.append((left, i + 1))
                elif self.color != board[i + 1][left].color:
                    attack.append((left, i + 1))

            if i - 1 >= 0:
                if board[i - 1][left] == 0:
                    moves.append((left, i - 1))
                elif self.color != board[i - 1][left].color:
                    attack.append((left, i - 1))

        return [moves, attack]


class Pawn(Piece):
    img_index = 3

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.pawn = True
        self.first = True
        self.queen = False
        self.img = getPieceImage(color, "pawn")

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []
        attack = []

        row = i + 1
        row2 = i + 2
        if self.color == "w":
            row = i - 1
            row2 = i - 2

        if self.first:
            if board[row2][j] == 0 and board[row][j] == 0:
                moves.append((j, row2))

        if 7 >= row >= 0:
            if board[row][j] == 0:
                moves.append((j, row))

            if 7 >= j + 1 > 0:
                if board[row][j + 1] != 0:
                    if self.color != board[row][j + 1].color:
                        attack.append((j + 1, row))
            if 7 >= j - 1 > 0:
                if board[row][j - 1] != 0:
                    if self.color != board[row][j - 1].color:
                        attack.append((j - 1, row))

        return [moves, attack]

    def can_change(self, board):
        canchange = False
        if(self.color == 'w' and self.row == 0):
            canchange = True

        elif(self.color == 'b' and self.row == 7):
            canchange = True

        return canchange


class Queen(Piece):
    img_index = 4

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.img = getPieceImage(color, "queen")

    def valid_moves(self, board):
        data = updownleftright(self, board)
        data2 = diagonal(self, board)
        data[0].extend(data2[0])
        data[1].extend(data2[1])
        return data


class Rook(Piece):
    img_index = 5

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.rook = True
        self.img = getPieceImage(color, "rook")

    def valid_moves(self, board):
        return updownleftright(self, board)


def getPieceImage(color, piece):
    return pygame.image.load(os.path.join("img", color +"_"+ piece +".png"))

def updownleftright(self, board):
    i = self.row
    j = self.col
    down_row = self.row
    up_row = self.row
    left_col = self.col
    right_col = self.col
    down_yn = False
    up_yn = False
    left_yn = False
    right_yn = False
    moves = []
    attack = []

    # DOWN
    while down_row < 8:
        if down_row != i:
            if board[down_row][j] == 0:
                moves.append((j, down_row))
            elif self.color != board[down_row][j].color:
                attack.append((j, down_row))
                down_yn = True
            else:
                down_yn = True

        if not down_yn:
            down_row += 1
        else:
            break

    # UP
    while up_row > -1:
        if up_row != i:
            if board[up_row][j] == 0:
                moves.append((j, up_row))
            elif self.color != board[up_row][j].color:
                attack.append((j, up_row))
                up_yn = True
            else:
                up_yn = True

        if not up_yn:
            up_row -= 1
        else:
            break

    # Left
    while left_col < 8:
        if left_col != j:
            if board[i][left_col] == 0:
                moves.append((left_col, i))
            elif self.color != board[i][left_col].color:
                attack.append((left_col, i))
                left_yn = True
            else:
                left_yn = True

        if not left_yn:
            left_col += 1
        else:
            break

    # RIGHT
    while right_col > -1:
        if right_col != j:
            if board[i][right_col] == 0:
                moves.append((right_col, i))
            elif self.color != board[i][right_col].color:
                attack.append((right_col, i))
                right_yn = True
            else:
                right_yn = True

        if not right_yn:
            right_col -= 1
        else:
            break

    return [moves, attack]


def diagonal(self, board):
    i = self.row
    j = self.col
    downleft_row = self.row
    downright_row = downleft_row
    downleft_col = self.col
    downright_col = downleft_col

    upleft_row = self.row
    upright_row = upleft_row
    upleft_col = self.col
    upright_col = upleft_col

    downright_yn = False
    downleft_yn = False
    upleft_yn = False
    upright_yn = False
    moves = []
    attack = []

    # DOWNRIGHT
    while 8 > downright_row >= 0 and downright_col < 8:
        if downright_row != i and downright_col != j:
            if board[downright_row][downright_col] == 0:
                moves.append((downright_col, downright_row))
            elif self.color != board[downright_row][downright_col].color:
                attack.append((downright_col, downright_row))
                downright_yn = True
            else:
                downright_yn = True

        if not downright_yn:
            downright_row += 1
            downright_col += 1
        else:
            break

    # DOWNLEFT
    while 0 <= downleft_row < 8 and downleft_col >= 0:
        if downleft_row != i and downleft_col != j:
            if board[downleft_row][downleft_col] == 0:
                moves.append((downleft_col, downleft_row))
            elif self.color != board[downleft_row][downleft_col].color:
                attack.append((downright_col, downright_row))
                downleft_yn = True
            else:
                downleft_yn = True

        if not downleft_yn:
            downleft_row += 1
            downleft_col -= 1
        else:
            break

    # UPRIGHT
    while 8 > upright_row >= 0 and upright_col < 8:
        if upright_row != i and upright_col != j:
            if board[upright_row][upright_col] == 0:
                moves.append((upright_col, upright_row))
            elif self.color != board[upright_row][upright_col].color:
                attack.append((upright_col, upright_row))
                upright_yn = True
            else:
                upright_yn = True

        if not upright_yn:
            upright_row -= 1
            upright_col += 1
        else:
            break

    # UPLEFT
    while 0 <= upleft_row < 8 and upleft_col >= 0:
        if upleft_row != i and upleft_col != j:
            if board[upleft_row][upleft_col] == 0:
                moves.append((upleft_col, upleft_row))
            elif self.color != board[upleft_row][upleft_col].color:
                attack.append((upleft_col, upleft_row))
                upleft_yn = True
            else:
                upleft_yn = True

        if not upleft_yn:
            upleft_row -= 1
            upleft_col -= 1
        else:
            break

    return [moves, attack]