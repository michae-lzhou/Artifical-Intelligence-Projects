# The Pancake Problem
#
# CS 131 - Artificial Intelligence
#
# Michael Zhou - October 9, 2024
# 
# This program will solve the pancake problem using gap heuristics

import random
from searchable_heap import SearchableHeap
import time

def main():
    # The search problem will be defined as follows:
    # Initial State: the initial "problem" (or the layout of the pancakes)
    # Possible Actions: flipping at position x, where all pancakes above
    #                   position x is flipped.
    # Successor Function: each flip will bring the "agent" to a new state of the
    #                     problem with a new layout of pancakes
    # Goal Test: all of the pancakes are sorted in decreasing order, with the
    #            largest pancake at the bottom of the plate
    # Path Cost Function: each action costs 1 unit, since the decision of which
    #                     position to flip is irrelevant to the problem, only
    #                     the total number of flips

    # setting up the problem and search space with either user input or
    # randomized values

    print("-------------------------------------------------------------------------------")
    print("---                           PREFERENCE SETTING                            ---")
    print("-------------------------------------------------------------------------------")

    l_list = input("Please indicate how many pancakes you'd like (Press ENTER" +
                   " to skip) ")
    pnck_list = []
    
    if l_list == "":
        l_list = random.randint(1, 30)
        pnck_list = random.sample(range(1, int(l_list) + 1), int(l_list))
    elif l_list.isnumeric():
        # allowing the user to randomly generate a list of custom length
        custom = input("Would you like to generate a custom list? (y, n) ")

        # allowing the user to generate a custom list
        if custom == 'y':
            print("Only enter unique values from 1 to", l_list)
            dupe = set()
            for i in range(int(l_list)):
                val = input("Value: ")
                if val in dupe:
                    print("ERROR: You entered a duplicate value, exiting program.")
                    return
                if not val.isnumeric():
                    print("ERROR: You didn't enter a number, exiting program.")
                    return
                dupe.add(val)
                pnck_list.append(int(val))
            if not check_list(pnck_list):
                print("ERROR: You did not enter a valid set of values," \
                      " exiting program.")
                return
        # randomly generating a list
        else:
            pnck_list = random.sample(range(1, int(l_list) + 1), int(l_list))
    else:
        print("ERROR: You didn't enter a valid number, exiting program.")
        return

    display_children = input("Display algorithm details and debug information?" \
                             " (press any key to display, ENTER to skip) ")

    ucs = input("Press any key to select the UCS algorithm, ENTER to select " \
                "A* algorithm ")

    print("-------------------------------------------------------------------------------")
    print("---                             INITIAL STATE                               ---")
    print("-------------------------------------------------------------------------------")
    print("Length of list:  ", l_list)

    print("Initial State:   ", pnck_list)

    # initialize some data structures to hold relevant information
    frontier = SearchableHeap()
    cost = {tuple(pnck_list) : 0}
    visited = set()
    parent = {}

    # initialize frontier with the initial state of the problem
    if not ucs: frontier.push((cost[tuple(pnck_list)] + h_func(pnck_list), tuple(pnck_list)))
    else: frontier.push((0, tuple(pnck_list)))
    parent[tuple(pnck_list)] = None
    print("Frontier:        ", frontier)

    # The backward cost function for this problem will be the 
    # flips it took to get to the current state through the initial state.

    print()
    print("-------------------------------------------------------------------------------")
    if not ucs: print("---                        BEGINNING A* ALGORITHM                           ---")
    else: print("---                        BEGINNING UCS ALGORITHM                          ---")
    print("-------------------------------------------------------------------------------")

    start_time = time.time()

    # while loop to run until we find the target (or when we run out of
    # unexplored nodes) 
    while len(frontier) != 0:
        # choose the smallest forward + backward cost state to explore next
        min_node = frontier.pop()
        print()
        print("Beginning a new iteration...")
        print()
        print("Curr State:      ", min_node[1])
        print("Curr Total Cost: ", min_node[0])
        # print("Frontier:", frontier)

        # check if we've reached the goal state
        if (h_func((min_node[1])) == 0):
            # an upside-down pancake also qualifies for our goal state
            # so we have to do some clean up
            if (min_node[1][-1] != 1):
                temp = flip(min_node[1], 0)
                parent[temp] = min_node[1]
                print()
                print("Flipping the whole stack. One second..")
                print()
                print("-------------------------------------------------------------------------------")
                print("Solution Found! This solution took", \
                      cost[tuple(min_node[1])] + 1, "flips.")
                print("Solution: ", tuple(temp))
                print()
                print_path(temp, parent)
                print()
                end_time = time.time()
                print("Elapsed Time: ", end_time - start_time)
                print("-------------------------------------------------------------------------------")
                print()
                return
            else:
                print()
                print("-------------------------------------------------------------------------------")
                print("Solution Found! This solution took", \
                      cost[tuple(min_node[1])], "flips.")
                print("Solution: ", min_node[1])
                print()
                print_path(min_node[1], parent)
                print()
                end_time = time.time()
                print("Elapsed Time: ", end_time - start_time)
                print("-------------------------------------------------------------------------------")
                print()
                return

        # added the current node to the visited list
        visited.add(min_node[1])

        # each "slot" is a possible successor (i.e. if the pancake is [1, 2, 3],
        # we have 3 "slots" to flip from: from 1, from 2, from 3)
        for i in range(int(l_list) - 1):
            child_pnck = flip(min_node[1], i)
            if display_children: 
                print()
                print("Child", i, ":        ", child_pnck)

            # current state's cost + 1 to reach the child state
            backward_cost = cost[tuple(min_node[1])] + 1

            cost[tuple(child_pnck)] = backward_cost
            # print("backward cost: ", backward_cost)
            forward_cost = 0
            if not ucs: forward_cost = h_func(child_pnck)
            tot_cost = backward_cost + forward_cost
            # print("tot cost: ", tot_cost)

            # if child is not in frontier or visited, insert child in frontier
            if not frontier.search((tot_cost, tuple(child_pnck))) and not child_pnck in visited:
                frontier.push((tot_cost, tuple(child_pnck)))
            # if child is in frontier with higher cost, replace the child in
            # frontier
            # elif frontier.search((tot_cost, tuple(child_pnck))[0]) > tot_cost:
            #     frontier.update(frontier.search((tot_cost, tuple(child_pnck)),
            #                                     (tot_cost, tuple(child_pnck))))
            elif cost[tuple(child_pnck)] > tot_cost:
                frontier.update(frontier.search(cost[tuple(child_pnck)], tuple(child_pnck)),
                                                (tot_cost, tuple(child_pnck)))
            else:
                if display_children: print("Ignoring this child..")
                continue

            # keeping track of each node's parent
            parent[tuple(child_pnck)] = min_node[1]
            if display_children:
                print("Backward Cost:   ", backward_cost)
                if not ucs: print("Forward Cost:    ", forward_cost)
                print("Total Cost:      ", tot_cost)

            ## # if the child is explored and the new cost is worse, skip
            ## if child_pnck in visited and \
            ##    backward_cost >= cost[tuple(child_pnck)]:
            ##     if display_children: print("Ignoring this child..")
            ##     continue
            ## if not child_pnck in visited or \
            ##    backward_cost < cost[tuple(child_pnck)]:
            ##     cost[tuple(child_pnck)] = backward_cost
            ##     forward_cost = 0
            ##     if not ucs: forward_cost = h_func(child_pnck)
            ##     tot_cost = backward_cost + forward_cost
            ##     if display_children:
            ##         print("Backward Cost:   ", backward_cost)
            ##         if not ucs: print("Forward Cost:    ", forward_cost)
            ##         print("Total Cost:      ", tot_cost)

            ##     # adding the child to the frontier to explore in the future
            ##     frontier.push((tot_cost, tuple(child_pnck)))

            ##     # keeping track of each node's parent
            ##     parent[tuple(child_pnck)] = min_node[1]


