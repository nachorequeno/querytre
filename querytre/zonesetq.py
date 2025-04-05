import timedrel.timedrel_ext_rational as ext

import matplotlib.pyplot as plt

from matplotlib.axes import Axes
from matplotlib.figure import Figure

import io

from PIL import Image

class zoneset(object):
    """docstring for zoneset"""
    def __init__(self, data=None):
        super(zoneset, self).__init__()
        if data == None:
            self.container = ext.zone_set()
        else:
            self.container = data

    def __iter__(self):
        return iter(self.container)

    def __and__(self, other):
        return zoneset.intersection(self, other)

    def __or__(self, other):
        return zoneset.union(self, other)

    def __invert__(self, other):
        return zoneset.complementation(self)

    def __nonzero__(self):
        return not zoneset.empty(self)

    def __ge__(self, other):
        return zoneset.includes(self, other)

    def __le__(self, other):
        return zoneset.includes(other, self)

    def __eq__(self, other):
        return zoneset.includes(self, other) and zoneset.includes(other, self)

    # [TODO] We cannot directly pass rationals from Python to C++
    def add(self, bmin, bmax, emin, emax, dmin, dmax):
        self.container.add(ext.zone.make(ext.geq(bmin), ext.lt(bmax),ext.gt(emin), ext.leq(emax), ext.gt(dmin), ext.leq(dmax)))

    def union(self, other):
        return zoneset.union(self, other)

    def intersect(self, other):
        return zoneset.intersection(self, other)

    def restrict(self, lower, upper):
        return zoneset.duration_restriction(self, lower, upper)

    def concatenate(self, other):
        return zoneset.concatenation(self, other)

    def includes(self, other):
        return ext.includes(self.container, other.container)

    def iterate(self):
        return zoneset.transitive_closure(self)

    def empty(self):
        return self.container.empty()

    @classmethod
    def from_periods(cls, periods, anchor=None):

        zset = zoneset()

        if anchor == None:
            func = zset.container.add_from_period_string
        elif anchor == "rise":
            func = zset.container.add_from_period_rise_anchor_string
        elif anchor == "fall":
            func = zset.container.add_from_period_fall_anchor_string
        elif anchor == "both":
            func = zset.container.add_from_period_both_anchor_string
        elif anchor == "none":
            func = zset.container.add_from_period_both_anchor_string
        else:
            raise Exception(r"Unknown anchor: Options are {none, rise, fall, both}")

        for (begin, end) in periods:
            func(begin, end)

        return zset

    @classmethod
    def from_dataframe(cls, df, predicate, anchor=None):
        def collect(df, predicate):
            def _collect(df, predicate):
                value = False
                for row in df.itertuples():
                    if predicate(row) != value:
                        value = not value
                        yield(row.Index)

                if value:
                    yield(df.iloc[-1].Index)

            value = False
            begin = end = None
            for ts in _collect(df, predicate):
                if value:
                    end = ts
                    yield (begin, end)
                else:
                    begin = ts
                value = not value

        return cls.from_periods(collect(df, predicate), anchor)



    @classmethod
    def union(cls, first, *others):
        result = first.container
        for other in others:
            result = ext.union(result, other.container)

        return zoneset(result)

    @classmethod
    def intersection(cls, first, *others):
        result = first.container
        for other in others:
            result = ext.intersection(result, other.container)

        return zoneset(result)

    # [TODO] We cannot directly pass lower and upper bounds as rationals
    @classmethod
    def duration_restriction(cls, zset, lower, upper):
        return zoneset(ext.duration_restriction(zset.container, lower, upper))

    @classmethod
    def complementation(cls, zset):
        return zoneset(ext.complementation(zset.container))

    @classmethod
    def set_difference(cls, first, second):
        return zoneset(ext.set_difference(first.container, second.container))

    @classmethod
    def concatenation(cls, first, *others):
        result = first.container
        for other in others:
            result = ext.concatenation(result, other.container)

        return zoneset(result)

    @classmethod
    def transitive_closure(cls, zset):
        return zoneset(ext.transitive_closure(zset.container))

    # [TODO] Cannot directly pass lower and upper bounds as rationals
    @classmethod
    def modal_diamond(cls, zset, relation, lower, upper):
        if relation == "meets" or relation == "A":
            return zoneset(ext.diamond_meets(zset.container, lower, upper))
        elif relation == "met_by" or relation == "Ai":
            return zoneset(ext.diamond_met_by(zset.container, lower, upper))
        elif relation == "starts" or relation == "B":
            return zoneset(ext.diamond_starts(zset.container, lower, upper))
        elif relation == "started_by" or relation == "Bi":
            return zoneset(ext.diamond_started_by(zset.container, lower, upper))
        elif relation == "finishes" or relation == "E":
            return zoneset(ext.diamond_finishes(zset.container, lower, upper))
        elif relation == "finished_by" or relation == "Ei":
            return zoneset(ext.diamond_finished_by(zset.container, lower, upper))
        else:
            raise ValueError("Unknown relation")

    # [TODO] Cannot directly pass lower and upper bounds as rationals
    @classmethod
    def modal_box(cls, zset, relation, lower, upper):
        if relation == "meets" or relation == "A":
            return zoneset(ext.box_meets(zset.container, lower, upper))
        elif relation == "met_by" or relation == "Ai":
            return zoneset(ext.box_met_by(zset.container, lower, upper))
        elif relation == "starts" or relation == "B":
            return zoneset(ext.box_starts(zset.container, lower, upper))
        elif relation == "started_by" or relation == "Bi":
            return zoneset(ext.box_started_by(zset.container, lower, upper))
        elif relation == "finishes" or relation == "E":
            return zoneset(ext.box_finishes(zset.container, lower, upper))
        elif relation == "finished_by" or relation == "Ei":
            return zoneset(ext.box_finished_by(zset.container, lower, upper))
        else:
            raise ValueError("Unknown relation")

    def __str__(self):
        return str(self.container)

    def __repr__(self):
        return f"zonesetq({str(self.container)})"

    # [TODO] Cannot directly pass lower and upper bounds as rationals
    def plot_zones(self, fig: Figure = None) -> Axes:
        '''
        Function to plot zones
        '''
        def get_values(zone) -> tuple[int, ...]:
            bminv = zone.bmin().value
            bmaxv = zone.bmax().value
            eminv = zone.emin().value
            emaxv = zone.emax().value
            dminv = zone.dmin().value
            dmaxv = zone.dmax().value
            return (bminv, bmaxv, eminv, emaxv, dminv, dmaxv)

        def get_signs(zone) -> tuple[bool, ...]:
            bmins = zone.bmin().sign
            bmaxs = zone.bmax().sign
            emins = zone.emin().sign
            emaxs = zone.emax().sign
            dmins = zone.dmin().sign
            dmaxs = zone.dmax().sign
            return (bmins, bmaxs, emins, emaxs, dmins, dmaxs)

        def draw_lines(b: float, bp: float, e: float, ep: float, d: float, dp: float, formatos: tuple[int, ...],
                    ax: Axes) -> None:

            # In montre, 0 means strict (b < t), and 1 means not strict (b <= t)
            # Line styles: '--' == 'dashed, '--' == 'solid'
            # line_styles = {0: '--', 1: '-'}
            line_styles = {0: 'dashed', 1: 'solid'}
            styles = [line_styles[fmt] for fmt in formatos]

            xmin, xmax = ax.get_xlim()
            ymin, ymax = ax.get_ylim()

            # Diagonals
            # dp_line = [b + dp, bp + dp]  # Top diagonal
            # d_line = [b + d, bp + d]  # Bottom diagonal
            # x = [b, bp]

            x = [xmin, xmax]
            dp_line = [x[0] + dp, x[1] + dp]  # Top diagonal
            d_line = [x[0] + d, x[1] + d]  # Bottom diagonal

            ax.plot(x, d_line, color='b', linestyle=styles[4])
            ax.plot(x, dp_line, color='b', linestyle=styles[5])

            # Vertical lines
            #ax.vlines(x=b, ymin=min(e, d_line[0]), ymax=max(ep, dp_line[1]), color='r', linestyle=styles[0])
            #ax.vlines(x=bp, ymin=min(e, d_line[0]), ymax=max(ep, dp_line[1]), color='r', linestyle=styles[1])

            ax.vlines(x=b, ymin=ymin, ymax=ymax, color='g', linestyle=styles[0])
            ax.vlines(x=bp, ymin=ymin, ymax=ymax, color='g', linestyle=styles[1])

            # Horizontal lines
            # ax.hlines(y=e, xmin=b, xmax=bp, color='g', linestyle=styles[2])
            # ax.hlines(y=ep, xmin=b, xmax=bp, color='g', linestyle=styles[3])

            ax.hlines(y=e, xmin=xmin, xmax=xmax, color='r', linestyle=styles[2])
            ax.hlines(y=ep, xmin=xmin, xmax=xmax, color='r', linestyle=styles[3])

            # Set axis limits
            # plt.xlim(0, bp + dp)
            # plt.ylim(0, bp + dp)

        def fill_polygon(b: float, bp: float, e: float, ep: float, d: float, dp: float, ax: Axes) -> None:

            # Polygon has, as maximum, six points.
            # Polygon points:
            p1 = (b, e)
            p2 = (b, b + dp)
            p3 = (ep - dp, ep)
            p4 = (bp, ep)
            p5 = (bp, bp + d)
            p6 = (e - d, e)

            # Set of points. Sets are used in order to prevent duplicated points
            lp = [p1, p2, p3, p4, p5, p6]

            xs = [x[0] for x in lp]
            ys = [x[1] for x in lp]

            ax.fill(xs, ys, color='grey')

        def plot_2D(values, signs, fig: Figure = None) -> Axes:
            if fig is None:
                fig = plt.figure()

            ax_list = fig.axes
            if ax_list is None or len(ax_list) == 0:
                ax = fig.add_subplot(111)
            else:
                ax = ax_list[0]

            b, bp, e, ep, d, dp = values
            formats = (int(signs[0]), int(signs[1]), int(signs[2]), int(signs[3]), int(signs[4]), int(signs[5]))

            draw_lines(b, bp, e, ep, d, dp, formats, ax)
            fill_polygon(b, bp, e, ep, d, dp, ax)

            return ax

        if fig is None:
            fig = plt.figure()

        ax_list = fig.axes
        if ax_list is None or len(ax_list) == 0:
            ax = fig.add_subplot(111)
        else:
            ax = ax_list[0]

        zones = self.container

        min_bs = (get_values(zone)[0] for zone in zones)
        max_bs = (get_values(zone)[1] for zone in zones)
        min_es = (get_values(zone)[2] for zone in zones)
        max_es = (get_values(zone)[3] for zone in zones)

        min_x, max_x = min(min_bs), max(max_bs)
        min_y, max_y = min(min_es), max(max_es)
        ax.set_xlim((0, max_x)) # min_x
        ax.set_ylim((0, max_y)) # min_y

        for zone in zones:
            plot_2D(get_values(zone), get_signs(zone), fig=fig)

        return ax

    def display(self):
        # Crear el gráfico y dibujar las zonas
        fig, ax = plt.subplots()
        self.plot_zones(fig)

        # Mostrar el gráfico
        plt.show()

    def get_image(self):
        # Crear el gráfico y dibujar las zonas
        fig, ax = plt.subplots()
        self.plot_zones(fig)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Open the image using Pillow
        image = Image.open(buf)

        return image
