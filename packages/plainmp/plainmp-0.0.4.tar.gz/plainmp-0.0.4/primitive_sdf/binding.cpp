#include <pybind11/detail/common.h>
#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "primitive_sdf.hpp"
namespace py = pybind11;

namespace primitive_sdf {

PYBIND11_MODULE(_psdf, m) {
  m.doc() = "Primitive SDF module";
  py::class_<Pose>(m, "Pose").def(
      py::init<const Eigen::Vector3d&, const Eigen::Matrix3d&>());
  py::class_<AABB>(m, "AABB")
      .def_readonly("lb", &AABB::lb)
      .def_readonly("ub", &AABB::ub);
  py::class_<SDFBase, SDFBase::Ptr>(
      m, "SDFBase");  // user is not supposed to instantiate this class. This to
                      // tell pybind that this is a base class
  py::class_<UnionSDF, UnionSDF::Ptr, SDFBase>(m, "UnionSDF")
      .def(py::init<std::vector<SDFBase::Ptr>, bool>())
      .def("evaluate_batch", &UnionSDF::evaluate_batch)
      .def("evaluate", &UnionSDF::evaluate)
      .def("get_aabb", &UnionSDF::get_aabb)
      .def("is_outside", &UnionSDF::is_outside);
  py::class_<BoxSDF, BoxSDF::Ptr, SDFBase>(m, "BoxSDF")
      .def(py::init<const Eigen::Vector3d&, const Pose&>())
      .def("evaluate_batch", &BoxSDF::evaluate_batch)
      .def("evaluate", &BoxSDF::evaluate)
      .def("get_aabb", &BoxSDF::get_aabb)
      .def("is_outside", &BoxSDF::is_outside);
  py::class_<CylinderSDF, CylinderSDF::Ptr, SDFBase>(m, "CylinderSDF")
      .def(py::init<double, double, const Pose&>())
      .def("evaluate_batch", &CylinderSDF::evaluate_batch)
      .def("evaluate", &CylinderSDF::evaluate)
      .def("get_aabb", &CylinderSDF::get_aabb)
      .def("is_outside", &CylinderSDF::is_outside);
  py::class_<SphereSDF, SphereSDF::Ptr, SDFBase>(m, "SphereSDF")
      .def(py::init<double, const Pose&>())
      .def("evaluate_batch", &SphereSDF::evaluate_batch)
      .def("evaluate", &SphereSDF::evaluate)
      .def("get_aabb", &SphereSDF::get_aabb)
      .def("is_outside", &SphereSDF::is_outside);
}

}  // namespace primitive_sdf
