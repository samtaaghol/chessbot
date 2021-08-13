from pieces.piece import Piece


class Rook(Piece):
    def get_vectors(self):
        for x in range(1, 8):
            self.vectors += [(0, x), (x, 0), (0, -x), (-x, 0)]
