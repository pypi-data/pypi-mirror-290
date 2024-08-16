#include "primitive_sdf.hpp"
#include <pybind11/detail/common.h>
#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace primitive_sdf {

namespace py = pybind11;

void bind_primitive_sdf(py::module& m) {
  auto m_psdf = m.def_submodule("primitive_sdf");
  py::class_<Pose>(m_psdf, "Pose", py::module_local())
      .def(py::init<const Eigen::Vector3d&, const Eigen::Matrix3d&>());

  py::class_<SDFBase, SDFBase::Ptr>(
      m_psdf, "SDFBase",
      py::module_local());  // user is not supposed to instantiate this class.
                            // This to tell pybind that this is a base class
  py::class_<PrimitiveSDFBase, PrimitiveSDFBase::Ptr, SDFBase>(
      m_psdf, "PrimitiveSDFBase",
      py::module_local());  // user is not supposed to instantiate this class.
                            // This to tell pybind that this is a base class
  py::class_<UnionSDF, UnionSDF::Ptr, SDFBase>(m_psdf, "UnionSDF",
                                               py::module_local())
      .def(py::init<std::vector<SDFBase::Ptr>, bool>())
      .def("evaluate_batch", &UnionSDF::evaluate_batch)
      .def("evaluate", &UnionSDF::evaluate);
  py::class_<BoxSDF, BoxSDF::Ptr, PrimitiveSDFBase>(m_psdf, "BoxSDF",
                                                    py::module_local())
      .def(py::init<const Eigen::Vector3d&, const Pose&>())
      .def("evaluate_batch", &BoxSDF::evaluate_batch)
      .def("evaluate", &BoxSDF::evaluate);
  py::class_<CylinderSDF, CylinderSDF::Ptr, PrimitiveSDFBase>(
      m_psdf, "CylinderSDF", py::module_local())
      .def(py::init<double, double, const Pose&>())
      .def("evaluate_batch", &CylinderSDF::evaluate_batch)
      .def("evaluate", &CylinderSDF::evaluate);
  py::class_<SphereSDF, SphereSDF::Ptr, PrimitiveSDFBase>(m_psdf, "SphereSDF",
                                                          py::module_local())
      .def(py::init<double, const Pose&>())
      .def("evaluate_batch", &SphereSDF::evaluate_batch)
      .def("evaluate", &SphereSDF::evaluate);
}
}  // namespace primitive_sdf
