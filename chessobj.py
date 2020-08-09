import numpy

def cta(x, y):
    """
    Chess coordinates to Array coordinates.
    """
    return (x - 1, 8 - y)

def atc(x, y):
    """
    Array coordinates to Chess coordinates.
    """
    return (x + 1, 8  - y)

def cx(x):
    return x-1

def cy(y):
    return 8-y

def in_bounds(x,y):
    return (0 < x < 9) and (0 < y < 9)

def diagonal_path(start, end):
    pass

def translate(coordinates, vector):
    return (coordinates[0] + vector[0], coordinates[1] + vector[1])

class Board:
    def __init__(self):
        self.current_player = "White"
        self.board = numpy.full((8,8), None)
        self.setup_board()
        self.assign_positions()
        self.black_defended = {}
        self.white_defended = {}
        self.defended_squares = {}
        self.update_piece_moves()
        self.king_checked = False

    def setup_board(self):
        self.board[0] = [Rook("Black"),
                         Knight("Black"),
                         Bishop("Black"),
                         Queen("Black"),
                         King("Black"),
                         Bishop("Black"),
                         Knight("Black"),
                         Rook("Black")]
        self.board[7] = [Rook("White"),
                         Knight("White"),
                         Bishop("White"),
                         Queen("White"),
                         King("White"),
                         Bishop("White"),
                         Knight("White"),
                         Rook("White")]
        self.board[1], self.board[6] = [Pawn("Black")] * 8, [Pawn("White")] * 8

    def get_available_moves(self):
        moves = []
        for row in self.board:
            for piece in row:
                if piece != None:
                    for move in piece.moves:
                        if piece.color == self.current_player:
                            moves.append((piece.position, translate(piece.position, move)))
        return moves

    def piece_at(self, x, y):
        return self.board[cy(y)][cx(x)] != None

    def switch_team(self):
        if self.current_player == "White":
            self.current_player = "Black"
        else:
            self.current_player = "White"

    def move(self, start, end):
        # move is in format (piece_coordinates, dest_coordinates)
        sx,sy = start
        ex,ey = end
        vector = (ex-sx, ey-sy)
        piece = self.board[cy(sy)][cx(sx)]
        if piece == None:
            return False
        if piece.color != self.current_player:
            return False
        if vector in piece.get_moves(self.board, self.defended_squares):
            self.board[cy(ey)][cx(ex)], self.board[cy(sy)][cx(sx)] = piece, None
            self.board[cy(ey)][cx(ex)].position = (ex, ey)
            self.board[cy(ey)][cx(ex)].has_moved = True
            self.board[cy(ey)][cx(ex)].attacking = []
            self.board[cy(ey)][cx(ex)].get_attacking(self.board)
            self.update_piece_moves()
            self.switch_team()
            print(self.board)
        else:
            print(self.board[cy(sy)][cx(sx)])


    def assign_positions(self):
        for x in range(0, 8):
            for y in range(0,8):
                if self.board[y][x] != None:
                    #print((x,y), atc(x,y), self.board[y][x].color, self.board[y][x].__class__.__name__)
                    self.board[y][x].position = atc(x, y)

    def update_piece_moves(self):
        self.king_checked = False
        if self.current_player == "White":
            self.defended_squares = self.black_defended
        else:
            self.defended_squares = self.white_defended
        king_pos = ()
        for row in self.board:
            for piece in row:
                if piece != None:
                    piece.get_moves(self.board, self.defended_squares)
                    print(piece.color, piece.__class__.__name__, piece.moves)
                    self.defended_squares.update(piece.attacking)
                    if piece.__class__.__name__ == "King":
                        king_pos = piece.position
        if king_pos in self.defended_squares:
            self.king_checked = True

    def is_square_defended(self, x, y):
        return (x,y) in self.defended_squares

