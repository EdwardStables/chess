# Chess Game Server

Server that implements chess game logic. Clients send info with HTTP requests to simplifiy usage both locally and over the network. 

Server is agnostic to whether players are real or bots.

Server is essentially a stateful REST API (yeah I know, technically REST shouldn't have state, but good luck making a chess server without state)

## Endpoints


### Get Data
POST: `api/state`

Body: 
```json
{
    "game_id" : 12345,
    "player_token" : 12345
}
```

Return:
```json
{
    "game_id" : 12345,
    "to_play" : true,
    "is_white" : true,
    "white_pieces" : {
        "a4" : "rook",
        ...,
        "g8" : "queen"
    },
    "black_pieces" : {
        ...
    }
}
```

### Play

POST: `api/move`

Body: 
```json
{
    "game_id" : 12345,
    "player_token" : 12345,
    "move" : ["a4", "a5"]
}
```

Return:
```json
{
    "game_id" : 12345,
    "move_accepted" : true
}
```
or:
```json
{
    "game_id" : 12345,
    "move_accepted" : false,
    "reason" : "Not your move"
}
```
Various reasons are possible:

- Not your move (waiting on other player)
- Piece blocked (if the board was empty then that would be a valid move)
- Invalid positions (one of the given positions was not a valid space on a chess board)
- Invalid move (destination move was not valid for the piece being moved) 

Others will be added as needed