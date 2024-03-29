n = 4
board = []
for _ in range(n):
    row = []
    for _ in range(n):
        row.append([])
    board.append(row)
print(board)
board[0][0] = 2
print(board)
