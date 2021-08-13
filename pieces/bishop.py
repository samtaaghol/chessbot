from pieces.piece import Piece


class Bishop(Piece):
    def get_vectors(self):
        for x in range(1, 8):
            self.vectors += [(x, x), (x, -x), (-x, x), (-x, -x)]
