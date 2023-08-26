class Empty:
    def __init__(self, icon: chr, onBoard) -> None:
        self.icon = icon


class Pawn:
    def __init__(self, cord: tuple, onBoard, isWhite: bool = True) -> None:
        self.onBoard = onBoard
        self.isWhite = isWhite
        self.cord = cord
        self.icon = "♟" if isWhite else "♙"

class Rook:
    def __init__(self, cord: tuple, onBoard, isWhite: bool = True) -> None:
        self.onBoard = onBoard
        self.isWhite = isWhite
        self.cord = cord
        self.icon = "♜" if isWhite else "♖"


class Knight:
    def __init__(self, cord: tuple, onBoard, isWhite: bool = True) -> None:
        self.onBoard = onBoard
        self.isWhite = isWhite
        self.cord = cord
        self.icon = "♞" if isWhite else "♘"


class Bishop:
    def __init__(self, cord: tuple, onBoard, isWhite: bool = True) -> None:
        self.onBoard = onBoard
        self.isWhite = isWhite
        self.cord = cord
        self.icon = "♝" if isWhite else "♗"


class Queen:
    def __init__(self, cord: tuple, onBoard, isWhite: bool = True) -> None:
        self.onBoard = onBoard
        self.isWhite = isWhite
        self.cord = cord
        self.icon = "♛" if isWhite else "♕"


class King:
    def __init__(self, cord: tuple, onBoard, isWhite: bool = True) -> None:
        self.onBoard = onBoard
        self.isWhite = isWhite
        self.cord = cord
        self.icon = "♚" if isWhite else "♔"


class ChessBoard:
    def __init__(self, FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", isWhiteTurn: bool = True, emptyIcon: chr = "_") -> None:
        charToObj = {
            "p": Pawn,
            "r": Rook,
            "n": Knight,
            "b": Bishop,
            "q": Queen,
            "k": King,
        }
        self.FEN = FEN
        self.y = ["8", "7", "6", "5", "4", "3", "2", "1"]
        self.x = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.cords = {}
        for colum in self.x:
            for row in self.y:
                self.cords[colum + row] = Empty(emptyIcon, self)
        row = 0
        colum = 0
        while not (row > 7 and colum == 7):
            if FEN[0] == "/":
                colum += 1
                row = 0
                FEN = FEN[1:]
            elif FEN[0].isnumeric():
                row += int(FEN[0])
                FEN = FEN[1:]
            else:
                if FEN[0].isupper():
                    self.cords[self.x[row] + self.y[colum]] = charToObj[FEN[0].lower()]((7 - colum, row), self, True)
                else:
                    self.cords[self.x[row] + self.y[colum]] = charToObj[FEN[0]]((7 - colum, row), self, False)
                FEN = FEN[1:]
                row += 1

    def print(self) -> None:
        """prints the board"""
        print("\n   a b c d e f g h\n")
        for y in self.y:
            print(end=f"{y}  ")
            for x in self.x:
                print(self.cords[x + y].icon, end=" ")
            print()
        print()


board = ChessBoard()
board.print()