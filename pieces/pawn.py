from pieces.piece import Piece


class Pawn(Piece):
    def get_vectors(self):
        self.vectors = [(0, self.color), (0, 2 * self.color)]

    def valid_move(self, board, dst):
        return super().valid_move(board, dst) and self.is_enemy(board, dst)

    def get_moves(self, board):
        possible_moves = [
            (self.pos[0] + 1, self.pos[1] + self.color),
            (self.pos[0] + 1, self.pos[1] + self.color),
            (self.pos[0], self.pos[1] + self.color),
        ]
        return [move for move in possible_moves if self.valid_move(board, move)]
