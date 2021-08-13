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

    def valid_move(self, board, dst):
        return super().valid_move(board, dst) and board.is_safe(dst)
