# Chess Game Server

Server that implements chess game logic. Clients send info with HTTP requests to simplifiy usage both locally and over the network. 

Server is agnostic to whether players are real or bots.

Server is essentially a stateful REST API (yeah I know, technically REST shouldn't have state, but good luck making a chess server without state)

## Endpoints

### Get Data
`/api/state/<game_id>`

State of current game

`/api/state`

List overall stats

### Do something
`/api/new`

Create a new game, returns game ID

`/api/move/<game_id>?piece=<piece>&pos=<pos>`

Do a move. Piece is the current position of the piece to move, pos is the target piece.
Fails if the move is invalid, e.g. black move on white turn, pos isn't a valid move, piece is not occupied.
