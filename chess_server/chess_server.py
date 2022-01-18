#hacky for now
import sys
sys.path.append("..")
from chess.chess_game.chess import Chess
from flask import Flask
from flask_restful import Resource, Api, reqparse
from random import randint
from datetime import datetime

app = Flask(__name__)
api = Api(app)



class ChessWrapper:
    def __init__(self):
        self.creation_time = datetime.now()
        self.last_activity_time = datetime.now()
        self.game = Chess()

all_games = {}

class GameState(Resource):
    def get(self, game_id):
        if game := all_games.get(int(game_id), False):
            return {
                "game_id" : game_id,
                "to_play" : game.game.to_play
            }

api.add_resource(GameState, '/api/state/<string:game_id>')

class OverallState(Resource):
    def get(self):
            return {"game_count" : len(all_games)}

api.add_resource(OverallState, '/api/state')

class CreateGame(Resource):
    def post(self):
        global all_games
        while (new_id := randint(1111111,9999999)) in all_games:
            pass
        all_games[new_id] = ChessWrapper()
        return {"game_id" : new_id}
api.add_resource(CreateGame, '/api/new')

move_parser = reqparse.RequestParser()
move_parser.add_argument("piece", type=str)
move_parser.add_argument("pos", type=str)

class Move(Resource):
    def post(self, game_id):
        game = all_games.get(int(game_id),False)
        if game == False:
            return "Invalid ID"

        args = move_parser.parse_args()
        return self.do_move(game.game, args["piece"], args["pos"])

    def do_move(self, game: Chess, piece, pos):
        board = game.board
        occ = board.occupied(piece)
        if occ is None or occ != game.to_play:
            return {"Status" : "Fail: Invalid Piece"}
        piece = board.get_piece(piece)
        possible_moves = piece.moves(board)
        if pos not in possible_moves:
            return {"Status" : "Fail: Selected move is invalid"}
        
        board.move(piece, pos)
        return {"Status" : "Success"}


api.add_resource(Move, '/api/move/<string:game_id>')


if __name__ == '__main__':
    app.run(debug=True)