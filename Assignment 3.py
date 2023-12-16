#commented in VSCode, uncommented in Blender
#import bpy
#import bmesh


# I used QGIS to warp the file from cellsize 10 to cellsize 40, so instead of 2400x1200 points i have 600x300
# Function to read elevation data from the  file

def read_file(file_path):
    with open("file_path", 'r') as file:
        # Read header lines containing metadata
        #.split()[1]) is expected to grab numerical value of ncols from file, so 600 here, same logic for the rest of the header reader
        ncols = int(file.readline().split()[1])  # Number of columns in the grid, 
        nrows = int(file.readline().split()[1])  # Number of rows in the grid
        xllcorner = float(file.readline().split()[1])  # X-coordinate of the lower-left corner
        yllcorner = float(file.readline().split()[1])  # Y-coordinate of the lower-left corner
        cellsize = float(file.readline().split()[1])  # Size of each cell (pixel),should be 40 after warping the file with QGIS
        NODATA_value = float(file.readline().split()[1])  # Value indicating no data

        # Read the elevation data as a list of lists (2D array)
        heights = [list(map(float, line.split())) for line in file]

    return heights, ncols, nrows, xllcorner, yllcorner, cellsize

# Path to the .asc file
file_path = 'd:\\M5221_resampled.asc'

# Reading the elevation data from the file
heights, ncols, nrows, xllcorner, yllcorner, cellsize = read_file(file_path)

# Create a new bmesh object
bm = bmesh.new()

# Create a list to store references to the vertices created below
verts = []

# Iterate over each row and column in the elevation data
for row_index, row in enumerate(heights):
    #elevation value give in the file is z
    for col_index, z in enumerate(row):
        # Calculate the x and y coordinates based on the grid position and cell size
        x = xllcorner + col_index * cellsize
        y = yllcorner + row_index * cellsize

        # Create a new vertex at the calculated position with the elevation as the z-coordinate in the mesh bm
        vert = bm.verts.new((x, y, z))
        # Add the vertex to the list
        verts.append(vert)

# Update the bmesh's internal vertex index table, to ensure that vertices can be accessed properly by their index
bm.verts.ensure_lookup_table() 

# Create faces by connecting adjacent vertices
for row_index in range(nrows - 1): #-1 used because last row and collumn cant form a quad since they wont have enough adjacents
    for col_index in range(ncols - 1):
        # Define the four vertices of the current quad
        v1 = verts[row_index * ncols + col_index]
        #v2 is to the right of v1, hence col_index+1
        v2 = verts[row_index * ncols + (col_index + 1)]
        #v3 is to right and down from v1, hence both row_index+1 and col_index+1
        v3 = verts[(row_index + 1) * ncols + (col_index + 1)]
        #v4 is down from v1 hence row_index+1
        v4 = verts[(row_index + 1) * ncols + col_index]

        # Create a new face using these vertices
        bm.faces.new((v1, v2, v3, v4))

# Create a new Blender mesh object
mesh = bpy.data.meshes.new("TerrainElevation")

# Create a new Blender object that uses the mesh data
obj = bpy.data.objects.new("TerrainElevationObj", mesh)

# Link the object to the active collection in the scene to visualize it
bpy.context.collection.objects.link(obj)

