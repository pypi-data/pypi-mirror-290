from dataclasses import dataclass
from decimal import Decimal
from math import sqrt
from typing import Self, Iterator

from math_tompy.symbolic import expr_to_calc
from sympy import Point2D


@dataclass
class Vector2:
    x: Decimal
    y: Decimal

    def __init__(self, x: Decimal, y: Decimal) -> None:
        self.x = Decimal(x)
        self.y = Decimal(y)

    def __add__(self, other: Self) -> Self:
        x_: Decimal = self.x + other.x
        y_: Decimal = self.y + other.y
        vector: Self = Vector2(x=x_, y=y_)
        return vector

    def __sub__(self, other: Self) -> Self:
        x_: Decimal = self.x - other.x
        y_: Decimal = self.y - other.y
        vector: Self = Vector2(x=x_, y=y_)
        return vector

    def __mul__(self, other: Self | Decimal) -> Self:
        if isinstance(other, Vector2):
            x_: Decimal = self.x * other.x
            y_: Decimal = self.y * other.y
        elif isinstance(other, Decimal):
            x_: Decimal = self.x * other
            y_: Decimal = self.y * other
        else:
            raise TypeError(f"Type '{type(other)}' of other is not supported for '{type(Self)}' multiplication.")
        vector: Self = Vector2(x=x_, y=y_)
        return vector

    def __abs__(self) -> Decimal:
        origin = Vector2Injector.from_decimal(x=Decimal(0), y=Decimal(0))
        distance = origin.distance(other=self)
        return distance

    def __iter__(self):
        return iter([self.x, self.y])

    def __len__(self) -> int:
        return 2

    def __getitem__(self, index: int | slice) -> Decimal:
        if isinstance(index, int):
            if int == 0:
                value: Decimal = self.x
            elif int == 1:
                value: Decimal = self.y
            else:
                raise IndexError(f"Index '{index}' out of valid range [0, 1].")
        elif isinstance(index, slice):
            # if wraparound:
            #     value: Self = self._get_slice_with_wraparound(slice_=index)
            # else:
            #     value: Self = self._get_slice(slice_=index)
            raise ValueError(f"__getitem__ does not support slice.")
        else:
            raise ValueError(f"__getitem__ requires an integer or a slice, not a {type(index)}.")
        return value

    def __eq__(self, other: Self) -> bool:
        equality: bool = False
        same_type: bool = isinstance(other, type(self))
        if same_type:
            same_x: bool = self.x == other.x
            same_y: bool = self.y == other.y
            equality = same_x and same_y
        return equality

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.x}, {self.y})"

    @property
    def unit(self) -> Self:
        length: Decimal = abs(self)
        x_: Decimal = self.x / length
        y_: Decimal = self.y / length
        vector: Self = Vector2Injector.from_decimal(x=x_, y=y_)
        return vector

    def distance(self, other: Self) -> Decimal:
        pair_squares: list[Decimal] = [Decimal((value0 - value1) ** 2) for value0, value1 in zip(self, other)]
        square_sum: Decimal = Decimal(sum(pair_squares))
        root_of_pair_square_sum: Decimal = Decimal(sqrt(square_sum))
        return root_of_pair_square_sum


class Vector2Injector:
    @staticmethod
    def from_point(point: Point2D) -> Vector2:
        x: Decimal = Decimal(expr_to_calc(expression=point.x).result())
        y: Decimal = Decimal(expr_to_calc(expression=point.y).result())
        vector: Vector2 = Vector2(x=x, y=y)
        return vector

    @staticmethod
    def from_decimal(x: Decimal, y: Decimal) -> Vector2:
        vector: Vector2 = Vector2(x=x, y=y)
        return vector


def positions_from(samples_x: int, samples_y: int, resolution: Decimal) -> Iterator[Vector2]:
    x_positions: list[Decimal] = [sample * resolution for sample in range(0, samples_x)]
    y_positions: list[Decimal] = [sample * resolution for sample in range(0, samples_y)]

    positions: Iterator[Vector2] = (Vector2Injector.from_decimal(x=x, y=y) for x in x_positions for y in y_positions)

    return positions
