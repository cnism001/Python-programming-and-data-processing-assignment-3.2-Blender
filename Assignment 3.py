# ReadEsriFile.py -- Open file and read the first lines that contain header

# Print is done in console that can be opened from "Window" menu -> "Toggle System Console". 
# Opening file and printing is done the same way as in any python script or application.



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