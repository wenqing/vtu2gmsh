## By Wenqing Wang. 03 Aug 2023
import sys
import pyvista as pyv
import vtk

def main():
    if "--help" in sys.argv:
        print("This script converts VTU file to Gmsh file.")
        print("Usage: python vtu2gmsh.py <input_file> <output_file>")
        return

    if len(sys.argv) != 3:
        print("Usage: python vtu2gmsh.py <input_file> <output_file>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        mesh = pyv.UnstructuredGrid(input_file)
        cell_types = mesh.celltypes
        mat_IDs = mesh.cell_data["MaterialIDs"]

        f = open(output_file, "w")
        f.write('$MeshFormat\n2.2 0 8\n$EndMeshFormat\n$Nodes\n')
        nn = mesh.GetNumberOfPoints()

        #Write nodes

        f.write('%d\n' % nn)
        for i in range(0, nn):
            point = mesh.points[i]
            f.write('%d %g %g %g\n' % (i, point[0], point[1], point[2] ))

        f.write('$EndNodes\n$Elements\n')

        #Write element
        ne = mesh.GetNumberOfCells()
        f.write('%d\n' % ne)

        for i in range(0, ne):
            cell = mesh.GetCell(i)
            cell_type = cell.GetCellType()
            gmsh_element_type = 1
            match cell_type:
                case 3: #LINE
                    gmsh_element_type = 1
                case 5: #TRI
                    gmsh_element_type = 2
                case 9: #QUAD
                    gmsh_element_type = 3
                case 10: #TET
                    gmsh_element_type = 4
                case 12: #HEX
                    gmsh_element_type = 5
                case 13: #PRISM
                    gmsh_element_type = 6
                case 14: #PYRAMID
                    gmsh_element_type = 7
                case _:
                    raise Exception("VTK cell type %d is not supported" % cell_type) 
            mat_id = mat_IDs[i] if len(mat_IDs) > 0 else 0       
            f.write('%d %d 2 %d %d' % (i, gmsh_element_type, mat_id, mat_id))
    
            nne = cell.GetNumberOfPoints()
            for j in range(0, nne):
               f.write(' %d ' % (cell.GetPointId(j)))     
            f.write('\n')

        f.write('$EndElements\n')    
        f.close()
        print('The conversion is successful!')
    except FileNotFoundError:
        print("Error: file %s is not found" % input_file)
    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    main()
        
