import piece
import numpy

# import piece2
class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.pawnpromote = False

        self.board = [[0 for x in range(self.cols)] for _ in range(rows)]
        # print(self.board)

        for i in range(8):
            self.board[6][i] = piece.Pawn(6, i, "w")
            self.board[1][i] = piece.Pawn(1, i, "b")

        self.board[0][0] = piece.Rook(0, 0, "b")
        self.board[0][1] = piece.Knight(0, 1, "b")
        self.board[0][2] = piece.Bishop(0, 2, "b")
        self.board[0][3] = piece.Queen(0, 3, "b")
        self.board[0][4] = piece.King(0, 4, "b")
        self.board[0][5] = piece.Bishop(0, 5, "b")
        self.board[0][6] = piece.Knight(0, 6, "b")
        self.board[0][7] = piece.Rook(0, 7, "b")

        self.board[7][0] = piece.Rook(7, 0, "w")
        self.board[7][1] = piece.Knight(7, 1, "w")
        self.board[7][2] = piece.Bishop(7, 2, "w")
        self.board[7][3] = piece.Queen(7, 3, "w")
        self.board[7][4] = piece.King(7, 4, "w")
        self.board[7][5] = piece.Bishop(7, 5, "w")
        self.board[7][6] = piece.Knight(7, 6, "w")
        self.board[7][7] = piece.Rook(7, 7, "w")

        self.turn = "w"
    def update_moves(self):
        for row in self.board:
            for block in row:
                if block != 0:
                    block.update_valid_moves(self.board)

    def draw(self, win):
        for row in self.board:
            for block in row:
                if block != 0:
                    block.draw(win)

        if self.pawnpromote:
            pass

    def select(self, i, j, color):
        changed = False
        prev = (-1, -1)

        for row in self.board:
            for block in row:
                if block != 0:
                    if block.selected:
                        prev = block.getPos()

        # if piece
        if self.board[j][i] == 0 and prev != (-1, -1):
            changed = self.step_move(prev, (i, j), 0, changed)
        else:
            if prev == (-1, -1):
                self.reset_selected()
                if self.board[j][i] != 0:
                    self.board[j][i].selected = True
            else:

                if self.board[prev[1]][prev[0]].color != self.board[j][i].color:
                    changed = self.step_move(prev, (i, j), 1, changed)

                    if self.board[j][i].color == color:
                        self.board[j][i].selected = True

                else:
                    if self.board[j][i].color == color:
                        self.reset_selected()

                        self.board[j][i].selected = True

        return changed


    def step_move(self, start, end, num, changed):
        moves = self.board[start[1]][start[0]].move_list
        if end in moves[num]:
            changed = self.move(start, end)
        self.reset_selected()

        return changed

    def reset_selected(self):
        for row in self.board:
            for block in row:
                if block != 0:
                    block.selected = False

    def get_danger_moves(self, color):
        danger_moves = []
        for row in self.board:
            for block in row:
                if block != 0:
                    if block.color != color:
                        for move in block.move_list:
                            danger_moves.extend(move)

        return danger_moves

    def is_checked(self, color):
        self.update_moves()
        danger_moves = self.get_danger_moves(color)
        king_pos = (-1, -1)
        for row in self.board:
            for block in row:
                if block != 0:
                    if block.king and block.color == color:
                        king_pos = block.getPos()

        if king_pos in danger_moves:
            return True

        return False

    def move(self, start, end):
        #checkedBefore = self.is_checked(color)
        changed = True
        nBoard = self.board[:]

        if nBoard[start[1]][start[0]].pawn:
            if nBoard[start[1]][start[0]].first:
                nBoard[start[1]][start[0]].first = False

            if nBoard[start[1]][start[0]].color == 'w' and end[1] == 0:
                self.pawnpromote = True
                print("promote white pawn")
            elif nBoard[start[1]][start[0]].color == 'b' and end[1] == 7:
                self.pawnpromote = True
                print("promote black pawn")

        nBoard[start[1]][start[0]].change_pos( (end[1], end[0]) )
        nBoard[end[1]][end[0]] = nBoard[start[1]][start[0]]
        nBoard[start[1]][start[0]] = 0

        self.board = nBoard

        self.update_moves()

        return changed

    def promotion(self, end):
        pass