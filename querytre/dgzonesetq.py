import timedrel.timedrel_ext_diag as ext
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import io
from PIL import Image

class dgzone_set(object):
    """Python wrapper for dgzone_set C++ class"""

    def __init__(self, zsq, notation=""):
        """Initialize the dgzone_set object.

        Args:
            data: Rational zone set from which the dgzone_set will be created.
            notation (str, optional): The notation associated with the dgzone_set.
        """

        # Assuming data is a rational zone_set and a string notation for dgzone_set
        self.container = ext.dgzone_set(zsq.container, notation)
        self.notation = notation

    def __and__(self, other):
        """Intersection operator (&) for dgzone_set."""
        return dgzone_set(self.intersection(other))

    def __or__(self, other):
        """Union operator (|) for dgzone_set."""
        return dgzone_set(self.union(other))

    def __concat__(self, other):
        """ Concatenation operator + for dgzone_set"""

    def __str__(self):
        """String representation of the dgzone_set."""
        return str(self.container)

    def get_notation(self):
        """Get the notation of the dgzone_set."""
        return self.container.get_notation()

    def intersection(self, other):
        """Compute the intersection of two dgzone_sets."""
        return ext.dgzone_set.intersection(self.container, other.container)

    def union(self, other):
        """Compute the union of two dgzone_sets."""
        return ext.dgzone_set.set_union(self.container, other.container)

    # TODO return a dgzonesetq rather than the dgzone_set
    def concatenation(self, other):
        """Perform concatenation of two dgzone_sets."""
        return ext.dgzone_set.concatenation(self.container, other.container)

    def kleene_plus(self):
        """Perform Kleene plus operation on the dgzone_set."""
        return ext.dgzone_set.kleene_plus(self.container)

    def duration_restriction(self, dmin, dmax):
        """Apply duration restriction on the dgzone_set."""
        return ext.dgzone_set.duration_restriction(self.container, dmin, dmax)

    # def infer_concatenation(self, index, dg1, dg2, time_interval):
    #     """Infer concatenation for a dgzone_set."""
    #     return ext.dgzone_set.infer_concatenation(self.container, index, dg1.container, dg2.container, time_interval)

    # def infer_kleene_plus(self, index, dg1, time_interval):
    #     """Infer Kleene plus for a dgzone_set."""
    #     return ext.dgzone_set.infer_kleene_plus(self.container, index, dg1.container, time_interval)
