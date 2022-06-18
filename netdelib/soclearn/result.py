class RunResult(object):
    def __init__(self, current=None, individual=None, social=None, neighbors=None):
        if (current is not None):
            self.current = current
        if (individual is not None):
            self.individual = individual
        if (social is not None):
            self.social = social
        if (neighbors is not None):
            self.neighbors = neighbors

    def concatenate(self, tail):
        # First element is removed, should be same as last element of current (or None)
        try:
            self.current += tail.current[1:]
        except AttributeError:
            pass
        try:
            self.individual += tail.individual[1:]
        except AttributeError:
            pass
        try:
            self.social += tail.social[1:]
        except AttributeError:
            pass
        try:
            self.neighbors += tail.neighbors[1:]
        except AttributeError:
            pass
        