from stockfish import Stockfish


stockfish = Stockfish(path='stockfish/stockfish-ubuntu-x86-64')
stockfish.make_moves_from_current_position(['e2e3']) # bot
stockfish.make_moves_from_current_position(['a7a6']) # player
stockfish.make_moves_from_current_position(['e3e4']) # bot
stockfish.make_moves_from_current_position(['h7h5']) # player
stockfish.make_moves_from_current_position(['f1a6']) # bot
# print(stockfish.get_board_visual())
print(stockfish.get_best_move())
print(stockfish.get_board_visual())
