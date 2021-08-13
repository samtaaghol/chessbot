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

    """
    
    """

    def valid_move(self, board, dst):
        return self.valid_target(board, dst) and not board.moves_into_check(
            self.format_move(dst)
        )
