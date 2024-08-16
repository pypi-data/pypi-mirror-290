#include <pybind11/pybind11.h>
#include "constraint_binding.hpp"
#include "third/primitive_sdf_binding.hpp"
#include "third/tinyfk_binding.hpp"

#ifdef USE_VALGRIND
#include <valgrind/callgrind.h>
#endif

namespace py = pybind11;

void start_profiling() {
#ifdef USE_VALGRIND
  CALLGRIND_START_INSTRUMENTATION;
#else
  throw std::runtime_error(
      "Valgrind is not enabled. Please recompile with -DUSE_VALGRIND=ON");
#endif
}

void stop_profiling() {
#ifdef USE_VALGRIND
  CALLGRIND_STOP_INSTRUMENTATION;
#endif
}

PYBIND11_MODULE(_plainmp, m) {
  primitive_sdf::bind_primitive_sdf(m);
  cst::bind_collision_constraints(m);
  tinyfk::bind_tinyfk(m);
  m.def("start_profiling", &start_profiling);
  m.def("stop_profiling", &stop_profiling);
}
