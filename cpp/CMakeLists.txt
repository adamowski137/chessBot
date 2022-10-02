cmake_minimum_required(VERSION 3.4)
set (CMAKE_CXX_STANDARD 11)

project(chess_lib)

include(FetchContent)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY git@github.com:pybind/pybind11.git
)

FetchContent_GetProperties(pybind11)
if(NOT pybind11_POPULATED)
    FetchContent_Populate(pybind11)
    add_subdirectory(${pybind11_SOURCE_DIR} ${pybind11_BINARY_DIR})
endif()

pybind11_add_module(chess_lib src/evaluation.cpp)
target_include_directories(chess_lib PUBLIC include)

