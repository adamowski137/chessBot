#include <pybind11/pybind11.h>

#include <iostream>
#include <stdio.h>

// https://pybind11.readthedocs.io/en/stable/index.html

namespace py = pybind11;

/// Minimal example, prints squares that contain pieces
void evaluate(py::dict board) {
  for (const auto &piece : board) {
    int key;
    key = piece.first.cast<int>();
    std::cout << key << std::endl;
  }
}

PYBIND11_MODULE(chess_lib, m) {
  m.doc() = "Static Evaluation for a chess board.";
  m.def("evaluate", &evaluate);
}
