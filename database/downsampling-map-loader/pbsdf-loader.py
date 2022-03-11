# read json into an array of cell objects
# load sample
# loop over cmmi files
    # query the array of cell objects

class Cell:
    theta_h = 0
    phi_h = 0
    theta_d = 0
    phi_d = 0
    theta_d_bin = 0
    theta_h_bin = 0
    phi_d_bin = 0
    x = 0
    y = 0
    AOI = 0
    AOC = 0


def loadCellData(cellFilePath):
    # todo
    cellData = []
    return cellData


# load the cell data
cellFilePath = ""
cellData = loadCellData(cellFilePath)

# loop over bins
# for each bin you have a specific files
    # for each file you have a specific x, y pixel location
    # at that pixel location you take the MM
    # average all the MMs for that specific bin
 

cellDataresult = [cell for cell in cellData if cell.x == mm and cell.y == mm and cell.AOI == fileAOI and cell.AOC == fileALOC]
    