# The forward cost function for this problem will be defined as the total
# sum of pancakes whose lower neighbor does not differ by more than 1 unit.
def h_func(pnck_list):
    h_val = 0;
    for ind, val in enumerate(pnck_list):
        if ind == 0: continue
        if abs(pnck_list[ind - 1] - val) != 1:
            h_val += 1
#    print()
#    print(".....................Calculating heuristic value...............................")
#    print("List:            ", pnck_list)
#    print("Heuristic value: ", h_val)
#    print("...........................Ending Calculation..................................")
#    print()
    return h_val

# The pancake flip function: it will take in an index and flip the pancake
# stack. :)
def flip(pnck_list, i):
    if i == 0:
        return pnck_list[::-1]
    return pnck_list[:i] + pnck_list[:i-1:-1]

# The backtracking function: it will take in a child node and backtrack,
# printing out all of the intermediate steps it took to get to the current
# position
def print_path(pnck_list, parent):
    path = []
    curr_node = tuple(pnck_list)
    while curr_node != None:
        # print(curr_node)
        path.append(curr_node)
        curr_node = parent[curr_node]
    print("Reconstructed Path: ")
    for ind, node in enumerate(path[::-1]):
        print("Step", ind, ": ", node)

# The check list function: it will take in a list of pancake values, check
# whether the values are valid (contain unique values from 1 to len), and
# return a boolean value
def check_list(pnck_list):
    temp = set()
    for val in pnck_list:
        temp.add(val)
    for i in range(1, len(pnck_list)):
        if not i in temp:
            return False
    return True

if __name__ == "__main__":
    main()
