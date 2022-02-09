from __future__ import annotations
from operator import indexOf
from typing import Set, List


CHESS_BOARD_LETTERS = ['a','b','c','d','e','f','g','h']

class Chess:
    def __init__(self):
        self.board = populate_chessboard()
        self.to_play = True

    def get_white_pieces(self):
        return {p.pos : p.name for p in self.board.all_pieces() if p.is_white}    

    def get_black_pieces(self):
        return {p.pos : p.name for p in self.board.all_pieces() if not p.is_white}    

class Board:
    def __init__(self, pieces: List[Piece]):
        self._pieces = pieces

    def can_move(self, pos, piece_colour):
        return self.occupied(pos) != piece_colour

    def all_pieces(self) -> List[Piece]:
        return self._pieces

    def occupied(self, pos):
        for p in self._pieces:
            if p.pos == pos:
                return True if p.is_white else False
        return None

    def get_piece(self, pos) -> Piece:
        for p in self._pieces:
            if p.pos == pos:
                return p
        return None

    def all_moves(self, side: bool):
        sided_pieces = filter(lambda p: p.is_white==side, self._pieces)

        def split(movelist):
            moves = set()
            takes = set()
            for m in movelist:
                gp = self.get_piece(m)
                (moves if gp is None or gp.is_white==side else takes).add(m)
            return (moves, takes)

        return {p : split(p.moves(self)) for p in sided_pieces}

    def validate(self):
        #Run a set of rules to ensure that the board is legal
        positions = [p.pos for p in self._pieces]
        #no duplicated positions
        if len(positions) != len(set(positions)):
            return False
        #no illegal positions
        if any((not validate_position(p)) for p in positions):
            return False

        return True

    def move(self, piece: Piece, pos):
        #is this is a piece we have
        if piece not in self._pieces:
            return False

        valid_moves = piece.moves(self)
        if pos not in valid_moves:
            return False

        piece.pos = pos
        piece.has_moved = True
        return True


def populate_chessboard():
    pieces = [
        Pawn("a2", True),Pawn("b2", True),Pawn("c2", True),Pawn("d2", True),
        Pawn("e2", True),Pawn("f2", True),Pawn("g2", True),Pawn("h2", True),
        Rook("a1", True),Knight("b1", True),Bishop("c1", True),Queen("d1", True),
        King("e1", True),Bishop("f1", True),Knight("g1", True),Rook("h1", True),
        Pawn("a7", False),Pawn("b7", False),Pawn("c7", False),Pawn("d7", False),
        Pawn("e7", False),Pawn("f7", False),Pawn("g7", False),Pawn("h7", False),
        Rook("a8", False),Knight("b8", False),Bishop("c8", False),Queen("d8", False),
        King("e8", False),Bishop("f8", False),Knight("g8", False),Rook("h8", False),
    ]
    return Board(pieces)

class Piece:
    def __init__(self, name, pos: str, is_white: bool):
        self.name = name
        self.pos = pos
        self.is_white = is_white
        validate_position(self.pos)
        self.has_moved = False

    def moves(board) -> Set[str]:
        raise NotImplementedError

    def cardinal_iteration(self, board: Board) -> Set[str]:
        positions = set()
        for dir in range(0,4):
            for pos in iterate_board(self.pos, dir):
                occ = board.occupied(pos)
                if  occ is None:
                    positions.add(pos)
                    continue
                if occ != self.is_white:
                    positions.add(pos)
                break
        return positions

    def diagonal_iteration(self, board: Board) -> Set[str]:
        positions = set()
        for dir in range(0,4):
            for pos in iterate_board_diag(self.pos, dir):
                occ = board.occupied(pos)
                if  occ is None:
                    positions.add(pos)
                    continue
                if occ != self.is_white:
                    positions.add(pos)
                break
        return positions

class Rook(Piece):
    def __init__(self, pos, is_white):
        super().__init__("Rook", pos, is_white)

    def moves(self, board: Board):
        return self.cardinal_iteration(board)

class Bishop(Piece):
    def __init__(self, pos, is_white):
        super().__init__("Bishop", pos, is_white)

    def moves(self, board: Board):
        return self.diagonal_iteration(board)

class Queen(Piece):
    def __init__(self, pos, is_white):
        super().__init__("Queen", pos, is_white)

    def moves(self, board: Board):
        return self.diagonal_iteration(board).union(self.cardinal_iteration(board))

class King(Piece):
    def __init__(self, pos, is_white):
        super().__init__("King", pos, is_white)

    def moves(self, board: Board):
        positions = set()
        for p in surrounding_positions(self.pos):
            if board.can_move(p,self.is_white):
                positions.add(p)
        return positions

