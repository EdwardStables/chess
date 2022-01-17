from chess import *

def test_validate_position():
    assert validate_position("a1") 
    assert validate_position("h1") 
    assert not validate_position("i1") 
    assert not validate_position("a0") 
    assert not validate_position("a9") 

def board_pieces_rook():
    return [Rook("a1", True), Rook("h8", False)]

def board_pieces_bishop():
    return [Bishop("b2", True)]

def test_board_occupied():
    b = Board(board_pieces_rook())
    assert b.occupied("a1") == True
    assert b.occupied("b1") == None
    assert b.occupied("h8") == False

def test_surround_positions():
    assert set(run_iterator(surrounding_positions, "b2")) == {"a1","b1","c1","c2","c3","b3","a3","a2"}

def test_iterate_board_diag():
    # to top right
    assert run_iterator(iterate_board_diag, "a1", 0) == ["b2","c3","d4","e5","f6","g7","h8"]
    assert run_iterator(iterate_board_diag, "g7", 0) == ["h8"]
    assert run_iterator(iterate_board_diag, "h8", 0) == []
    # to bottom right
    assert run_iterator(iterate_board_diag, "a8", 1) == ["b7","c6","d5","e4","f3","g2","h1"]
    assert run_iterator(iterate_board_diag, "g2", 1) == ["h1"]
    assert run_iterator(iterate_board_diag, "h1", 1) == []
    # to bottom left
    assert run_iterator(iterate_board_diag, "h8", 2) == ["g7","f6","e5","d4","c3","b2","a1"]
    assert run_iterator(iterate_board_diag, "b2", 2) == ["a1"]
    assert run_iterator(iterate_board_diag, "a1", 2) == []
    # to top left
    assert run_iterator(iterate_board_diag, "h1", 3) == ["g2","f3","e4","d5","c6","b7","a8"]
    assert run_iterator(iterate_board_diag, "b7", 3) == ["a8"]
    assert run_iterator(iterate_board_diag, "a8", 3) == []

def run_iterate_board_diag(start, dir):
    out = []
    for pos in iterate_board_diag(start, dir):
        out.append(pos)
    return out

def test_iterate_board():
    # a->h
    assert run_iterator(iterate_board, "a1", 0) == ["b1","c1","d1","e1","f1","g1","h1"]
    assert run_iterator(iterate_board, "g8", 0) == ["h8"]
    assert run_iterator(iterate_board, "h1", 0) == []
    # h->a
    assert run_iterator(iterate_board, "a1", 1) == []
    assert run_iterator(iterate_board, "b1", 1) == ["a1"]
    assert run_iterator(iterate_board, "h1", 1) == ["g1","f1","e1","d1","c1","b1","a1"]
    # 1->8
    assert run_iterator(iterate_board, "a1", 2) == ["a2","a3","a4","a5","a6","a7","a8"]
    assert run_iterator(iterate_board, "h7", 2) == ["h8"]
    assert run_iterator(iterate_board, "a8", 2) == []
    # 8->1
    assert run_iterator(iterate_board, "a1", 3) == []
    assert run_iterator(iterate_board, "a2", 3) == ["a1"]
    assert run_iterator(iterate_board, "h8", 3) == ["h7","h6","h5","h4","h3","h2","h1"]

def run_iterator(iterator, *args):
    out = []
    for pos in iterator(*args):
        out.append(pos)
    return out

def test_rook_moves_empty_board():
    assert get_moves(Rook("a1", True)) ==  {"b1","c1","d1","e1","f1","g1","h1",
                                            "a2","a3","a4","a5","a6","a7","a8"}

def test_rook_moves_friendly():
    pieces = [Rook("a1",True),Rook("a2",True),Rook("b1",True)]
    assert get_moves(pieces) == set()

def test_rook_moves_unfriendly():
    pieces = [Rook("a1",True),Rook("a2",False),Rook("b1",False)]
    assert get_moves(pieces) == {"a2","b1"}

def test_rook_moves_empty_board_black():
    assert get_moves(Rook("a1", True)) ==  {"b1","c1","d1","e1","f1","g1","h1",
                                            "a2","a3","a4","a5","a6","a7","a8"}

def test_rook_moves_friendly_black():
    pieces = [Rook("a1",False),Rook("a2",False),Rook("b1",False)]
    assert get_moves(pieces) == set()

def test_rook_moves_unfriendly_black():
    pieces = [Rook("a1",False),Rook("a2",True),Rook("b1",True)]
    assert get_moves(pieces) == {"a2","b1"}

def test_bishop_moves_empty_board():
    assert get_moves(Bishop("b2", True)) == {"a1","c1","a3",
                                             "c3","d4","e5","f6","g7","h8"}

def test_bishop_moves_friendly():
    pieces = [Bishop("b2",True),Bishop("c3",True),Bishop("a3",True)]
    assert get_moves(pieces) == {"a1","c1"}

