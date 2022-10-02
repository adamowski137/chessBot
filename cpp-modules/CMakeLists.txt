cmake_minimum_required(VERSION 3.4)
set (CMAKE_CXX_STANDARD 11)

project(chess_lib)

include(ExternalProject)
set (EXTERNAL_INSTALL_LOCATION ${CMAKE_BINARY_DIR}/external)

ExternalProject_Add(pybind11
            GIT_REPOSITORY git@github.com:pybind/pybind11.git
            CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${EXTERNAL_INSTALL_LOCATION}
            )

include_directories(${EXTERNAL_INSTALL_LOCATION}/include)
link_directories(${EXTERNAL_INSTALL_LOCATION}/lib)

# add_subdirectory(pybind11)
# pybind11_add_module(cmake_example evaluation.cpp)
# target_compile_definitions(cmake_example
#                            PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})
