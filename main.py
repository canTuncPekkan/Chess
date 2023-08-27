class Empty:
    def __init__(self, icon: chr, onBoard) -> None:
        self.icon = icon


class Pawn:
    def __init__(self, onBoard, isWhite: bool = True) -> None:
        self.onBoard = onBoard
        self.isWhite = isWhite
        self.icon = '\033[97m♟\033[0m' if isWhite else '\033[30m♟\033[0m'


class Rook:
    def __init__(self, onBoard, isWhite: bool = True) -> None:
        self.onBoard = onBoard
        self.isWhite = isWhite
        self.icon = '\033[97m♜\033[0m' if isWhite else '\033[30m♜\033[0m'


class Knight:
    def __init__(self, onBoard, isWhite: bool = True) -> None:
        self.onBoard = onBoard
        self.isWhite = isWhite
        self.icon = '\033[97m♞\033[0m' if isWhite else '\033[30m♞\033[0m'


class Bishop:
    def __init__(self, onBoard, isWhite: bool = True) -> None:
        self.onBoard = onBoard
        self.isWhite = isWhite
        self.icon = '\033[97m♝\033[0m' if isWhite else '\033[30m♝\033[0m'


class Queen:
    def __init__(self, onBoard, isWhite: bool = True) -> None:
        self.onBoard = onBoard
        self.isWhite = isWhite
        self.icon = '\033[97m♛\033[0m' if isWhite else '\033[30m♛\033[0m'


class King:
    def __init__(self, onBoard, isWhite: bool = True) -> None:
        self.onBoard = onBoard
        self.isWhite = isWhite
        self.icon = '\033[97m♚\033[0m' if isWhite else '\033[30m♚\033[0m'


