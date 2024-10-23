#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# go_home task - Michael Zhou
#

import bt_library as btl
from ..globals import HOME_PATH


class GoHome(btl.Task):
    """
    Implementation of the Task "Go Home".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:

        self.print_message('Going home')
        path = blackboard.get_in_environment(HOME_PATH, "")
        self.print_message(path)

        return self.report_succeeded(blackboard)
