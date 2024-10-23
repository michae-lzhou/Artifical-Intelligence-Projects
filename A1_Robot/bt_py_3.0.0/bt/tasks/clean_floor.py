#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# clean_floor task - Michael Zhou
#

import bt_library as btl
import random
#from ..globals import HOME_PATH


class CleanFloor(btl.Task):
    """
    Implementation of the Task "Clean Floor"
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:

        self.print_message('Cleaning floor..')

        # small chance that it fails
        print(random.random())
        if random.random() > 0.8:
            return self.report_failed(blackboard)
        else:
            return self.report_running(blackboard)