class ChessBoard:
    """a chess board

    Args:
        FEN (str, optional): The FEN of the boards starting position. Defaults to "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR".
        isWhiteTurn (bool, optional): whos turn it is. Defaults to True.
        emptyIcon (chr, optional): chr place holder for empty squars. Defaults to '_'.
    """

    def __init__(
        self,
        FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
        isWhiteTurn: bool = True,
        emptyIcon: chr = "_",
    ) -> None:
        charToObj = {
            "p": Pawn,
            "r": Rook,
            "n": Knight,
            "b": Bishop,
            "q": Queen,
            "k": King,
        }
        self.isWhiteTurn = isWhiteTurn
        self.emptyIcon = emptyIcon
        self.FEN = FEN
        self.y = ["8", "7", "6", "5", "4", "3", "2", "1"]
        self.x = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.cords = {}
        for colum in self.x:
            for row in self.y:
                self.cords[colum + row] = Empty(self.emptyIcon, self)

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
                    self.cords[self.x[row] + self.y[colum]] = charToObj[FEN[0].lower()](
                        self, True
                    )
                else:
                    self.cords[self.x[row] + self.y[colum]] = charToObj[FEN[0]](
                        self, False
                    )
                FEN = FEN[1:]
                row += 1

    def move(self, algebraicNotation: str) -> bool:
        """moves peces on the boord

        Args:
            algebraicNotation (str): algebraic Notation of the move

        Returns:
            bool: is the move done
        """
        def pawnMove() -> bool:
            """handels pawn moves

            Returns:
                bool: is move sucsesfull
            TODO:
                1) pawn take DONE
                3) Pawn Premote
                4) add enpasant
            BUG:
                1) king being threthened by pawn creats a new dictnary key causing the pawn to go to the 3th dimention DONE

            """
            if algebraicNotation.find("x") > 0:  # the pawn is taking another peace
                if self.isWhiteTurn:  # White to play
                    if (
                        type(self.cords[algebraicNotation[2:4]]) != King
                        and type(self.cords[algebraicNotation[2:4]]) != Empty
                    ):
                        if not self.cords[algebraicNotation[2:4]].isWhite and (
                            type(
                                self.cords[
                                    algebraicNotation[0]
                                    + str(int(algebraicNotation[3]) - 1)
                                ]
                            )
                            == Pawn
                            and self.cords[
                                algebraicNotation[0]
                                + str(int(algebraicNotation[3]) - 1)
                            ].isWhite
                        ):  # is there something we can take on the place the user wants to go
                            self.cords[
                                algebraicNotation[0]
                                + str(int(algebraicNotation[3]) - 1)
                            ] = Empty(self.emptyIcon, self)
                            self.cords[algebraicNotation[2:4]] = Pawn(self, True)
                            self.isWhiteTurn = not self.isWhiteTurn
                            return True
                else:  # Black to play
                    if (
                        type(self.cords[algebraicNotation[2:4]]) != King
                        and type(self.cords[algebraicNotation[2:4]]) != Empty
                    ):
                        if self.cords[algebraicNotation[2:4]].isWhite and (
                            type(
                                self.cords[
                                    algebraicNotation[0]
                                    + str(int(algebraicNotation[3]) + 1)
                                ]
                            )
                            == Pawn
                            and not self.cords[
                                algebraicNotation[0]
                                + str(int(algebraicNotation[3]) + 1)
                            ].isWhite
                        ):  # is there something we can take on the place the user wants to go
                            self.cords[
                                algebraicNotation[0]
                                + str(int(algebraicNotation[3]) + 1)
                            ] = Empty(self.emptyIcon, self)
                            self.cords[algebraicNotation[2:4]] = Pawn(self, False)
                            self.isWhiteTurn = not self.isWhiteTurn
                            return True
            else:  # the pawn is moving forward
                if (
                    type(self.cords[algebraicNotation[0:2]]) == Empty
                ):  # no peice in the place we are trying to move torwards
                    if self.isWhiteTurn:  # White to play
                        if (
                            type(self.cords[algebraicNotation[0] + str(int(algebraicNotation[1]) - 1)]) == Pawn and self.cords[algebraicNotation[0] + str(int(algebraicNotation[1]) - 1)].isWhite
                        ):  # do we have a white pawn on one place below
                            self.cords[
                                algebraicNotation[0]
                                + str(int(algebraicNotation[1]) - 1)
                            ] = Empty(self.emptyIcon, self)
                            self.cords[algebraicNotation[0:2]] = Pawn(self, True)
                            self.isWhiteTurn = not self.isWhiteTurn
                            return True
                        self.cords[algebraicNotation[0] + str(int(algebraicNotation[1]) - 2)] = self.cords[algebraicNotation[0] + str(int(algebraicNotation[1]) - 2)]
                        if (
                            type(self.cords[algebraicNotation[0] + str(int(algebraicNotation[1]) - 2)]) == Pawn
                            and self.cords[algebraicNotation[0] + str(int(algebraicNotation[1]) - 2)].isWhite
                            and int(algebraicNotation[1]) - 2 == 2
                        ):  # do we have a white pawn on two place below and if that place is on the 2 line
                            self.cords[
                                algebraicNotation[0]
                                + str(int(algebraicNotation[1]) - 2)
                            ] = Empty(self.emptyIcon, self)
                            self.cords[algebraicNotation[0:2]] = Pawn(self, True)
                            self.isWhiteTurn = not self.isWhiteTurn
                            return True
                    else:  # Black to play
                        if (
                            type(self.cords[algebraicNotation[0] + str(int(algebraicNotation[1]) + 1)]) == Pawn and not self.cords[algebraicNotation[0] + str(int(algebraicNotation[1]) + 1)].isWhite
                        ):  # do we have a Black pawn on one place below
                            self.cords[
                                algebraicNotation[0]
                                + str(int(algebraicNotation[1]) + 1)
                            ] = Empty(self.emptyIcon, self)
                            self.cords[algebraicNotation[0:2]] = Pawn(self, False)
                            self.isWhiteTurn = not self.isWhiteTurn
                            return True
                        if (
                            type(self.cords[algebraicNotation[0] + str(int(algebraicNotation[1]) + 2)]) == Pawn
                            and not self.cords[algebraicNotation[0] + str(int(algebraicNotation[1]) + 2)].isWhite
                            and int(algebraicNotation[1]) + 2 == 7
                        ):  # do we have a black pawn on two place below and if that place is on the 7 line
                            self.cords[
                                algebraicNotation[0]
                                + str(int(algebraicNotation[1]) + 2)
                            ] = Empty(self.emptyIcon, self)
                            self.cords[algebraicNotation[0:2]] = Pawn(self, False)
                            self.isWhiteTurn = not self.isWhiteTurn
                            return True
            return False
            
        if algebraicNotation[0].islower():  # a pawn is being moved
            return pawnMove()
        elif algebraicNotation[0] == "N":  # a Knight is being moved
            algebraicNotation = algebraicNotation[1:]
            return pawnMove()

    def print(self) -> None:
        """prints the board"""
        turn = "White" if self.isWhiteTurn else "Black"
        print(f"\n{turn} move\n   a b c d e f g h\n")
        for y in self.y:
            print(end=f"{y}  ")
            for x in self.x:
                print(self.cords[x + y].icon, end=" ")
            print(end=f" {y}\n")
        print("\n   a b c d e f g h")


board = ChessBoard(emptyIcon= '\033[32m\u2022\033[0m')
print(board.move("Kf3"))
board.print()