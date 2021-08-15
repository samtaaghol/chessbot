from pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)

    def move(self, end):
        self.pos = end
        if (0, -2 * self.color) in self.vectors:
            self.vectors.remove((0, -2 * self.color))

    def get_vectors(self):
        self.vectors = [(0, -self.color), (0, -2 * self.color)]

    def get_moves(self, board):

        moves = [
            move for move in super().get_moves(board) if not board.is_enemy(move[1])
        ]

        return moves + self.get_attacking_moves(board)

    def get_defending_squares(self, board):
        return [
            defense
            for defense in self.get_attacking_moves(board)
            if board.valid_defense(defense)
        ]

    def get_attacking_moves(self, board):
        attk_moves = [
            (self.pos, (self.pos[0] + 1, self.pos[1] - self.color)),
            (self.pos, (self.pos[0] - 1, self.pos[1] - self.color)),
        ]

        return [
            move
            for move in attk_moves
            if board.valid_move(move) and board.is_enemy(move[1])
        ]
