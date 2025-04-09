#include <pybind11/pybind11.h>
#include <gmpxx.h>
#include <gmp.h>

#include "bound.hpp"
#include "zone.hpp"
#include "zone_set.hpp"
#include "utils.hpp"

namespace py = pybind11;

using T = mpq_class;

PYBIND11_MODULE(timedrel_ext_rational, m) {
    m.doc() = "timedrel rationals plugin"; // optional module docstring

    using namespace timedrel;

    typedef lower_bound<T> lower_bound_type;
    typedef upper_bound<T> upper_bound_type;

    py::class_<lower_bound_type>(m, "lower_bound")
        .def(py::init<T, bool>())
        .def_readonly("value", &lower_bound_type::value)
        .def_readonly("sign", &lower_bound_type::sign)
    ;

    m.def("lt", &upper_bound_type::strict);
    m.def("leq", &upper_bound_type::nonstrict);

    py::class_<upper_bound_type>(m, "upper_bound")
        .def(py::init<T, bool>())
        .def_readonly("value", &upper_bound_type::value)
        .def_readonly("sign", &upper_bound_type::sign)
    ;

    m.def("gt", &lower_bound_type::strict);
    m.def("geq", &lower_bound_type::nonstrict);

    typedef zone<T> zone_type;
    typedef zone_set<T> zone_set_type;

    py::class_<zone_type>(m, "zone")
        .def("bmin", &zone_type::get_bmin)
        .def("bmax", &zone_type::get_bmax)
        .def("emin", &zone_type::get_emin)
        .def("emax", &zone_type::get_emax)
        .def("dmin", &zone_type::get_dmin)
        .def("dmax", &zone_type::get_dmax)

        .def<zone_type (*)(
            const lower_bound_type&, const upper_bound_type&,
            const lower_bound_type&, const upper_bound_type&,
            const lower_bound_type&, const upper_bound_type&)>
        ("make", &zone_type::make)
    ;

    py::class_<zone_set_type>(m, "zone_set")
        .def(py::init<>())
        .def<void (zone_set_type::*)(const zone_type&)>("add", &zone_set_type::add)
        .def<void (zone_set_type::*)(const std::array<T, 6>&)>("add", &zone_set_type::add)
        .def<void (zone_set_type::*)(const std::array<T, 6>&, const std::array<bool, 6>&)>("add", &zone_set_type::add)
        .def("get_as_python_float", &zone_set_type::get_as_double) // Python float is C++ double
        .def("add_from_period", &zone_set_type::add_from_period)
        .def("add_from_period_rise_anchor", &zone_set_type::add_from_period_rise_anchor)
        .def("add_from_period_fall_anchor", &zone_set_type::add_from_period_fall_anchor)
        .def("add_from_period_both_anchor", &zone_set_type::add_from_period_both_anchor)
        .def("add_from_period_string", &zone_set_type::add_from_period_string)
        .def("add_from_period_rise_anchor_string", &zone_set_type::add_from_period_rise_anchor_string)
        .def("add_from_period_fall_anchor_string", &zone_set_type::add_from_period_fall_anchor_string)
        .def("add_from_period_both_anchor_string", &zone_set_type::add_from_period_both_anchor_string)
        .def("empty", &zone_set_type::empty)
        .def("__iter__", [](const zone_set_type &s) { return py::make_iterator(s.cbegin(), s.cend()); },
                         py::keep_alive<0, 1>() /* Essential: keep object alive while iterator exists */)
        .def("__str__", &zone_set_type::toString)
    ;

    m.def("filter", &zone_set_type::filter);
    m.def("includes", &zone_set_type::includes);

    // Set operations
    m.def<zone_set_type (*)(const zone_set_type&)>("complementation", &zone_set_type::complementation);
    m.def<zone_set_type (*)(const zone_set_type&, const std::string &, const std::string &)>("duration_restriction", &zone_set_type::duration_restriction_string);
    m.def<zone_set_type (*)(const zone_set_type&, const zone_set_type&)>("union", &zone_set_type::set_union);
    m.def<zone_set_type (*)(const zone_set_type&, const zone_set_type&)>("intersection", &zone_set_type::intersection);
    m.def<zone_set_type (*)(const zone_set_type&, const zone_set_type&)>("difference", &zone_set_type::set_difference);

    // Sequential operations
    m.def<zone_set_type (*)(const zone_set_type&, const zone_set_type&)>("concatenation", &zone_set_type::concatenation);
    m.def<zone_set_type (*)(const zone_set_type&)>("transitive_closure", &zone_set_type::transitive_closure);

    // Modal operations of the logic of time periods
    m.def<zone_set_type (*)(const zone_set_type&, const std::string&, const std::string&)>("diamond_starts", &zone_set_type::diamond_starts_string);
    m.def<zone_set_type (*)(const zone_set_type&, const std::string&, const std::string&)>("diamond_started_by", &zone_set_type::diamond_started_by_string);
    m.def<zone_set_type (*)(const zone_set_type&, const std::string&, const std::string&)>("diamond_finishes", &zone_set_type::diamond_finishes_string);
    m.def<zone_set_type (*)(const zone_set_type&, const std::string&, const std::string&)>("diamond_finished_by", &zone_set_type::diamond_finished_by_string);
    m.def<zone_set_type (*)(const zone_set_type&, const std::string&, const std::string&)>("diamond_meets", &zone_set_type::diamond_meets_string);
    m.def<zone_set_type (*)(const zone_set_type&, const std::string&, const std::string&)>("diamond_met_by", &zone_set_type::diamond_met_by_string);
    m.def<zone_set_type (*)(const zone_set_type&, const std::string&, const std::string&)>("box_starts", &zone_set_type::box_starts_string);
    m.def<zone_set_type (*)(const zone_set_type&, const std::string&, const std::string&)>("box_started_by", &zone_set_type::box_started_by_string);
    m.def<zone_set_type (*)(const zone_set_type&, const std::string&, const std::string&)>("box_finishes", &zone_set_type::box_finishes_string);
    m.def<zone_set_type (*)(const zone_set_type&, const std::string&, const std::string&)>("box_finished_by", &zone_set_type::box_finished_by_string);
    m.def<zone_set_type (*)(const zone_set_type&, const std::string&, const std::string&)>("box_meets", &zone_set_type::box_meets_string);
    m.def<zone_set_type (*)(const zone_set_type&, const std::string&, const std::string&)>("box_met_by", &zone_set_type::box_met_by_string);
}