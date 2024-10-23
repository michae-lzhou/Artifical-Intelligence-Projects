#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

# COMP: identify/create all files that need to be made
# TODO: implement priority composite
# TODO: implement sequence composite
# TODO: implement spot_cleaning conditional
# TODO: implement general_cleaning conditional
# TODO: implement dusty_spot conditional
# TODO: implement until_fails decorator
# TODO: implement go_home task
# TODO: implement charge task
# TODO: implement clean_spot task
# TODO: implement done_spot task
# TODO: implement always_fail task
# TODO: implement clean_floor task
# TODO: implement done_general task
# TODO: implement do_nothing task
# TODO: design test cases for each possible condition
# TODO: put everything together


import bt_library as btl
import random

from bt.robot_behavior import robot_behavior
from bt.globals import BATTERY_LEVEL, GENERAL_CLEANING, SPOT_CLEANING, DUSTY_SPOT_SENSOR, HOME_PATH, CHARGING, SHUTDOWN

# Main body of the assignment
current_blackboard = btl.Blackboard()

battery = input("What is the starting battery level? (0-100) ")
spot_cleaning = input("Spot clenaing? (True or False) ")
general_cleaning = input("General cleaning? (True or False) ")

current_blackboard.set_in_environment(BATTERY_LEVEL, int(battery))
current_blackboard.set_in_environment(SPOT_CLEANING, bool(spot_cleaning))
current_blackboard.set_in_environment(GENERAL_CLEANING, bool(general_cleaning))
current_blackboard.set_in_environment(DUSTY_SPOT_SENSOR, False)
current_blackboard.set_in_environment(HOME_PATH, "")
current_blackboard.set_in_environment(CHARGING, False)
current_blackboard.set_in_environment(SHUTDOWN, False)

done = False

while not done:
    # Each cycle in this while-loop is equivalent to 1 second time

    # Step 1: Change the environment
    #   - Change the battery level (charging or depleting)
    battery = current_blackboard.get_in_environment(BATTERY_LEVEL, 100)
    if current_blackboard.get_in_environment(CHARGING, False):
        battery += 10
        if battery > 100: battery = 100
    else:
        battery -= 1
    current_blackboard.set_in_environment(BATTERY_LEVEL, battery)
    # print(battery)

    #   - Simulate the response of the dusty spot sensor
    #   - Simulate user input commands
    # ask for user input here
    dusty = input("Is the current spot dirty? (1: yes, 0: no) ")
    if dusty == '1':
        current_blackboard.set_in_environment(DUSTY_SPOT_SENSOR, True)
        current_blackboard.set_in_environment(GENERAL_CLEANING, True)
    elif dusty == '0':
        current_blackboard.set_in_environment(DUSTY_SPOT_SENSOR, False)
    else:
        chance = random.random()
        # 20% chance that the current spot is dirty
        if chance >= 0.8:
            current_blackboard.set_in_environment(DUSTY_SPOT_SENSOR, True)
            current_blackboard.set_in_environment(GENERAL_CLEANING, True)
        else:
            current_blackboard.set_in_environment(DUSTY_SPOT_SENSOR, False)

    # Step 2: Evaluating the behavior tree

    # Print the state of the tree nodes before the evaluation
    print('BEFORE -------------------------------------------------------------------------')
    btl.print_states(current_blackboard)
    print('================================================================================')

    result = robot_behavior.evaluate(current_blackboard)

    # Print the state of the tree nodes before the evaluation
    print('AFTER --------------------------------------------------------------------------')
    btl.print_states(current_blackboard)
    print('================================================================================')

    # Step 3: Determine if your solution must terminate
    if current_blackboard.get_in_environment(SHUTDOWN, False):
        done = True
