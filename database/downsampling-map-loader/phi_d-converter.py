#*****
# TODO: make sure phi_d gets shifted to 0-2pi in CSV files
    # import file
    # check all phi_d values
    # if negative add 2pi
    # re-export and to the same file location so it replaces it
#*****

import csv
from decimal import Decimal #import to use the csv module
import os
from sys import path_importer_cache

# open CSV file
filePath = "/Users/carolinehumphreys/Desktop/Polarization Lab/data"

class Cell:
    theta_h = 0
    phi_h = 0
    theta_d = 0
    phi_d = 0

# parse the CSV file
def parse(fileName,newCoordinateFile):
    with open(fileName, mode="r") as csv_file: #"r" represents the read mode
        reader = csv.reader(csv_file) #this is the reader object

        # loop over all the elements in the CSV fike
        for rowIndex, row in enumerate(reader):
            # you have to loop through the document to get each data
                for index, column in enumerate(row):
                    print(rowIndex)
                    print(index)
                    cell = parseColumn(column)
                    cellString = createCellString(cell)
                    newCoordinateFile.write(cellString)
                    #print(cell)# index is added to get a particular column
                    if index < len(row)-1:
                        newCoordinateFile.write(",")
                    else:
                        newCoordinateFile.write("\n")
                    


# parse the each column
def parseColumn(column):
    column = column.replace('{','')
    column = column.replace('}','')
    theta_h = column.rsplit(",", 4)[0]
    phi_h = column.rsplit(",", 4)[1]
    theta_d = column.rsplit(",", 4)[2]
    phi_d = column.rsplit(",", 4)[3]
    cell = Cell()
    if theta_h.__contains__("*^-"):
        cell.theta_h = "0"
    else:
        if theta_h.__contains__("Indeterminate"):
            cell.theta_h = "nan"
        else:
            cell.theta_h = Decimal(theta_h)

    if phi_h.__contains__("Indeterminate"):
        cell.phi_h = "nan"
    else:
        cell.phi_h = Decimal(phi_h)

    if theta_d.__contains__("Indeterminate"):
        cell.theta_d = "nan"
    else:
        cell.theta_d = Decimal(theta_d)

    if phi_d.__contains__("Indeterminate"):
        cell.phi_d = "nan"
    else:
        cell.phi_d = Decimal(phi_d)
        if cell.phi_d < 0:
            cell.phi_d = cell.phi_d + Decimal(6.2831853072)

    return cell

def createCellString(cell):
    cellString = f'"{{{cell.theta_h},{cell.phi_h},{cell.theta_d},{cell.phi_d}}}"'
    return cellString

# loop over path
for subdirs, dirs, files in os.walk(filePath):
        for fileName in files:
            if fileName.__contains__(".DS_Store"):
                continue
            print(fileName)
            coordinateFilePath = os.path.join(filePath,fileName)
            newFileName = f'{fileName}.new'
            newCoordinateFilePath = os.path.join(filePath,newFileName)
            newCoordinateFile = open(newCoordinateFilePath, "w")
            parse(coordinateFilePath,newCoordinateFile)
            newCoordinateFile.close()
            

