import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np
import pandas
from shutil import copyfile
import parameter_file
from subprocess import call


melt_temperature = 0
space_dims = 2
nodes_per_cell = pow(2, space_dims)  # This doesn't consider hanging nodes
temperature = -1
material = {'name': 'water-ice', 'melting temperature': 0}


def solve_pde(state):
    # Prepare input file for PDE solver
    copyfile(parameter_file.reference_path, parameter_file.run_input_path)
    parameter_file.set_state(state)
    # Run the PDE solver
    call(['../PDE/dimice-heat', parameter_file.run_input_path])
    # Read the solution
    solution_file_path = 'solution.0.10.vtk'
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(solution_file_path)
    reader.Update()
    nodes = vtk_to_numpy(reader.GetOutput().GetPoints().GetData())
    u = vtk_to_numpy(reader.GetOutput().GetPointData().GetArray(0))
    # Clean up the data
    data = np.column_stack((nodes[:, 0], nodes[:, 1], u))
    table = pandas.DataFrame(data=data)
    table = table.drop_duplicates()
    data = table.as_matrix()
    return data


def test():
    state = (0., 0., 0.)
    data = solve_pde(state)
    print(data)

if __name__ == "__main__":
    test()
