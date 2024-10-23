#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# until_fails decorator - Michael Zhou
#

from bt_library.blackboard import Blackboard
from bt_library.common import ResultEnum
from bt_library.decorator import Decorator
from bt_library.tree_node import TreeNode


class UntilFails(Decorator):
    """
    Specific implementation of the until fails decorator.
    """
    TIMER_NOT_IN_USE = -1

    __time: int

    def __init__(self, child: TreeNode):
        """
        Default constructor.

        :param child: Child associated to the decorator
        """
        super().__init__(child)

    def run(self, blackboard: Blackboard) -> ResultEnum:
        """
        Execute the behavior of the node.

        :param blackboard: Blackboard with the current state of the problem
        :return: The result of the execution
        """

        # Evaluate the child
        result_child = self.child.run(blackboard)

        # Only return success until the child fails
        if result_child == ResultEnum.FAILED:
            self.print_message(f"Status = FINISHED")
            return self.report_succeeded(blackboard)
        else: return self.report_running(blackboard)
