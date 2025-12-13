import timedrel.timedrel_ext_diag as ext
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import io
from PIL import Image

class dgzonesetq(object):
    """Python wrapper for dgzone_set C++ class"""

    def __init__(self, zsq, notation="", children=[], op_type="atomic"):
        """Initialize the dgzone_set object.

        Args:
            data: Rational zone set from which the dgzone_set will be created.
            notation (str, optional): The notation associated with the dgzone_set.
            children (list, optional): The list of children in the parse tree.
        """

        # Assuming data is a rational zone_set and a string notation for dgzone_set
        if isinstance(zsq, ext.dgzone_set):
            self.container = zsq
            self.notation = zsq.get_notation()
        else:
            self.container = ext.dgzone_set(zsq.container, notation)
            self.notation = notation

        self.children = children
        self.op_type = op_type

    def __and__(self, other):
        """Intersection operator (&) for dgzone_set."""
        return dgzonesetq(self.intersection(other), children=[self, other], op_type="and")

    def __or__(self, other):
        """Union operator (|) for dgzone_set."""
        return dgzonesetq(self.union(other), children=[self, other], op_type="or")

    def __add__(self, other):
        """ Concatenation operator + for dgzone_set"""
        return dgzonesetq(self.concatenation(other), children=[self, other], op_type="concat")

    def __str__(self):
        """String representation of the dgzone_set."""
        retstr = self.op_type+"\n"
        retstr += str(self.children)+"\n"
        retstr += str(self.container)
        retstr += self.notation

        return retstr

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
        kplus_container = ext.dgzone_set.kleene_plus(self.container)
        return dgzonesetq(kplus_container, children=[self], op_type="kplus")

    def duration_restriction(self, dmin, dmax):
        """Apply duration restriction on the dgzone_set."""
        dr_container = ext.dgzone_set.duration_restriction(self.container, dmin, dmax)
        return dgzonesetq(dr_container, children=[self], op_type="durarest")

    def infer_concatenation(self, index, dg1, dg2, time_interval):
        """Infer concatenation for a dgzone_set."""
        return ext.dgzone_set.infer_concatenation(self.container, index, dg1.container, dg2.container, time_interval)

    def infer_kleene_plus(self, index, dg1, time_interval):
        """Infer Kleene plus for a dgzone_set."""
        return ext.dgzone_set.infer_kleene_plus(self.container, index, dg1.container, time_interval)

    def child_zone_indices(self, index):
        return self.container.child_zone_indices(index)

    def infer(self, index, time_interval):
        if self.op_type == "and":
            return [time_interval]
        elif self.op_type == "or":
            return [time_interval]
        elif self.op_type == "concat":
            assert len(self.children) == 2
            child1 = self.children[0]
            child2 = self.children[1]
            return self.infer_concatenation(index, child1, child2, time_interval)
        elif self.op_type == "kplus":
            assert len(self.children) == 1
            child = self.children[0]
            return self.infer_kleene_plus(index, child, time_interval)
        elif self.op_type == "durarest":
            return [time_interval]
        elif self.op_type == "atomic":
            return [time_interval]
