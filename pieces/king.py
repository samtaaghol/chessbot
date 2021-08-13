from pieces.piece import Piece


class King(Piece):
    def get_vectors(self):
        self.vectors = [
            (0, 1),
            (0, -1),
            (-1, 0),
            (1, 0),
            (-1, 1),
            (1, 1),
            (-1, -1),
            (1, -1),
        ]

    def valid_move(self, board, a, b):
        return super().valid_move(board, a, b) and board.safe_square(self.color, a, b)
