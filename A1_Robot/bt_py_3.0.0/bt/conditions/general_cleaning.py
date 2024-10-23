#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# general_cleaning conditional - Michael Zhou
#

import bt_library as btl
from ..globals import GENERAL_CLEANING


class GeneralCleaning(btl.Condition):
    """
    Implementation of the condition "general cleaning".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Checking if general-cleaning')

        return self.report_succeeded(blackboard) \
            if blackboard.get_in_environment(GENERAL_CLEANING, False) \
            else self.report_failed(blackboard)
