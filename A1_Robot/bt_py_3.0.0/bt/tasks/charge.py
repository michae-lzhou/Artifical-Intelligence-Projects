#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# charge task - Michael Zhou
#

import bt_library as btl
from ..globals import BATTERY_LEVEL, CHARGING


class Charge(btl.Task):
    """
    Implementation of the Task "Charge".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Charging')

        blackboard.set_in_environment(CHARGING, True)
        
        if blackboard.get_in_environment(BATTERY_LEVEL, 100) < 100:
            return self.report_running(blackboard)

        blackboard.set_in_environment(CHARGING, False)
        return self.report_succeeded(blackboard)
