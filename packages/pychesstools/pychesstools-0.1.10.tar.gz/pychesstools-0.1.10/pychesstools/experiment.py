"""An experiment: board as compiled UserDict, with methods linking to step functions."""

import json
import random
import re
from collections import UserDict
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from typing import ClassVar, Final

from . import __RICH_AVAILABLE__, __WORKING_DIRECTORY__
from .board import (
    _COLORS_AND_RANKS,
    _GENERATORS_AND_TYPES,
    BISHOP_GENERATORS,
    BLACK_SQUARES,
    COLORS,
    FEN_REPRESENTATIONS,
    FILES,
    FORWARD_STEP_FUNCTIONS_BY_PAWN_COLOR,
    PIECE_SYMBOLS,
    PLAINTEXT_ABBRS,
    PLAINTEXT_ABBRS_BY_TYPE_AND_COLOR,
    ROOK_GENERATORS,
    SIDES,
    SQUARES,
    Color,
    Piece,
    PieceType,
    Side,
    king_navigable_squares,
    knight_navigable_squares,
    other_color,
    pawn_capturable_squares,
    squares_in_rank,
    step_right,
)

if __RICH_AVAILABLE__:
    import rich.console

    console = rich.console.Console()

with (__WORKING_DIRECTORY__ / "fischer_setups.json").open() as file:
    FISCHER_SETUPS: list[str] = json.load(file)


