import timedrel.timedrel_ext_diag as ext
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import io
from PIL import Image
from anytree import Node, RenderTree
from fractions import Fraction
from ppl import Variable, Constraint_System, C_Polyhedron

class diagtree(object):
    """Diagnostics tree for TRE"""
    def __init__(self, time_interval, notation="", children=None):
        if children is None:
            children = []
        self.time_interval = time_interval
        self.notation      = notation
        self.children      = children
    def print(self):
        print(self.notation, self.time_interval)
        for child in self.children:
            child.print()
    def anytree_node(self, parent=None):
        notation = self.notation
        whole_node_label = notation + " <--> [" + self.time_interval[0] + "," + self.time_interval[1] + "]"
        if parent is None:
            whole_node = Node(whole_node_label)
        else:
            whole_node = Node(whole_node_label, parent=parent)
        for child in self.children:
            child_tree_node = child.anytree_node(parent=whole_node)

        return whole_node


class dgzonesetq(object):
    """Python wrapper for dgzone_set C++ class"""

    def __init__(self, zsq, notation="", children=None, op_type="atomic", timing_parameters=None):
        """Initialize the dgzone_set object.

        Args:
            data: Rational zone set from which the dgzone_set will be created.
            notation (str, optional): The notation associated with the dgzone_set.
            children (list, optional): The list of children in the parse tree.
            op_type (str): The type of operator denoted with a string
            timing_parameters [list, optional]: The timing parameters
        """
        if children is None:
            children = []

        # Assuming data is a rational zone_set and a string notation for dgzone_set
        if isinstance(zsq, ext.dgzone_set):
            self.container = zsq
            self.notation = zsq.get_notation()
        else:
            self.container = ext.dgzone_set(zsq.container, notation)
            self.notation = notation

        self.children = children
        self.op_type = op_type
        if timing_parameters is None:
            self.timing_parameters = []
        else:
            self.timing_parameters = timing_parameters

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

    def duration_restriction(self, dmin, dmax, timing_parameters=None):
        """Apply duration restriction on the dgzone_set."""
        dr_container = ext.dgzone_set.duration_restriction(self.container, dmin, dmax)
        return dgzonesetq(dr_container, children=[self], op_type="durarest", timing_parameters=timing_parameters)

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
            return [time_interval, time_interval]
        elif self.op_type == "or":
            return [time_interval, time_interval]
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
            return []

    def create_tree(self, index, time_interval):
        notation = self.notation
        diag_children = []

        child_tintervals = self.infer(index, time_interval)
        child_zindices = self.child_zone_indices(index)
        assert len(child_tintervals) == len(child_zindices)

        if self.op_type == "kplus":
            for czindex, ctinterval in zip(child_zindices, child_tintervals):
                child_tree = self.children[0].create_tree(czindex, ctinterval)
                diag_children.append(child_tree)
        else:
            for czindex, ctinterval, child in zip(child_zindices, child_tintervals, self.children):
                if czindex >= 0:
                    child_tree = child.create_tree(czindex, ctinterval)
                    diag_children.append(child_tree)

        return diagtree(time_interval, notation, diag_children)

    # [TODO]? Can this function be written over the diagtree?
    def infer_parameter_constraints(self, index, time_interval):
        notation = self.notation

        child_tintervals = self.infer(index, time_interval)
        child_zindices = self.child_zone_indices(index)
        assert len(child_tintervals) == len(child_zindices)

        # [TODO]? Using Python Fractions instead of gmp rationals
        # The parameter constraints list to return
        parameter_constraints = []

        if self.op_type == "durarest":
            assert len(self.timing_parameters) <= 2
            assert len(time_interval) == 2
            i = 0
            interval_duration = Fraction(time_interval[1]) - Fraction(time_interval[0])
            duration_numerator = interval_duration.numerator
            duration_denominator = interval_duration.denominator
            if len(self.timing_parameters) == 1:
                parameter = self.timing_parameters[0]
                # This is the lower bound
                constraint = parameter*duration_denominator <= duration_numerator
                parameter_constraints.append(constraint)

                # This is the upper bound
                constraint = duration_numerator <= duration_denominator*parameter
                parameter_constraints.append(constraint)
            elif len(self.timing_parameters) == 2:
                for parameter in self.timing_parameters:
                    if i == 0:
                        # This is the lower bound parameter
                        constraint = parameter*duration_denominator <= duration_numerator
                        parameter_constraints.append(constraint)
                    elif i == 1:
                        # This is the upper bound parameter
                        constraint = duration_numerator <= duration_denominator*parameter
                        parameter_constraints.append(constraint)
                    i += 1

            for czindex, ctinterval, child in zip(child_zindices, child_tintervals, self.children):
                if czindex >= 0:
                    child_parameter_constraints = child.infer_parameter_constraints(czindex, ctinterval)
                    parameter_constraints += child_parameter_constraints
        elif self.op_type == "kplus":
            for czindex, ctinterval in zip(child_zindices, child_tintervals):
                child_parameter_constraints = self.children[0].infer_parameter_constraints(czindex, ctinterval)
                parameter_constraints += child_parameter_constraints
        else:
            for czindex, ctinterval, child in zip(child_zindices, child_tintervals, self.children):
                if czindex >= 0:
                    child_parameter_constraints = child.infer_parameter_constraints(czindex, ctinterval)
                    parameter_constraints += child_parameter_constraints

        return parameter_constraints
