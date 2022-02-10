import math

class TimeSeriesResult (object):
    
    def __init__ (self):
        # Exact value of the result
        self.value = []

        # Number of samples
        self.counts = []

        # Total of all sample results and squares
        self.totals = []
        self.squares = []

    def add_sample (self, t, v):
        """Add sample v at time t"""
        # Increment count
        try:
            self.counts[t] += 1
        except IndexError:
            self.counts.append(1)
        # Add sample value to total
        try:
            self.totals[t] += v
        except IndexError:
            self.totals.append(v)
        # Add square of sample to sum of squares
        try:
            self.squares[t] += v * v
        except IndexError:
            self.squares.append(v * v)
            
    def add_y (self, v):
        self.value.append(v)
    
    def y (self):
        """Return exact values"""
        return self.value
    
    def mean (self):
        """Calculate mean values"""
        return [self.totals[i] / self.counts[i] for i in range(len(self.totals))]
    
    def var (self):
        """Calculate variance values"""
        m = self.mean()
        n = len(m)
        return [(self.squares[i] - m[i] * m[i]) / self.counts[i] for i in range(n)]
    
    def se (self):
        """Calculate the standard error values"""
        v = self.var()
        n = len(v)
        return [v[i] / math.sqrt(self.counts[i]) for i in range(n)]
    
    def yerr95(self):
        """Calculate 95% confidence intervals"""
        return [sei * 1.96 for sei in self.se()]