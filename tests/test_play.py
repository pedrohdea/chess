from stockfish import Stockfish

from loguru import logger

stockfish = Stockfish(path='stockfish/stockfish-ubuntu-x86-64')
logger.debug(stockfish.get_board_visual())
stockfish.make_moves_from_current_position(['e2e3']) # bot
stockfish.make_moves_from_current_position(['a7a6']) # player
stockfish.make_moves_from_current_position(['e3e4']) # bot
stockfish.make_moves_from_current_position(['h7h5']) # player
stockfish.make_moves_from_current_position(['f1a6']) # bot
# logger.debug(stockfish.get_board_visual())
logger.debug(stockfish.get_best_move())
logger.debug(stockfish.get_board_visual())
