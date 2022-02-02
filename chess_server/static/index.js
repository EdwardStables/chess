//STATE 
var currentGameId = "none";
var selected_piece = "none"
var selection_state = "CHOOSE_PIECE"


function get_cell(col_letter, row_number) {
  var rows = document.getElementById("chess_board").children[0].children;
  var row = rows[Math.abs(row_number-8)].children;
  var cell = row[letter_to_index(col_letter)] ;
  return cell;
}

function letter_to_index(col_letter) {
  var dict = {'a':0, 'b':1, 'c':2, 'd':3,'e':4, 'f':5, 'g':6, 'h':7};
  return dict[col_letter];
}

function index_to_letter(col_number) {
  var dict = {0:'a', 1:'b', 2:'c', 3:'d',4:'e', 5:'f', 6:'g', 7:'h'};
  return dict[col_number];
}

function highlight(c, r){
  highlight_cell(c, r);
}

function clear_highlight(){
  var letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
  for (var i=1; i <= 8; i++){
    for (var j=0; j <= 7; j++){
      unhighlight_cell(letters[j], i);
    }
  }
}

function highlight_cell(c, r){
  get_cell(c, r).classList.add("highlight");
}

function unhighlight_cell(c, r){
  get_cell(c, r).classList.remove("highlight");
}

function set_piece(c, r, piece, is_white) {
  clear_piece(c, r);
  var cell = get_cell(c, r);
  cell.innerHTML = piece
  if (is_white) {
    cell.classList.add("is_white");
  } else {
    cell.classList.add("is_black");
  }
}

function clear_all_pieces(){
  var letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
  for (var i=1; i <= 8; i++){
    for (var j=0; j <= 7; j++){
      clear_piece(letters[j], i);
    }
  }
}

function clear_piece(c, r){
  var cell = get_cell(c, r);
  cell.innerHTML = ""
  cell.classList.remove("is_white");
  cell.classList.remove("is_black");
}

function add_cell_handlers(table_body){
  for(var i=0; i < table_body.children.length; i++) {
    for(var j=0; j < table_body.children[i].children.length; j++){
      var cell = table_body.children[i].children[j];

      var clickHandler = function(col_letter, row_number) {
        return function() {
          if (selection_state == "CHOOSE_PIECE"){
            server_request("query/"+currentGameId+"?piece="+col_letter+row_number, "GET", query_response_handler);
          } else if (selection_state == "CHOOSE_MOVE"){
            server_request("move/"+currentGameId+"?piece="+selected_piece+"&pos="+col_letter+row_number, "POST", move_response_handler);
          }
        }
      }
      cell.onclick = clickHandler(index_to_letter(j), Math.abs(i-8));
    }
  }
}

function query_response_handler(response){
  console.log("Query response:")
  console.log(response)
  if (response.Status == "Success"){
    clear_highlight();
    highlight(response.Piece[0], response.Piece[1])
    response.Moves.forEach(p => {
      console.log(p)
      highlight(p[0], p[1]);
    });
    selected_piece = response.Piece
    selection_state = "CHOOSE_MOVE"
  } else {
    selection_state = "CHOOSE_PIECE"
    console.log(response.Status);
  }
}

function move_response_handler(response){
  console.log("Move response:")
  console.log(response)
  if (response.Status == "Success"){
    clear_highlight();
    get_game_state(currentGameId);
    selection_state = "CHOOSE_PIECE"
  } else {
    clear_highlight()
    selection_state = "CHOOSE_PIECE"
    console.log(response.Status);
  }
}

function place_pieces(piece_obj, is_white){
  for (const [place, name] of Object.entries(piece_obj)) {
    set_piece(place[0], place[1], name, is_white)
  }
}

function create_game(){
  console.log("Requesting creation of new game...");
  server_request("new", "POST", create_game_response_handler);
}

function create_game_response_handler(response){
  currentGameId = response["game_id"]
  document.getElementById("game_id").textContent = currentGameId
  get_game_state(currentGameId)
}

function get_game_state(currentGameId){
  console.log("Requesting state of game ID " + currentGameId);
  server_request("state/"+currentGameId, "GET", get_game_state_response_handler);
}

function get_game_state_response_handler(response){
  document.getElementById("to_play").textContent = response.to_play ? "White" : "Black";
  clear_all_pieces();
  place_pieces(response.white_pieces, true);
  place_pieces(response.black_pieces, false);
}

window.onload = function () {
  add_cell_handlers(document.getElementById("chess_board").children[0]);
}

function server_request(endpoint, type, handler){
  const Http = new XMLHttpRequest();
  const url='http://127.0.0.1:5000/api/' + endpoint;
  Http.open(type, url);
  Http.send();

  Http.onreadystatechange = (e) => {
    if (Http.readyState === XMLHttpRequest.DONE){
      handler(JSON.parse(Http.responseText))
    }
  }
}