class Board(UserDict[str, Piece | None]):
    """A chess board."""

    AUTOPRINT: ClassVar[bool] = False
    """Print board upon `__repr__` call."""

    def __init__(self, __dict: dict[str, Piece | None] | None = None) -> None:
        """Create a board."""
        super().__init__(__dict)
        for square in SQUARES:
            if square not in self:
                self.update({square: None})
        self._kings: dict[Color, str] = {}
        self._initial_squares: Final[
            dict[tuple[PieceType, Color, Side | None], str]
        ] = {}

    def __repr__(self) -> str:
        """Get string representation of board."""
        if self.AUTOPRINT:
            self.print()
        return f"Board('{self._piece_repr()}')"

    def __setitem__(self, index: str, value: Piece | None) -> None:
        """Set a square to a piece or None if setting to empty."""
        if value is not None and value.piece_type == "king":
            self._kings[value.color] = index
        self.data[index] = value

    def _piece_repr(self) -> str:
        """Export the board in Extended Position Notation."""
        _repr = ""
        for rank in range(8, 0, -1):
            blank_sq_counter = 0
            for sq in squares_in_rank(rank):
                if (piece := self[sq]) is None:
                    blank_sq_counter += 1
                    continue
                if blank_sq_counter > 0:
                    _repr += str(blank_sq_counter)
                    blank_sq_counter = 0
                _repr += PLAINTEXT_ABBRS_BY_TYPE_AND_COLOR[
                    piece.piece_type, piece.color
                ]
            if blank_sq_counter > 0:
                _repr += str(blank_sq_counter)
            if rank > 1:
                _repr += "/"
        return _repr

    @property
    def pieces(self) -> dict[str, Piece]:
        """Get all pieces on the board."""
        return {sq: piece for sq, piece in self.items() if piece is not None}

    @property
    def ascii(self) -> str:
        """Get an ASCII representation of the board."""
        output = ""
        for rank in range(8, 0, -1):
            output += f"{rank} "
            for sq in squares_in_rank(rank):
                if (piece := self[sq]) is None:
                    output += ". "
                else:
                    output += (
                        f"{PLAINTEXT_ABBRS[piece.piece_type].upper()} "
                        if piece.color == "white"
                        else f"{PLAINTEXT_ABBRS[piece.piece_type].lower()} "
                    )
            output += "\n"
        output += "  a b c d e f g h "
        return output

    @classmethod
    def from_fen(cls, piece_placement_data: str) -> "Board":
        """Create a board from EPD or FEN."""
        if match := re.search(
            r"(?P<R8>[^/]+)/(?P<R7>[^/]+)/(?P<R6>[^/]+)/(?P<R5>[^/]+)/"
            r"(?P<R4>[^/]+)/(?P<R3>[^/]+)/(?P<R2>[^/]+)/(?P<R1>[^/\s]+)",
            piece_placement_data,
        ):
            groups = match.groups()
        else:
            raise ValueError("Could not read piece placement data.")
        self = cls()
        for rank, group in zip(range(8, 0, -1), groups[:8], strict=True):
            cursor = f"a{rank}"
            for char in group:
                if char.isalpha():
                    self[cursor] = Piece(*FEN_REPRESENTATIONS[char])
                    if (cur := step_right(cursor, 1)) is not None:
                        cursor = cur
                elif char.isnumeric():
                    self[cursor] = None
                    if (cur := step_right(cursor, int(char))) is not None:
                        cursor = cur
        return self

    @classmethod
    def staunton_pattern(cls) -> "Board":
        """Create a board with standard piece setup."""
        self = cls()
        for color, pc_rank, pawn_rank in _COLORS_AND_RANKS:
            for file in FILES:
                self[f"{file}{pawn_rank}"] = Piece("pawn", color)
            self[f"a{pc_rank}"] = Piece("rook", color)
            self[f"b{pc_rank}"] = Piece("knight", color)
            self[f"c{pc_rank}"] = Piece("bishop", color)
            self[f"d{pc_rank}"] = Piece("queen", color)
            self[f"e{pc_rank}"] = Piece("king", color)
            self[f"f{pc_rank}"] = Piece("bishop", color)
            self[f"g{pc_rank}"] = Piece("knight", color)
            self[f"h{pc_rank}"] = Piece("rook", color)
        return self

    @classmethod
    def fischer_random(cls) -> "Board":
        """Set board for Fischer random chess / Chess960."""
        return cls.from_fen(random.choice(FISCHER_SETUPS))

    @contextmanager
    def test_position(self, changes: dict[str, Piece | None]) -> Iterator[None]:
        """
        Make temporary changes to the board to test properties of a position.
        Warning: Do not raise exceptions within a `test_position` context manager.
        """
        original_contents = {sq: self[sq] for sq in changes}
        for sq in changes:
            self[sq] = changes[sq]
        yield
        for sq in original_contents:
            self[sq] = original_contents[sq]

    def _rich_renderable(self) -> str:
        """Get a Rich renderable representation of the board."""
        rank_renderable = "\n"
        for rank in range(8, 0, -1):
            rank_renderable += f"[white]{rank}[/white] "
            for sq in squares_in_rank(rank):
                piece = self[sq]
                if piece is not None:
                    color_tags = (
                        ("[reverse][#ffffff]", "[/#ffffff][/reverse]")
                        if piece.color == "white"
                        else ("[white]", "[/white]")
                    )
                    rank_renderable += (
                        f"{color_tags[0]}{PIECE_SYMBOLS[piece.piece_type]}"
                        f" {color_tags[1]}"
                    )
                else:
                    rank_renderable += (
                        "[reverse][#789656]  [/reverse][/#789656]"
                        if sq in BLACK_SQUARES
                        else "[reverse][#f0edd1]  [/reverse][/#f0edd1]"
                    )
            rank_renderable += "\n"
        rank_renderable += "[bold][white]  a b c d e f g h [/bold][/white]\n"
        return rank_renderable

    def print(self, *, plaintext: bool = False) -> None:
        """Print the ChessBoard to console."""
        if not plaintext and __RICH_AVAILABLE__:
            console.print(self._rich_renderable())
        else:
            print(self.ascii)

    def _is_checked_by_rook_bishop_queen(self, color: Color, king_sq: str) -> bool:
        for generator_list, types in _GENERATORS_AND_TYPES:
            for generator in generator_list:
                for sq in generator(king_sq):
                    if (
                        (pc := self[sq]) is not None
                        and pc.color != color
                        and pc.piece_type in types
                    ):
                        return True
                    elif pc is not None:
                        break
        return False

    def _is_checked_by_pawn(self, color: Color, king_sq: str) -> bool:
        return any(
            (pc := self[sq]) is not None
            and pc.piece_type == "pawn"
            and pc.color == other_color(color)
            for sq in pawn_capturable_squares(color, king_sq)
        )

    def _is_checked_by_king(self, color: Color, king_sq: str) -> bool | None:
        return (
            king in king_navigable_squares(king_sq)
            if (king := self._kings.get(other_color(color))) is not None
            else None
        )

    def _is_checked_by_knight(self, color: Color, king_sq: str) -> bool:
        return any(
            (pc := self[sq]) is not None
            and pc.piece_type == "knight"
            and pc.color == other_color(color)
            for sq in knight_navigable_squares(king_sq)
        )

    def set_initial_positions(self) -> None:
        """Set initial positions of pieces used for castling."""
        for color in COLORS:
            rooks = [
                sq
                for sq, pc in self.items()
                if pc is not None and pc.piece_type == "rook" and pc.color == color
            ]
            match len(rooks):
                case 2:
                    (
                        self._initial_squares["rook", color, "queenside"],
                        self._initial_squares["rook", color, "kingside"],
                    ) = (
                        (rooks[0], rooks[1])
                        if FILES.index(rooks[0][0]) < FILES.index(rooks[1][0])
                        else (rooks[1], rooks[0])
                    )
                case 1:
                    for side in SIDES:
                        self._initial_squares["rook", color, side] = rooks[0]
            if self._kings.get(color) is None:
                with suppress(StopIteration):
                    self._kings[color] = next(
                        sq
                        for sq, pc in self.items()
                        if pc is not None
                        and pc.piece_type == "king"
                        and pc.color == color
                    )
            with suppress(KeyError):
                self._initial_squares["king", color, None] = self._kings[color]
        self._piece_count = len(self.pieces)

    def is_checked_square(self, color: Color, square: str) -> bool:
        """Whether a square is threatened by an opposite color piece."""
        return (
            self._is_checked_by_rook_bishop_queen(color, square)
            or self._is_checked_by_pawn(color, square)
            or self._is_checked_by_king(color, square)
            or self._is_checked_by_knight(color, square)
        )

    def king_is_in_check(self, color: Color) -> bool | None:
        """Whether king is in check."""
        return (
            None
            if (king_sq := self._kings.get(color)) is None
            else self.is_checked_square(color, king_sq)
        )

    def _get_piece_at_non_empty_square(self, square: str) -> Piece:
        if (piece := self[square]) is None:
            raise ValueError(f"No piece at square '{square}'.")
        return piece

    def get_threatening_pieces(
        self,
        square: str,
        color: Color | None = None,
        *,
        square_is_empty: bool = False,
    ) -> dict[str, Piece]:
        """
        Get pieces threatening a square. If include_all_pawn_moves, includes forward
        move to tile.
        """
        threatening_pieces: list[tuple[str, Piece]] = []
        color_ = (
            self._get_piece_at_non_empty_square(square).color
            if color is None
            else color
        )
        for generator_list, types in (
            (ROOK_GENERATORS, ("rook", "queen")),
            (BISHOP_GENERATORS, ("bishop", "queen")),
        ):
            for generator in generator_list:
                for sq in generator(square):
                    if (
                        (pc := self[sq]) is not None
                        and pc.color != color_
                        and pc.piece_type in types
                    ):
                        threatening_pieces.append((sq, pc))
                        break
                    elif pc is not None:
                        break
        oc = other_color(color_)
        if (other_king := self._kings.get(oc)) in king_navigable_squares(square):
            pc = self[other_king]
            assert pc is not None
            threatening_pieces.append((other_king, pc))
        sq_iterators: list[tuple[PieceType, tuple[str, ...]]] = [
            ("knight", knight_navigable_squares(square))
        ]
        if not square_is_empty:
            sq_iterators.append(("pawn", pawn_capturable_squares(color_, square)))
        threatening_pieces.extend(
            (sq, pc)
            for pt, iterator in sq_iterators
            for sq in iterator
            if (pc := self[sq]) is not None
            and pc.piece_type == pt
            and pc.color == oc
        )
        if square_is_empty and (
            (
                (sq_ := FORWARD_STEP_FUNCTIONS_BY_PAWN_COLOR[color_](square, 1))
                is not None
                and (pc := self[sq_]) is not None
                and pc.piece_type == "pawn"
                and pc.color == oc
            )
            or (
                pc is None
                and (sq_ := FORWARD_STEP_FUNCTIONS_BY_PAWN_COLOR[color_](square, 2))
                is not None
                and sq_[1] in ("2", "7")
                and (pc := self[sq_]) is not None
                and pc.piece_type == "pawn"
                and pc.color == oc
            )
        ):
            threatening_pieces.append((sq_, pc))
        return dict(threatening_pieces)
