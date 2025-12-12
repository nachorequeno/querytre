#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <gmpxx.h>
#include <gmp.h>

#include "bound.hpp"
#include "zone.hpp"
#include "zone_set.hpp"
#include "utils.hpp"
#include "indexed_zone.hpp"
#include "dgzone_set.hpp"

namespace py = pybind11;

using T = mpq_class;

PYBIND11_MODULE(timedrel_ext_diag, m) {
    m.doc() = "timedrel diagnostics plugin called diagnotre"; // optional module docstring

    using namespace timedrel;

    typedef dgzone_set<T> dgzone_set_type;

    py::class_<dgzone_set_type>(m, "dgzone_set")
        .def(py::init<const zone_set<T>&, std::string>(), py::arg("zs"), py::arg("notation"))
        .def("get_notation", &dgzone_set_type::get_notation)
        .def("get_zvec", &dgzone_set_type::get_zvec)
        .def_static("concatenation", &dgzone_set_type::concatenation)
        .def_static("kleene_plus", &dgzone_set_type::kleene_plus)
        .def_static("intersection", &dgzone_set_type::intersection)
        .def_static("set_union", &dgzone_set_type::set_union)
        .def_static("duration_restriction", &dgzone_set_type::duration_restriction)
        .def_static("infer_concatenation", &dgzone_set_type::infer_concatenation)
        .def_static("infer_kleene_plus", &dgzone_set_type::infer_kleene_plus)
        .def("__str__", [](const dgzone_set_type &self) {
            std::ostringstream os;
            os << self;
            return os.str();
        })
    ;
}