class Pawn(Piece):
    def __init__(self, pos, is_white):
        super().__init__("Pawn", pos, is_white)
    
    def moves(self, board: Board):
        dir = 1 if self.is_white else -1
        let = self.pos[0]
        let_num = indexOf(CHESS_BOARD_LETTERS, let)
        num = int(self.pos[1])

        positions = set()

        if num < 8 and board.occupied(n := f"{let}{num+dir}") is None:
            positions.add(n)
            if not self.has_moved and board.occupied(n := f"{let}{num+2*dir}") is None:
                positions.add(n)
            
        if let_num > 0 and board.occupied(n := f"{CHESS_BOARD_LETTERS[let_num-1]}{num+dir}") == (not self.is_white):
            positions.add(n)

        if let_num < 7 and board.occupied(n := f"{CHESS_BOARD_LETTERS[let_num+1]}{num+dir}") == (not self.is_white):
            positions.add(n)

        return positions

class Knight(Piece):
    def __init__(self, pos, is_white):
        super().__init__("Knight", pos, is_white)
    
    def moves(self, board: Board):
        let = self.pos[0]
        let_num = indexOf(CHESS_BOARD_LETTERS, let)+2
        local_CBL = ["k", "k"] + CHESS_BOARD_LETTERS + ["k", "k"]
        num = int(self.pos[1])
        positions = filter(validate_position, [
            f"{local_CBL[let_num-2]}{num-1}",
            f"{local_CBL[let_num-2]}{num+1}",
            f"{local_CBL[let_num-1]}{num+2}",
            f"{local_CBL[let_num+1]}{num+2}",
            f"{local_CBL[let_num+2]}{num-1}",
            f"{local_CBL[let_num+2]}{num+1}",
            f"{local_CBL[let_num-1]}{num-2}",
            f"{local_CBL[let_num+1]}{num-2}",
        ])

        positions = filter(lambda p: board.can_move(p, self.is_white), positions)

        return set(positions)

def surrounding_positions(pos: str):
    letter = pos[0]
    letter_ind = indexOf(CHESS_BOARD_LETTERS, letter)
    num = int(pos[1])
    positions = set()
    if letter_ind > 0:
        for n in range(num-1,num+2):
            positions.add(f"{CHESS_BOARD_LETTERS[letter_ind-1]}{n}")
    for n in range(num-1,num+2):
        positions.add(f"{letter}{n}")
    if letter_ind < len(CHESS_BOARD_LETTERS):
        for n in range(num-1,num+2):
            positions.add(f"{CHESS_BOARD_LETTERS[letter_ind+1]}{n}")
    for p in positions:
        if 1 <= int(p[1:]) <= 8 and p != pos:
            yield p

def iterate_board_diag(start, dir):
    letter = start[0]
    letter_ind = indexOf(CHESS_BOARD_LETTERS, letter)
    num = int(start[1])
    if dir == 0: #to top right
        while letter_ind < len(CHESS_BOARD_LETTERS)-1 and num < 8:
            yield CHESS_BOARD_LETTERS[(letter_ind := letter_ind+1)] + str(num:=num+1)
    if dir == 1: #to bottom right
        while letter_ind < len(CHESS_BOARD_LETTERS)-1 and num > 1:
            yield CHESS_BOARD_LETTERS[(letter_ind := letter_ind+1)] + str(num:=num-1)
    if dir == 2: #to bottom left
        while letter_ind > 0 and num > 1:
            yield CHESS_BOARD_LETTERS[(letter_ind := letter_ind-1)] + str(num:=num-1)
    if dir == 3: #to top left
        while letter_ind > 0 and num < 8:
            yield CHESS_BOARD_LETTERS[(letter_ind := letter_ind-1)] + str(num:=num+1)

def iterate_board(start, dir):
    letter = start[0]
    letter_ind = indexOf(CHESS_BOARD_LETTERS, letter)
    num = int(start[1])
    if dir == 0: #a -> h
        while letter_ind < len(CHESS_BOARD_LETTERS)-1:
            yield CHESS_BOARD_LETTERS[(letter_ind := letter_ind+1)] + str(num)
    if dir == 1: #h -> a
        while letter_ind > 0:
            yield CHESS_BOARD_LETTERS[(letter_ind := letter_ind-1)] + str(num)
    if dir == 2: #1 -> 8
        while num < 8:
            yield letter + str(num:=num+1)
    if dir == 3: #8 -> 1
        while num > 1:
            yield letter + str(num:=num-1)

def validate_position(position: str) -> bool:
    if len(position) != 2:
        return False
    if position[0] not in CHESS_BOARD_LETTERS:
        return False
    if not(1 <= int(position[1]) <= 8):
        return False
    return True
