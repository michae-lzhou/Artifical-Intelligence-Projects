# knapsack.py
#
# CS 131 - Artificial Intelligence
# 
# Michael Zhou - Octaber 17, 2024
#
# This file defines what a knapsack is and its properties. A knapsack can hold a
# max weight of 250 units and no limitations on max value.

from box import Box
import random

# Hard coding all of the boxes the problem provides
FIXED_BOXES = [
    Box(0, 20, 6),
    Box(1, 30, 5),
    Box(2, 60, 8),
    Box(3, 90, 7),
    Box(4, 50, 6),
    Box(5, 70, 9),
    Box(6, 30, 4),
    Box(7, 30, 5),
    Box(8, 70, 4),
    Box(9, 20, 9),
    Box(10, 20, 2),
]

pref_boxes = input("Please indicate your preferences for boxes: (ENTER for " \
                   "default boxes; ANY KEY for custom boxes) ")
if pref_boxes != "":
    FIXED_BOXES = []
    try:
        num_boxes = int(input("How many boxes would you like? "))
        for i in range(num_boxes):
            box_weight = int(input(f"How heavy is box {i}: "))
            box_value = int(input(f"How valuable is box {i}: "))
            FIXED_BOXES.append(Box(i, box_weight, box_value))
    except ValueError:
        print("You've entered an invalid input, exiting program")
        exit()

class InvalidKnapsack(Exception):
    pass

