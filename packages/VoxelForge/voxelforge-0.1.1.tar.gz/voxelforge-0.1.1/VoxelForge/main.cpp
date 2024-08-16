#include "voxel.h"
#include "octree.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h> 

namespace py = pybind11;

PYBIND11_MODULE(voxelforge_cpp, m) {
    // Bindings for Voxel
    py::class_<Voxel>(m, "Voxel")
        .def(py::init<int, int, int, pybind11::object>(), py::arg("x"), py::arg("y"), py::arg("z"), py::arg("data") = py::int_(1))
        .def_readwrite("x", &Voxel::x)
        .def_readwrite("y", &Voxel::y)
        .def_readwrite("z", &Voxel::z)
        .def_readwrite("data", &Voxel::data)
        .def("getData", &Voxel::getData)
        .def("setData", &Voxel::setData);

    // Bindings for VoxelGrid
    py::class_<VoxelGrid>(m, "VoxelGrid")
        .def(py::init<>())
        .def("addVoxel", &VoxelGrid::addVoxel, py::arg("x"), py::arg("y"), py::arg("z"), py::arg("data") = py::int_(1))
        .def("getVoxels", [](const VoxelGrid &grid) {
            return grid.voxels;
        })
        .def("toGraph", &VoxelGrid::toGraph)
        .def("toList", &VoxelGrid::toList);
    // Bindings for OctreeNode and subclasses
    py::class_<OctreeNode, std::shared_ptr<OctreeNode>>(m, "OctreeNode")
        .def("is_leaf", &OctreeNode::IsLeaf)
        .def("to_json", &OctreeNode::ToJson);  // Bind ToJson for OctreeNode

    py::class_<OctreeLeafNode, OctreeNode, std::shared_ptr<OctreeLeafNode>>(m, "OctreeLeafNode")
        .def(py::init<const Eigen::Vector3d&>())
        .def("get_point", &OctreeLeafNode::GetPoint)
        .def("to_json", &OctreeLeafNode::ToJson);  // Bind ToJson for OctreeLeafNode

    py::class_<OctreeInternalNode, OctreeNode, std::shared_ptr<OctreeInternalNode>>(m, "OctreeInternalNode")
        .def(py::init<>())
        .def("get_child", &OctreeInternalNode::GetChild)
        .def("to_bit_string", &OctreeInternalNode::ToBitString)
        .def("to_json", &OctreeInternalNode::ToJson);  // Bind ToJson for OctreeInternalNode

    py::class_<Octree, std::shared_ptr<Octree>>(m, "Octree")
        .def(py::init<const Eigen::Vector3d&, double, size_t>())
        .def("insert_point", &Octree::InsertPoint)
        .def("locate_leaf_node", &Octree::LocateLeafNode)
        .def("to_bit_string", &Octree::ToBitString)
        .def("to_json", &Octree::ToJson);  // Bind ToJson for Octree
}
