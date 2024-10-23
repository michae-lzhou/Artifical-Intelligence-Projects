#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# done_spot task - Michael Zhou
#

import bt_library as btl
from ..globals import SPOT_CLEANING


class DoneSpot(btl.Task):
    """
    Implementation of the Task "Done Spot"
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:

        self.print_message('Done cleaning spot.')

        blackboard.set_in_environment(SPOT_CLEANING, False)

        return self.report_succeeded(blackboard)
