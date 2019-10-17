# def iterativeDeepening(problem, max_depth = 100):
#
#     from util import Stack
#
#     stack = Stack()
#     stack.push((problem.getStartState(), [], []))
#
#     while not stack.isEmpty():
#         current, actions, path = stack.pop()
#
#         if problem.isGoalState(current): return actions
#
#         for successor, direction, cost in problem.getSuccessors(current):
#             if successor not in path and len(path) <= max_depth:
#                 stack.push((successor, actions + [direction], path + [current]))
#

def breadthFirstSearch(problem):

    from util import Queue

    queue = Queue()
    queue.push((problem.getStartState(), [], []))

    while not queue.isEmpty():
        current, actions, path = queue.pop()

        if problem.isGoalState(current): return actions

        for successor, direction, cost in problem.getSuccessors(current):
            if successor not in path:
                queue.push((successor, actions + [direction], path + [current]))
