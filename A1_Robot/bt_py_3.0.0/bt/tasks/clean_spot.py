#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# clean_spot task - Michael Zhou
#

import bt_library as btl
#from ..globals import HOME_PATH


class CleanSpot(btl.Task):
    """
    Implementation of the Task "Clean Spot"
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:

        self.print_message('Cleaning spot..')

        return self.report_running(blackboard)
