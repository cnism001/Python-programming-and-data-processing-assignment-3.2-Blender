# ReadEsriFile.py -- Open file and read the first lines that contain header

# Print is done in console that can be opened from "Window" menu -> "Toggle System Console". 
# Opening file and printing is done the same way as in any python script or application.

# Open file
# I used QGIS to downsample the file from cellsize 10 to cellsize 40, so instead of 2400x1200 points i have 600x300
esriFile = open("d:\\M5221_resampled.asc")

i = 1
while i < 7:
    # Read and print line
    print(esriFile.readline())
    i += 1
    
# Read and print the first data line
data = esriFile.readline()
# Print the list
print(data)
