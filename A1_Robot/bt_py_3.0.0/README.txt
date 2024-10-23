Acknowledgment:
    CS 131 Slides, Stack Overflow, Google

Implemented:
    The whole behavior tree, with some assumptions.

Assumptions:
    1. When the robot's battery falls below 30, it will navigate back to the
       it's home and start charging. However, I assume that the robot will
       remain on its charging station until it is fully charged (100). If it
       is not fully charged, the task "CHARGE" will remain RUNNING.
    2. The only senor data we need to simulate is the DUSTY_SPOT_SENSOR, and
       in this implementation, the user can either put in a 1 or a 0, or the
       computer will simulate a random value. The other conditionals,
       spot_cleaning and general_cleaning, are assumed to have to be
       pre-configured on the blackboard before the simulation is ran. I also
       maintain the assumption that after successfully spot_cleaning and 
       general_cleaning, the corresponding values will be set to False on the
       blackboard --- meaning that if it is pre-configured to True for either
       conditional, the robot will only perform that cleaning action once, since
       there were no instructions given to simulate/prompt for a value for
       spot_cleaning or general_cleaning.
    3. The priority node assumes that the children are already implemented in
       the order of importance. i.e. node A, B, C are assumed to be ordered by
       importance of the most important, the second most important, and the
       least important, respectively.

Architecture:
    The program follows the architecture pre-defined by the starter code. The bt
    folder contains necessary implementations of each type of composites,
    conditionals, decorators, and tasks. The bt_library contains the declaration
    of important elements used in the program, such as blackboard, behavior
    tree, and tree nodes. The behavior tree is implemented in the robot_behavior
    file in folder bt, which uses tree nodes to build the structure of the tree.
    each tree node is indicative of each node in the reference depiction of the
    behavior tree.

    The main body of the program begins by activating the initial 
    configurations to set up the state of the blackboard. Then, the program will
    start the evaluation cycles of the robot's behavior. At the beginning of
    each evaluation cycle, the robot will prompt the user ask whether or not the
    floor is dirty for the DUSTY_SPOT_SENSOR (1 for yes, 0 for no, other for
    random). Then it will print the state of the blackboard prior to the 
    evaluation, evaluate the behavior tree, and print the state of the 
    blackboard after the evaluation.

    The behavior tree itself is structured the same way as the depiction. Refer 
    to the diagram for details.

    The end condition for the program is when the robot has nothing more to
    clean, or when it reaches the do_nothing state.

Testing:
NOTE: Only the first three elements: batter level, spot cleaning, and general
      cleaning need to be changed for testing all combinations of the robot.
      The program will prompt the user to enter values at the beginning of the
      program to simulate the initial state. The dusty spot sensor is simulated
      as the program runs, and the tester may determine whether it is
      appropriate to trigger the response.
    
    Case 1:
        BATTERY_LEVEL = 0
        SPOT_CLEANING = True
        GENERAL_CLEANING = True
        DUSTY_SPOT_SENSOR = (input 1 on the 34th iteration)
    Expected Behavior:
        - Tests that all of the functionalities run accordingly.
        All of the functionalities - Charge, Spot Cleaning, General
        Cleaning, and Dusty Spot Cleaning. The program should terminate itself 
        after failing the clean floor task and move into do_nothing.
        
        During this period, the dusty spot sensor may pick up more spots to
        clean and may return to dusty spot cleaning. The tester may decide to
        simulate this action.
    
    Case 2:
        BATTERY_LEVEL = 40
        SPOT_CLEANING = True
        GENERAL_CLEANING = False
    Expected Behavior:
        - Tests the first level priority composite
        The robot will have enough battery to move into the spot_cleaning task;
        however, it won't have enough battery to complete it. Therefore, in the
        middle of the task, it will need to charge its battery. After the
        battery charges to full, it will pick up the running task again.

    Case 3:
        BATTERY_LEVEL = 100
        SPOT_CLEANING = False
        GENERAL_CLEANING = False
    Expected Behavior:
        - Tests the end condition
        The robot will terminate after the first iteration (with a small chance
        0.2 chance that the dusty spot sensor picks up something dirty).

Time:
    5 hours