class Knapsack:
    # Global variables
    user_pref = input("Please enter the max weight of the knapsack (ENTER" \
                      " to use default 250) ")
    MAX_WEIGHT = 250
    try:
        if user_pref != "":
            MAX_WEIGHT = int(user_pref)
    except ValueError:
        print("You've entered an invalid input, exiting program")
        exit()
    # if MAX_WEIGHT > sum(box.weight for box in FIXED_BOXES):
    #     print(f"Cannot find a combination of boxes with weight greater" \
    #             " than possible, exiting program")
    #     exit()
    MAX_VALUE = sum(x.value for x in FIXED_BOXES)
    LEN_BOXES = len(FIXED_BOXES)

    # determines how sharply overweight knapsacks decline in fitness:
    #       lower number = more tolerance for higher, more overweight knapsacks
    #       higher number = less tolerance for higher, more overweight knapsacks
    #       reasonable range for the problem: NORM_WEIGHT > 0.00055
    NORM_WEIGHT = 40 / pow((0.2 * MAX_WEIGHT), 2)

    # Unused:
    #     # this is used to counteract the effects of high value as a result of high
    #     # weight, since a (340, 30) knapsack is valued less than (360, 40) knapsack,
    #     # and we want the lower weight knapsack overriding value at this point
    #     #       lower number = punish overweight items more harshly
    #     #       higher number = punish overweight items less harshly
    #     #       reasonable range for the problem: NORM_WEIGHT > 0.5
    #     NORM_WEIGHT_2 = 0.5

    # determines how quickly undervalue knapsacks rise in fitness:
    #       ** I wouldn't mess with this value too much besides these two
    #NORM_VALUE = 50/pow(66, 4)
    NORM_VALUE = 50/pow(MAX_VALUE, 4)       # this value is scaled to the maximum total
                                            # value that can be obtained by combined all
                                            # boxes (66)
    #NORM_VALUE = 50/1936                   # this value is scaled to the maximum total
                                            # value that can be obtained at the best
                                            # possible answer (44)

    # Initializing a Knapsack
    def __init__(self, boxes: list) -> None:
        self.boxes = []
        self.weight = 0
        self.value = 0
        self.chromosome = boxes
        if len(boxes) != Knapsack.LEN_BOXES:
            raise InvalidKnapsack("Invalid Knapsack initialization")
        for ind, val in enumerate(boxes):
            if val == 1:
                self.boxes.append(FIXED_BOXES[ind])
                self.weight += FIXED_BOXES[ind].weight
                self.value += FIXED_BOXES[ind].value
        self.fitness = self.fitness_val()

    # Crossing over two Knapsack's chromosomes
    def crossover(self, other: "Knapsack") -> ("Knapsack", "Knapsack"):
        point = random.randint(1, len(FIXED_BOXES))
        new_boxes_1 = self.chromosome[:point] + other.chromosome[point:]
        new_boxes_2 = other.chromosome[:point] + self.chromosome[point:]
        return (Knapsack(new_boxes_1), Knapsack(new_boxes_2))

    # Mutating the Knapsack's chromosomes at a single point
    def mutate(self) -> None:
        point = random.randint(0, len(FIXED_BOXES) - 1)
        target = self.chromosome[point]
        if target == 0:
            self.chromosome[point] = 1
            self.boxes.append(FIXED_BOXES[point])
        if target == 1:
            self.chromosome[point] = 0
            self.boxes.remove(FIXED_BOXES[point])
        # recompute the values
        self.weight = sum(box.weight for box in self.boxes)
        self.value = sum(box.value for box in self.boxes)
        self.fitness = self.fitness_val()

    # Calculating the fitness of the current knapsack
    # Rationale: the value rises quadratically, "maxing out" at 66 (total value
    #            of all items combined), giving a fitness value of 50.
    #            the weight rises inverse-quadratically, "maxing out" at 250
    #            (max weight of a knapsack) with a fitness value of 50. If the
    #            weight is past 250, decrease inverse-quadratically, "bottoming"
    #            at 300 with a fitness value of 0. Therefore, more overweight
    #            knapsacks are valued less than more underweight knapsacks,
    #            since it would be more likely for an underweight knapsack to
    #            gain more items than an equally overweight knapsack to lose
    #            more items.
    #            Hence, the perfect knapsack would have a total value of 66 and
    #            weight of 250, giving a total fitness score of 100 -- but this
    #            isn't possible so the fitness value will mostly be around
    #            20-70 from random testing experience. A fitness value of above
    #            60 is really good.
    # Areas for Improvement: at very very high knapsack weights and varying
    #                        knapsack values, the fitness value becomes very
    #                        unpredictable (may go into the negatives),
    #                        although it will be mostly below 20. Some sort of
    #                        dynamically fitting function that more neatly tucks
    #                        it between 0 and ~15 would be nice, but would be
    #                        drastically harder to implement with little to no
    #                        impact on outcome. to work around this issue when
    #                        calculating average fitness for performance
    #                        metrics, we can ignore outliers with fitness value
    #                        below 0.
    def fitness_val(self) -> int:
        weight_fitness = 0
        value_fitness = 0
        if self.weight <= Knapsack.MAX_WEIGHT:
            weight_fitness = (-30 / pow(-Knapsack.MAX_WEIGHT, 2)) * \
                             pow((self.weight - Knapsack.MAX_WEIGHT), 2) + 30
            # weight_fitness = 0.2 * self.weight
        elif self.weight <= pow(30 / Knapsack.NORM_WEIGHT, 1/2) + \
                            Knapsack.MAX_WEIGHT:
            # don't immediately start my drop off curve at 50 when i'm past
            # 250 because i don't really want anything over 260
            weight_fitness = -1 * Knapsack.NORM_WEIGHT * \
                             pow((self.weight - Knapsack.MAX_WEIGHT), 2) + 25
        else:
            weight_fitness = -0.2 * (self.weight - 1.2 * Knapsack.MAX_WEIGHT)
            # weight_fitness = -1 * pow((self.weight - 300) /
            #                           Knapsack.NORM_WEIGHT_2, 1/2)
        value_fitness = Knapsack.NORM_VALUE * pow((self.value), 4)
        return weight_fitness + value_fitness
        # weight_sub = abs(self.weight - Knapsack.MAX_WEIGHT) * \
        #              Knapsack.NORM_WEIGHT
        # val_add = self.value * Knapsack.NORM_VALUE
        # return Knapsack.INIT_FITNESS - weight_sub + val_add

    # Checking if the two items are the same Knapsacks
    def equal(self, other: "Knapsack") -> bool:
        # for ind, box in enumerate(self.chromosome):
        #     if box != other.chromosome[ind]: return False
        if self.weight != other.weight: return False
        elif self.value != other.value: return False
        elif self.fitness != other.fitness: return False
        return True

    # Printing out a Knapsack's information
    def __str__(self) -> str:
        boxes_list = ',\n'.join(str(box) for box in self.boxes)
        return f"[Boxes:\n{boxes_list}]\nTotal Weight: {self.weight}\n" \
               f"Total Value: {self.value}\nFitness Value: {self.fitness}"

    # Less-than comparison of two Knapsacks' fitness values
    def __lt__(self, other: "Knapsack") -> bool:
        return self.fitness < other.fitness

    # Greater-than comparison of two Knapsacks' fitness values
    def __gt__(self, other: "Knapsack") -> bool:
        return self.fitness > other.fitness

    # Equality comparison of two Knapsacks' fitness values
    def __eq__(self, other: "Knapsack") -> bool:
        return self.chromosome == other.chromosome and \
               self.fitness == other.fitness

    # Less-than or equal to comparison of two Knapsacks' fitness values
    def __le__(self, other: "Knapsack") -> bool:
        return self.fitness <= other.fitness

    # Hashing function
    def __hash__(self):
        return hash((tuple(self.chromosome), self.fitness))
