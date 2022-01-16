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

def get_moves(piece):
    if type(piece) != list:
        piece = [piece]
    b = Board(piece)
    return piece[0].moves(b) 

def test_surround_positions():
    assert set(run_iterator(surrounding_positions, "b2")) == {"a1","b1","c1","c2","c3","b3","a3","a2"}