def test_bishop_moves_unfriendly():
    pieces = [Bishop("b2",True),Bishop("c3",False),Bishop("a3",False)]
    assert get_moves(pieces) == {"a1","c1","c3","a3"}

#queen is annoying to test, but should be covered by previous
def test_queen_moves_empty_board():
    assert get_moves(Queen("b2", True)) == {"a1","c3","d4","e5","f6","g7","h8",
                                            "a2","c2","d2","e2","f2","g2","h2",
                                            "b1","b3","b4","b5","b6","b7","b8",
                                            "c1","a3"}

def test_king_moves_empty_board():
    assert get_moves(King("b2", True)) == {"a1","b1","c1","c2","c3","b3","a3","a2"}

def test_king_moves_friendly():
    pieces = [King("a1", True),King("a2",True)]
    assert get_moves(pieces) == {"b1","b2"}

def test_king_moves_empty_board():
    pieces = [King("a1", True),King("a2",False)]
    assert get_moves(pieces) == {"b1","b2","a2"}

def test_pawn_moves_empty_board_white():
    assert get_moves(Pawn("b2", True)) == {"b3","b4"}

def test_pawn_moves_empty_board_white_has_moved():
    p = Pawn("b2", True)
    p.has_moved = True
    assert get_moves(p) == {"b3"}

def test_pawn_moves_white_friendly():
    pieces = [Pawn("b2", True), Pawn("b3", True)]
    assert get_moves(pieces) == set()

def test_pawn_moves_white_friendly_has_moved():
    pieces = [Pawn("b2", True), Pawn("b3", True)]
    pieces[0].has_moved = True
    assert get_moves(pieces) == set()

def test_pawn_moves_white_unfriendly():
    pieces = [Pawn("b2", True), Pawn("b3", False), Pawn("c3", False), Pawn("a3", False)]
    assert get_moves(pieces) == {"a3", "c3"}

def test_pawn_moves_empty_board_black():
    assert get_moves(Pawn("b7", False)) == {"b6","b5"}

def test_pawn_moves_empty_board_black_has_moved():
    p = Pawn("b7", False)
    p.has_moved = True
    assert get_moves(p) == {"b6"}

def test_pawn_moves_black_friendly():
    pieces = [Pawn("b7", False), Pawn("b6", False)]
    assert get_moves(pieces) == set()

def test_pawn_moves_black_friendly_has_moved():
    pieces = [Pawn("b7", False), Pawn("b6", False)]
    pieces[0].has_moved = True
    assert get_moves(pieces) == set()

def test_pawn_moves_black_unfriendly():
    pieces = [Pawn("b7", False), Pawn("b6", True), Pawn("c6", True), Pawn("a6", True)]
    assert get_moves(pieces) == {"a6", "c6"}
    pieces = [Pawn("b7", False), Pawn("c6", True), Pawn("a6", True)]
    assert get_moves(pieces) == {"a6", "c6","b6","b5"}

def test_knight_moves_empty_board():
    assert get_moves(Knight("c3",True)) == {"a2","a4","d1","b1","e2","e4","d5","b5"}

def test_knight_moves_empty_board_edge():
    assert get_moves(Knight("a1",True)) == {"c2","b3"}

def test_knight_moves_empty_board_friendly():
    pieces = [Knight("a1",True), Knight("b3",True)]
    assert get_moves(pieces) == {"c2"}

def test_knight_moves_empty_board_friendly_jump():
    pieces = [Knight("a1",True), Knight("b1",True),Knight("b2",True),Knight("a2",True)]
    assert get_moves(pieces) == {"c2","b3"}

def test_knight_moves_empty_board_unfriendly():
    pieces = [Knight("a1",True), Knight("b3",False)]
    assert get_moves(pieces) == {"c2","b3"}

def test_knight_moves_empty_board_unfriendly_jump():
    pieces = [Knight("a1",True), Knight("b1",False),Knight("b2",False),Knight("a2",False)]
    assert get_moves(pieces) == {"c2","b3"}

def get_moves(piece):
    if type(piece) != list:
        piece = [piece]
    b = Board(piece)
    return piece[0].moves(b) 

def test_populate_chessboard():
    b = populate_chessboard()
    assert b.validate()

def test_board_all_moves():
    pieces = [Rook("a1",True),Knight("b1",True),Pawn("a2",True),Pawn("b2",True)]
    board = Board(pieces) 
    assert board.all_moves(True) == {
        pieces[0] : set(),
        pieces[1] : {"a3","c3","d2"},
        pieces[2] : {"a3","a4"},
        pieces[3] : {"b3","b4"}
    }

def test_board_move():
    pieces = [Rook("a1",True),Knight("b1",True),Pawn("a2",True),Pawn("b2",True)]
    board = Board(pieces) 
    assert not board.move(pieces[1], "d3")
    assert pieces[1].pos == "b1"
    assert board.move(pieces[1], "a3")
    assert pieces[1].pos == "a3"
