#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# do_nothing task - Michael Zhou
#

import bt_library as btl
from ..globals import SHUTDOWN

class DoNothing(btl.Task):
    """
    Implementation of the Task "Do Nothing".
    """
    # do nothing


    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Doing nothing, exiting program')

        blackboard.set_in_environment(SHUTDOWN, True) 

        return self.report_succeeded(blackboard)
