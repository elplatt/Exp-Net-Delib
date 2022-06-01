class RunResult(object):
	def __init__(self, current=None, individual=None, social=None):
		if (current):
			self.current = current
		if (individual):
			self.individual = individual
		if (social):
			self.social = social

	def concatenate(self, tail):
		# First element is removed, should be same as last element of current (or None)
		if (self.current):
			self.current += tail.current[1:]
		if (self.individual):
			self.individual += tail.individual[1:]
		if (self.social):
			self.social += tail.social[1:]

		