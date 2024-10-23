#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# dusty_spot conditional - Michael Zhou
#

import bt_library as btl
from ..globals import DUSTY_SPOT_SENSOR


class DustySpot(btl.Condition):
    """
    Implementation of the condition "dusty spot cleaning".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Checking if the spot is dusty')

        return self.report_succeeded(blackboard) \
            if blackboard.get_in_environment(DUSTY_SPOT_SENSOR, True) \
            else self.report_failed(blackboard)
