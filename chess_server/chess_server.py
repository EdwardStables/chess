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

    def do_move(self, piece: str, pos: str):
        board = self.game.board
        occ = board.occupied(piece)
        if occ is None:
            return {"Status" : "Fail: No piece there"}
        if occ != self.game.to_play:
            return {"Status" : "Fail: Wrong colour piece"}
        piece = board.get_piece(piece)
        possible_moves = piece.moves(board)
        if pos not in possible_moves:
            return {"Status" : "Fail: Selected move is invalid"}
        
        board.move(piece, pos)
        self.game.to_play = not self.game.to_play
        return {"Status" : "Success"}

move_parser = reqparse.RequestParser()
move_parser.add_argument("piece", type=str)
move_parser.add_argument("pos", type=str)

all_games = {}

def generate_game_id():
    while (new_id := randint(1000000,9999999)) in all_games:
        pass
    return new_id

class GameState(Resource):
    def get(self, game_id):
        game_id = int(game_id)
        if game := all_games.get(game_id, False):
            game : ChessWrapper

            print(game.game.get_white_pieces())

            return {
                "game_id" : game_id,
                "to_play" : game.game.to_play,
                "white_pieces" : game.game.get_white_pieces(),
                "black_pieces" : game.game.get_black_pieces(),
            }
        else:
            return "Invalid ID", 404

class OverallState(Resource):
    def get(self):
            return {"game_count" : len(all_games)}

class CreateGame(Resource):
    def post(self):
        global all_games
        new_id = generate_game_id()
        all_games[new_id] = ChessWrapper()
        return {"game_id" : new_id}

class Move(Resource):
    def post(self, game_id):
        game = all_games.get(int(game_id),False)
        if game == False:
            return "Invalid ID", 404

        args = move_parser.parse_args()
        return game.do_move(args["piece"], args["pos"])


api.add_resource(CreateGame, '/api/new')
api.add_resource(GameState, '/api/state/<string:game_id>')
api.add_resource(OverallState, '/api/state')
api.add_resource(Move, '/api/move/<string:game_id>')

def get_app():
    return app

if __name__ == '__main__':
    app.run(debug=True)