import sys
sys.path.append("..")
import requests
from pytest import fixture
from chess.chess_server.chess_server import *
from time import sleep

BASE_URL = "http://127.0.0.1:5000"
def get(req: str) -> requests.Response:
    return requests.get(BASE_URL + req)
def post(req: str) -> requests.Response:
    return requests.post(BASE_URL + req)

@fixture(scope="session")
def app():
    yield get_app()

from flask import request
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with werkzeug server')
    func()

@fixture(scope="session")
def server(app):
    @app.route('/shutdown',methods=('POST',))
    def shutdown():
        shutdown_server()
        return "Shutting down server"

    from threading import Thread
    server_thread = Thread(target=app.run)
    server_thread.start()
    sleep(0.1) #sleep needed to give the server a chance to start
    yield server_thread
    requests.post(BASE_URL + "/shutdown")

@fixture
def create_game(server):
    return post("/api/new").json()["game_id"]


################################################################################
##### Endpoint status testing
################################################################################

def test_api_state_code_200(server):
    print("running test")
    assert get("/api/state").status_code == 200
    
def test_api_state_game_id_code_200(create_game):
    assert get(f"/api/state/{create_game}").status_code == 200

def test_api_state_invalid_game_id_code_404(server):
    #valid game IDs won't have leading zeros 
    assert get(f"/api/state/0000000").status_code == 404

def test_api_new_code_200(server):
    assert post(f"/api/new").status_code == 200

def test_api_move_code_200(create_game):
    assert post(f"/api/move/{create_game}?piece=a2&pos=a3").status_code == 200

def test_api_move_invalid_game_id_code_404(create_game):
    assert post(f"/api/move/0000000?piece=a2&pos=a3").status_code == 404

################################################################################
##### Server logic testing
################################################################################

def test_new_game_creates_id(server):
    count = get("/api/state").json()["game_count"]
    post("/api/new")
    assert get("/api/state").json()["game_count"] == count + 1

#TODO timeouts (find a neat way to do it)

################################################################################
##### JSON Schema Testing
################################################################################

#TODO

################################################################################
##### Game Logic Testing
################################################################################

#Only minimal testing here as testing for the chess backend handles most
#Just cover basic moving, taking, win/lose

def test_new_game_piece_layout(create_game):
    game_state = get(f"/api/state/{create_game}").json()
    print(game_state)
    assert game_state["game_id"] == create_game
    assert game_state["to_play"] == True
    assert game_state["white_pieces"] == {
        "a1" : "Rook", "b1" : "Knight", "c1" : "Bishop", "d1" : "Queen", 
        "e1" : "King", "f1" : "Bishop", "g1" : "Knight", "h1" : "Rook", 
        "a2" : "Pawn", "b2" : "Pawn", "c2" : "Pawn", "d2" : "Pawn", 
        "e2" : "Pawn", "f2" : "Pawn", "g2" : "Pawn", "h2" : "Pawn"
    }
    assert game_state["black_pieces"] == {
        "a8" : "Rook", "b8" : "Knight", "c8" : "Bishop", "d8" : "Queen", 
        "e8" : "King", "f8" : "Bishop", "g8" : "Knight", "h8" : "Rook", 
        "a7" : "Pawn", "b7" : "Pawn", "c7" : "Pawn", "d7" : "Pawn", 
        "e7" : "Pawn", "f7" : "Pawn", "g7" : "Pawn", "h7" : "Pawn"
    }

def test_game_move(create_game):
    wp = get(f"/api/state/{create_game}").json()["white_pieces"]
    assert wp.get("a2",False) == "Pawn"
    assert wp.get("a3",False) == False
    post(f"/api/move/{create_game}?piece=a2&pos=a3")
    wp = get(f"/api/state/{create_game}").json()["white_pieces"]
    assert wp.get("a2",False) == False
    assert wp.get("a3",False) == "Pawn"