class Piece:
    def __init__(self, color):
        self.has_moved = False
        self.color = color
        self.position = None

        self.vectors = []
        self.moves = []
        self.attacking = []

        self.c = 1
        if self.color == "Black":
            self.c = -self.c
        self.get_vectors()

    def __str__(self):
        return self.__class__.__name__[:4]

    def __repr__(self):
        return self.__class__.__name__[:4]

    def piece_at(self, board,  x, y):
        return board[cy(y)][cx(x)] != None

    def same_colour(self, board,  x, y):
        if self.piece_at(board, x, y):
            return board[cy(y)][cx(x)].color == self.color
        return False
    def path_clear(self, board, vector):
        sx, sy = self.position
        ex, ey = (sx + vector[0], sy + vector[1])
        dx, dy = (ex - sx, ey - sy)
        if not in_bounds(ex, ey) or self.same_colour(board, ex, ey):
            return False
        coords_in_path = []
        if abs(dx) == abs(dy):
            coords_in_path = self.get_diagonal_path((ex, ey))
        if dx == 0:
            for y in range(min([sy, ey]) + 1, max([sy, ey])):
                coords_in_path.append((sx, y))
        if dy == 0:
            for x in range(min([sx, ex])+1, max([sx, ex])):
                coords_in_path.append((x, sy))
        for coord in coords_in_path:
            if board[cy(coord[1])][cx(coord[0])] != None:
                return False
        return True

    def get_diagonal_path(self, end):
        sx, sy = self.position
        ex, ey = end
        coords = []
        xmod, ymod = -1, -1
        if ex > sx:
            xmod = 1
        if ey > sy:
            ymod = 1
        for i in range(1, abs(ex-sx)):
            coords.append((sx+i*xmod, sy+i*ymod))
        return coords

    def get_moves(self, board, attacked_squares):
        self.moves = []
        for move in self.vectors:
            if self.path_clear(board, move):
                self.moves.append((move))
        return self.moves

    def get_attacking(self, board):
        for move in self.moves:
            sx, sy = self.position
            ex, ey = move
            self.attacking.append((sx+ex, sy+ey))

class Pawn(Piece):
    def get_attacking(self, board):
        sx, sy = self.position
        for move in self.moves:
            ex, ey = move
            self.attacking.append((sx + ex, sy + ey))
        self.attacking += (sx + 1, sy + self.c),(sx + 1, sy + self.c)
    def get_vectors(self):
        self.vectors = [(0,self.c), (0,2*self.c)] # TODO: Pawn Attacks (1, 1*self.c), (-1, 1*self.c)
    def move(self, board, vector):
        super().move(board, vector)
        if self.has_moved and (0,2*self.c) in self.vectors:
            self.vectors.remove((0,2*self.c))
    def get_moves(self, board, attacked_squares):
        self.moves = []
        sx, sy = self.position
        for move in self.vectors:
            if self.path_clear(board, move):
                self.moves.append(move)
        if in_bounds(sx + 1, sy + self.c):
            left = board[cy(sy + self.c)][cx(sx + 1)]
            if (left != None) and left.color != self.color:
                self.moves.append((1, self.c))
        if in_bounds(sx - 1, sy + self.c):
            right = board[cy(sy + self.c)][cx(sx - 1)]
            if (right != None) and right.color != self.color:
                self.moves.append((-1, self.c))
        return self.moves

class Rook(Piece):
    def get_vectors(self):
        for x in range(1,8):
            self.vectors.append((0, x))
            self.vectors.append((x, 0))
            self.vectors.append((0,-x))
            self.vectors.append((-x,0))

class Knight(Piece):
    def get_vectors(self):
        self.vectors = [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]
    def path_clear(self, board, vector):
        sx, sy = self.position
        ex, ey = (sx + vector[0], sy + vector[1])
        #print((sx,sy), "+", vector, "=", (ex,ey))
        if not in_bounds(ex, ey) or ((board[cy(ey)][cx(ex)] != None) and (board[cy(ey)][cx(ex)].color == self.color)):
            return False
        return True

class Bishop(Piece):
    def get_vectors(self):
        for x in range(1, 8):
            self.vectors.append((x,  x))
            self.vectors.append((x, -x))
            self.vectors.append((-x, x))
            self.vectors.append((-x,-x))

class Queen(Piece):
    def get_vectors(self):
        self.vectors = Rook(self.color).vectors + Bishop(self.color).vectors

class King(Piece):
    def get_vectors(self):
        self.vectors = [(0,1),(0,-1),(-1,0),(1,0),(-1,1),(1,1),(-1,-1),(1,-1)]
    def get_moves(self, board, attacked_squares):
        self.moves = []
        for move in self.vectors:
            if translate(self.position, move) not in attacked_squares and self.path_clear(board, move):
                self.moves.append((move))
        return self.moves
board = Board()

class chessGui:
