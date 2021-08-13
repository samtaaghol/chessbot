from pieces.bishop import Bishop
from pieces.piece import Piece
from pieces.rook import Rook


class Queen(Piece):
    def get_vectors(self):
        self.vectors = Rook(None).vectors + Bishop(None).vectors
