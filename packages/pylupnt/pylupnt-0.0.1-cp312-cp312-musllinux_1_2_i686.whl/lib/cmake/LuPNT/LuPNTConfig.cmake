include(CMakeFindDependencyMacro)

string(REGEX MATCHALL "[^;]+" SEPARATE_DEPENDENCIES "fmt 7.1.3;Eigen3 3.4;autodiff 1.1;cspice;Matplot++ 1.2;OpenMP")

foreach(dependency ${SEPARATE_DEPENDENCIES})
  string(REPLACE " " ";" args "${dependency}")
  find_dependency(${args})
endforeach()

include("${CMAKE_CURRENT_LIST_DIR}/LuPNTTargets.cmake")
