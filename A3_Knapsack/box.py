# box.py
#
# CS 131 - Artificial Intelligence
# 
# Michael Zhou - Octaber 17, 2024
#
# This file defines what a box is and its properties. A box has an ID, a weight,
# and a value. The box is the item being placed into the knapsack

class Box:
    # Initializing a Box
    def __init__(self, ID: int, weight: int, value: int):
        self.ID = ID
        self.weight = weight
        self.value = value

    # Printing out a Box's information
    def __str__(self) -> str:
        return f"ID: {self.ID} Weight: {self.weight} Value: {self.value}"

    # Equality comparison of two Boxes
    def __eq__(self, other: "Box") -> bool:
        if self.ID != other.ID: return False
        elif self.weight != other.weight: return False
        elif self.value != other.value: return False
        return True
