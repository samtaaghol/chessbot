from pieces.piece import Piece


class Knight(Piece):
    def get_vectors(self):
        self.vectors = [
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
        ]

    def valid_move(self, board, a, b):
        return self.valid_target(board, a, b)
