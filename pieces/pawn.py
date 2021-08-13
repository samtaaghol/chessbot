from pieces.piece import Piece


class Pawn(Piece):
    def get_vectors(self):
        self.vectors = [(0, self.color), (0, 2 * self.color)]

    def get_moves(self, board):
        possible = [(self.pos[0], self.pos[1] + self.color)]
        attacking = [
            (self.pos[0] + 1, self.pos[1] + self.color),
            (self.pos[0] + 1, self.pos[1] + self.color),
        ]
        return filter(board.valid_move, possible) + filter(board.is_enemy, attacking)
