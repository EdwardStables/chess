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
  clear_highlight(); 
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

function clear_piece(c, r){
  console.log("clearing " + c + r);
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
          highlight(col_letter, row_number);
        }
      }

      cell.onclick = clickHandler(index_to_letter(j), Math.abs(i-8));
    }
  }
}

window.onload = function () {
  add_cell_handlers(document.getElementById("chess_board").children[0]);
}