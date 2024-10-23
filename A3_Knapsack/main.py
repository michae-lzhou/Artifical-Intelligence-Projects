# The Knapsack Problem #
# CS 131 - Artificial Intelligence
# 
# Michael Zhou - Octaber 16, 2024
#
# This program will employ the genetic algorithm to perform a local search on a
# set of 12 boxes with varying values and weights. The program will select the
# best possible combination of boxes to put into a knapsack, with a limiting
# weight cap of 250 units. The program will go through multiple
# iterations/generations to reach the optimal solution.

# TODO_LIST:
# TODO: implement the chromosome (begin with the easiest chromosome and make
#       sure everything works - simple 1, 0 for an array of all boxes)
# TODO: implement the selection process (rank based selection, culling by
#       50%)
# TODO: implement the genetic operators (mutation, crossover)
# TODO: implement solution test (goal state) -- you don't really know, you
#       just have to run for X number of iterations and look at the answer
# TODO: implement evolutionary measures (how can i display the metrics?
#       graph? plot? print intermediary states?)

from knapsack import Knapsack
from box import Box

print("Importing libraries... please be patient")
import random
import math
import time
import itertools
import matplotlib.pyplot as plt
import mplcursors
from collections import Counter

# Global variables
popsize_pref = input("What would you like your initial population size to be?"\
                     " (ENTER to use 100) ")
gen_pref = input("How many generations would you like to run? (ENTER to use" \
                 " 100) ")
mut_pref = input("What would you like your mutation rate to be? (ENTER to use" \
                 " 0.01) ")
POP_SIZE = 100
GENERATIONS = 100
MUT_RATE = 0.01
try:
    if popsize_pref != "":
        POP_SIZE = int(popsize_pref)
    if gen_pref != "":
        GENERATIONS = int(gen_pref)
    if mut_pref != "":
        MUT_RATE = float(mut_pref)
except ValueError:
    print("You've entered an invalid input, exiting program")
    exit()

def main():
    # the list that will hold all of the knapsacks within the population
    population = []

    # creating the initial population randomly
    for _ in range(POP_SIZE):
        population.append(Knapsack(rand_list()))

    # for i in population:
    #     print(i)
    #     print()

    print("Running Genetic Algorithm...")

    # the main control flow where the population 
    start = time.time()
    gen_fitness_val, gen_diversity_val = run_evolution(population)
    end = time.time()

    print()
    print("******************** Performance Statistics ********************")
    print(f"Generations:        {GENERATIONS}")
    print(f"Elapsed Time:       {end - start}")
    print(f"Avg Time/Gen:       {(end - start) / GENERATIONS}")

    # plot the fitness and diversity graph
    plot_graph(gen_fitness_val, gen_diversity_val)

