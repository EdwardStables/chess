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

def test_api_state_code_200(server):
    print("running test")
    assert get("/api/state").status_code == 200
    
def test_api_state_game_id_code_200(create_game):
    assert get(f"/api/state/{create_game}").status_code == 200

def test_api_state_game_new_code_200(server):
    assert post(f"/api/new").status_code == 200

def test_api_state_game_move_code_200(create_game):
    assert post(f"/api/move/{create_game}?piece=a2&pos=a3").status_code == 200
