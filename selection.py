class Selection:
    def __init__(self, start, end=None):
        self.start = start
        self.end = end

    def __str__(self):
        string = str(self.start)
        if self.end:
            string += F", {self.end}"
        return string

    def __eq__(self, other):
        """
        Determines if `self` and `other` are equivalent.
        :param other: a Selection
        :return: a bool
        """
        if not other:
            return False

        return {self.start, self.end} == {other.start, other.end}

    @classmethod
    def from_array(cls, array):
        cls(array[0], array[len(array) - 1])

