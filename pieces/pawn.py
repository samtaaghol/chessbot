from pieces.piece import Piece


class Pawn(Piece):
    def get_vectors(self):
        self.vectors = [(0, self.color), (0, 2 * self.color)]

    def valid_move(self, board, a, b):
        return super().valid_move(board, a, b) and self.is_enemy(board, a, b)

    def get_moves(self, board):
        attack_moves = [
            (self.x + 1, self.y + self.color),
            (self.x + 1, self.y + self.color),
        ]
        return super().get_moves(board) + filter(self.valid_move, attack_moves)
