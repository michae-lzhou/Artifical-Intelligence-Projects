#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt as bt
import bt_library as btl

# Instantiate the tree according to the assignment. The following are just examples.

sequence_check_battery = bt.Sequence(
    [
        bt.BatteryLessThan30(),
        bt.FindHome(),
        bt.GoHome(),
        bt.Charge()
    ]
)

sequence_spot_cleaning = bt.Sequence(
    [
        bt.SpotCleaning(),
        bt.Timer(20, bt.CleanSpot()),
        bt.DoneSpot()
    ]
)

sequence_dusty = bt.Sequence(
    [
        bt.DustySpot(),
        bt.Timer(35, bt.CleanSpot()),
        bt.AlwaysFail()
    ]
)

priority_dusty_clean = bt.Priority(
    [
        sequence_dusty,
        bt.UntilFails(bt.CleanFloor())
    ]
)

sequence_priority_dusty = bt.Sequence(
    [
        priority_dusty_clean,
        bt.DoneGeneral()
    ]
)

sequence_general_cleaning = bt.Sequence(
    [
        bt.GeneralCleaning(),
        sequence_priority_dusty
    ]
)

selection_cleaning = bt.Selection(
    [
        sequence_spot_cleaning,
        sequence_general_cleaning
    ]
)

do_nothing = bt.DoNothing()

tree_root = bt.Priority(
    [
        sequence_check_battery,
        selection_cleaning,
        do_nothing
    ]
)


# Example 1:
# tree_root = bt.Timer(5, bt.FindHome())

# Example 2:
# tree_root = bt.Selection(
#     [
#         BatteryLessThan30(),
#         FindHome()
#     ]
# )

# Example 3:
# tree_root = bt.Selection(
#     [
#         bt.BatteryLessThan30(),
#         bt.Timer(10, bt.FindHome())
#     ]
# )

# Store the root node in a behavior tree instance
robot_behavior = btl.BehaviorTree(tree_root)
