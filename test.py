from board import Board

b = Board()
print(b.get_available_moves())
b.safe_move(((0, 1), (0, 2)))
print(b.board)
