from pypy.module._stackless import interp_coroutine
from pypy.module._stackless.interp_clonable import ClonableCoroutine, fork
import os

class ChoicePointHolder(object):
    def __init__(self):
        self.choicepoints = []

    def next_choice(self):
        return self.choicepoints.pop()

    def choice(self):
        os.write(1, "choice\n")
        child = fork()
        if child is not None:
            self.choicepoints.append(child)
            return 0
        else:
            return 1
    
    def add(self, choice):
        self.choicepoints.append(choice)

    def more_choices(self):
        return bool(self.choicepoints)

choicepoints = ChoicePointHolder()

invalid_branches = [
    [0, 0, 0],
    [0, 0, 1],
    [0, 1],
    [1, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 1],
    [1, 0, 1],
    [1, 1, 0, 0],
    ]

class SearchTask(interp_coroutine.AbstractThunk):
    def call(self):
        try:
            path = []
            for i in range(10):
                path = path[:]
                path = path + [choicepoints.choice()]
                for invalid_branch in invalid_branches:
                    if len(path) < len(invalid_branches):
                        continue
                    for i in range(len(invalid_branch)):
                        if path[i] != invalid_branch[i]:
                            break
                    else:
                        return
            os.write(1, "found a solution!: ")
            os.write(1, "[" + ", ".join([str(i) for i in path]) + "]\n")
        except Exception, e:
            os.write(1, "exception raised :-(")

# ^ ^ ^ that's quite cool code I think :-)
# yes, I agree :-)
# much easier than doing it by hand


def search_all(argv):
    search_coro = ClonableCoroutine()
    search_coro.bind(SearchTask())
    choicepoints.add(search_coro)

    os.write(1, "starting\n")
    while choicepoints.more_choices():
        searcher = choicepoints.next_choice()
        searcher.switch()
    return 0

def target(*args):
    return search_all, None
