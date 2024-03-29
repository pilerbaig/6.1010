import lab

game = lab.new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
lab.set_value(game, [1, 2, 1], 7)
lab.dump(game)
# board:
#     [[3, '.'], [3, 3], [1, 1], [0, 0]]
#     [['.', 3], [3, '.'], [1, 7], [0, 0]]
# dimensions: (2, 4, 2)
# hidden:
#     [[True, True], [True, True], [True, True], [True, True]]
#     [[True, True], [True, True], [True, True], [True, True]]
# state: ongoing
