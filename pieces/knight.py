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

    def get_defending_squares(self, board):
        return self.get_moves(board)

    """
    
    """

    def get_moves(self, board):
        moves = []
        for (x, y) in self.vectors:

            # Applies the vector to our current position
            move = (self.pos, (self.pos[0] + x, self.pos[1] + y))

            # If the vector from start_pos to end_pos results in a valid move.
            if (
                board.in_bounds(move[0])
                and board.in_bounds(move[1])
                and self.valid_target(board, move[1])
                # and board.moves_into_check(move)
            ):

                # Add the end_pos to the list of moves considered valid.
                moves.append(move)

        # Formats the move into the (start_pos, end_pos) format.
        return moves