# plot_graph will display the metrics of this current run of generations,
# displaying the trend in fitness values and diversity values
def plot_graph(gen_fitness_val: list, gen_diversity_val: list) -> None:
    fig, ax1 = plt.subplots()

    color1 = 'tab:blue'
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Average Fitness Value', color=color1)
    line1, = ax1.plot(gen_fitness_val, color=color1,
             linewidth=3, label='Average Fitness Value')
    ax1.tick_params(axis='y', labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('Average Diversity Value', color=color2)
    line2, = ax2.plot(gen_diversity_val, color=color2,
             linewidth=3, label='Average Diversity Value')
    ax2.tick_params(axis='y', labelcolor=color2)

    fig.tight_layout()
    plt.title('Fitness Value & Diversity Over Generations')

    mplcursors.cursor([line1, line2], hover=True)

    plt.show()

# run_evolution will run through all of the generations indicated and
# (hopefully) reach the most optimal solution
def run_evolution(population: list) -> tuple:
    gen_fitness_val = []
    gen_diversity_val = []
    generations = []
    # elite_sol = population[0]
    for _ in range(GENERATIONS):
        # perform ranking and culling by 50% by using quickselect to find the
        # median in O(n) time, then partition around it in O(n) time to cull the
        # "worse" half, therefore avoiding sorting the population in O(n log n)
        median = quickselect(population, 0, POP_SIZE - 1, math.ceil(POP_SIZE / 2))
        # population[index + 1:] gives the best 50% of the population (culling)
        index = partition(population, 0, POP_SIZE - 1, median)
        # cheesy way to get around handling duplicates in partition..
        index = math.ceil(POP_SIZE / 2)
        if POP_SIZE % 2 == 1: index -= 1
        population = population[index + 1:]

        # crossover: use two parents to create two children, do this
        children = []
        # do so until I have enough children
        while len(children) < POP_SIZE - len(population):
            x = random.randint(0, len(population) - 1)
            y = random.randint(0, len(population) - 1)
            while y == x:
                y = random.randint(0, len(population) - 1)
            child_1, child_2 = population[x].crossover(population[y])
            children.append(child_1)
            children.append(child_2)

        # we may have excess children, so randomly pick from the list of
        # children and append to the culled population until it reaches the
        # original size
        while len(population) != POP_SIZE:
            kid = random.choice(children)
            children.remove(kid)
            if random.random() < MUT_RATE:
                kid.mutate()
            population.append(kid)
        
        #for x in population:
        #    if x.fitness > elite_sol.fitness:
        #        elite_sol = x
        
        # calculate the metrics of this generation
        fitness_val = avg_fitness(population)
        diversity_val = avg_hamming_distance(population)

        gen_fitness_val.append(fitness_val)
        gen_diversity_val.append(diversity_val)

        generations.append(population)

        # TODO: how can i detect whether or not the fitness and diversity vals
        # have converged (been really close for the past X generations),
        # fitness value - depends on the initial population,
        # diversity value - less than 0.12?

        # print()
        # print()
        # print()
        # print("*********** NEW GEN ***********")
        # print()
        # for box in population:
        #     print(box)
        #     print(box.fitness)
        #     print()
    # print out the best solution found from these generations (most common
    # answer)
    counts = Counter(population)
    max_freq = max(counts.values())
    tied_elems = [k for k, v in counts.items() if v == max_freq]
    best_solution = max(tied_elems)
    fitness_confidence = calculate_stability(generations, measure="fitness")
    diversity_confidence = calculate_stability(generations, measure="diversity")
    confidence = fitness_confidence + diversity_confidence

    #print(elite_sol)

    print("******************** BEST SOLUTION FOUND ********************")
    print(best_solution)
    print(f"Confidence: {confidence}%")
    return (gen_fitness_val, gen_diversity_val)

# calculate_stability will calculate how "stable" the solution of the last 1/3
# of the generations are, if they are relatively stable (close to 0), it means
# the algorithm is confident in the solution
def calculate_stability(generations: list, measure: str) -> float:
    if len(generations) < 3:
        return 0.0

    last_third = generations[-len(generations) // 3:]

    if measure == "fitness":
        values = [sum([ind.fitness for ind in gen]) / len(gen) for gen in last_third]
    elif measure == "diversity":
        values = [avg_hamming_distance(gen) for gen in last_third]

    X = list(range(len(values)))
    y = values

    slope = linear_regression_slope(X, y)

    confidence = 1 - min(abs(slope), 1.0)

    return confidence * 50

# linear_regression_slope without using scikitlearn or numpy to reduce import
# time
def linear_regression_slope(X, y):
    n = len(X)
    if n == 0:
        return 0.0

    sum_x = sum(X)
    sum_y = sum(y)
    sum_xy = sum(x * y[i] for i, x in enumerate(X))
    sum_x_squared = sum(x ** 2 for x in X)

    # Calculate slope
    numerator = n * sum_xy - sum_x * sum_y
    denominator = n * sum_x_squared - sum_x ** 2

    if denominator == 0:
        return 0.0  # To avoid division by zero

    slope = numerator / denominator
    return slope

# avg_fitness will calcualte the average fitness values of the current
# generation
def avg_fitness(population: list) -> float:
    return sum(x.fitness for x in population if x.fitness >= 0) / len(population)

# avg_hamming_distance will calculate the average hamming distance between all
# pairs of the population to find a value for the diversity of the current
# generation
def avg_hamming_distance(population: list) -> float:
    filtered_population = [ind for ind in population if ind.fitness >= 0]
    if len(filtered_population) < 2:
        return 0

    hamming_distances = []
    for ind1, ind2 in itertools.combinations(filtered_population, 2):
        hamming_distances.append(sum(c1 != c2 for c1, c2 in
                                     zip(ind1.chromosome, ind2.chromosome)))
    return sum(hamming_distances) / len(hamming_distances)

# quickselect finds the Knapsack with the median fitness value in O(n) time
def quickselect(population: list, l: int, r: int, k: int) -> "Knapsack":
    pivot = random.choice(population[l:r + 1])
    # pivot = population[r]
    if (k > 0 and k <= r - l + 1):
        index = partition(population, l, r, pivot)
        if (index - l == k - 1):
            return population[index]
        if (index - l > k - 1):
            return quickselect(population, l, index - 1, k)

        return quickselect(population, index + 1, r, k - index + l - 1)

# partition is part of the quickselect algorithm (but also used again to filter
# out the bottom half of the population), returns the index of the pivot after
# partitioning -- GeeksforGeeks
def partition(population: list, l: int, r: int, item: "Knapsack") -> int:
    ind = population.index(item)
    population[ind], population[r] = population[r], population[ind]
    x = population[r]
    i = l
    for j in range(l, r):
        if population[j] <= x:
            population[i], population[j] = population[j], population[i]
            i += 1
    population[i], population[r] = population[r], population[i]
    return i

# rand_list generates a list of 12 random 0's and 1's, representing which boxes
# are included within a knapsack
def rand_list():
    return [random.randint(0, 1) for _ in range(Knapsack.LEN_BOXES)]

if __name__ == "__main__":
    main()
