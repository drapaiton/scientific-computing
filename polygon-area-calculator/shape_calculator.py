from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(order=True)
class Rectangle:
    width:float
    height:float

    def set_width(self, new_width):
        self.width = new_width

    def set_height(self, new_height):
        self.height = new_height

    def get_area(self):
        return self.height * self.width
    def get_perimeter(self):
        return 2 * self.width + 2 * self.height

    def get_diagonal(self):
        return (self.width ** 2 + self.height ** 2) ** .5

    def get_picture(self)->str:
        if max(self.width,self.height) > 50:
            return "Too big for picture."
        else:
            row:str = "*" * int(self.width) + "\n"
            picture:str = row * int(self.height)
            return picture

    def get_amount_inside(self,another_shape:Rectangle):
        times_horizontal = self.width/another_shape.width
        times_horizontal = math.floor(times_horizontal)

        times_vertical = self.height/another_shape.height
        times_vertical = math.floor(times_vertical)

        return times_horizontal * times_vertical

@dataclass(init=False,repr=False)
class Square(Rectangle):
    side:float

    def __init__(self, side:float):
        super().__init__(side, side)
        self.side = side

    def set_side(self,side:float):
        self.width = side
        self.height = side
        self.side = side

    def set_width(self,width:float):
        self.width=width
        self.height=width
        self.side=width

    def set_height(self,height:float):
        self.width=height
        self.height=height
        self.side=height

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__ + f"(side={self.side})"
