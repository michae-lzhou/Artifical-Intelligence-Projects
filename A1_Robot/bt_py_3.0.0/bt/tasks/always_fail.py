#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# always fail task - Michael Zhou
#

import bt_library as btl
from ..globals import BATTERY_LEVEL, CHARGING


class AlwaysFail(btl.Task):
    """
    Implementation of the Task "Always Fail".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Always Fail')

        return self.report_failed(blackboard)
