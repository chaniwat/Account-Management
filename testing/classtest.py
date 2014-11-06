class Point:
    """Represents a point in 2-D space."""
    def __init__(self, x, y):
        """initiate variables (x, y)"""
        self.x = float(x)
        self.y = float(y)

    def length(self):
        """return vector length between (0, 0) to (x, y)"""
        return "%.2f" % (((self.x**2)+(self.y**2))**0.5)

    def sum(self):
        """return sum of (x, y)"""
        return "%.2f" % abs(self.x + self.y)

    def delta(self):
        """return delta of (x, y)"""
        return "%.2f" % abs(self.x - self.y)

point = Point(3, 4)
length = point.length()
sumpoint = point.sum()
deltapoint = point.delta()

print length
print sumpoint
print deltapoint