# look up table loader

from tensor import write_tensor
from tensor import read_tensor
import os
import csv
import math
import numpy as np
import json
from decimal import Decimal #import to use the csv module

# for each entry of the CSV file determine which bin its in
# store the addresses for each file for the bins -> creates lookup table
# then go on to make pBSDF

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

def parseCol(column):
    column = column.replace('{','')
    column = column.replace('}','')
    cell = Cell()
    cell.theta_h = column.rsplit(",", 4)[0]
    cell.phi_h = column.rsplit(",", 4)[1]
    cell.theta_d = column.rsplit(",", 4)[2]
    cell.phi_d = column.rsplit(",", 4)[3]
    return cell

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]

def parseCell(cell):
    # determine which bin this particular cell fits into
    cell.theta_d_bin = round(math.degrees(Decimal(cell.theta_d)))
    cell.phi_d_bin = round(math.degrees(Decimal(cell.phi_d)))
    myArray = []
    for val in range(0,91):
        result = 91*math.sqrt(val/90)
        myArray.append(result)
    cell.theta_h_bin = find_nearest(myArray,math.degrees(Decimal(cell.theta_h)))[0]
    return cell

def parseFiles(filePath):
    # loop over CSV files
    cellData = []
    for subdirs, dirs, files in os.walk(filePath):
        for fileName in files:
            # ignore the .DS_Store files
            if fileName.__contains__(".DS_Store"):
                continue

            # parse file name to get AOI and AOC
            AOI = fileName.rsplit("_", 3)[1]
            AOC = fileName.rsplit("_", 3)[2]
            # RusinkiewiczAngles_10_40.csv.new
            AOC = AOC.rsplit(".",2)[0]
            newFilePath = os.path.join(filePath,fileName)

            # loop over each cell
            # loop over all the elements in the CSV fike
            with open(newFilePath, mode="r") as csv_file: #"r" represents the read mode
                
                reader = csv.reader(csv_file)
                for rowIndex, row in enumerate(reader):
                # you have to loop through the document to get each data
                    for index, column in enumerate(row):
                        print(rowIndex)
                        print(index)
                        cell = parseCol(column)
                        cell.x = rowIndex
                        cell.y = index
                        cell.AOI = AOI
                        cell.AOC = AOC
                        # determine which bin the cell is in
                        parseCell(cell)
                        cellData.append(cell)
                        # store x,y,AOI,AOC in tensor/dictionary in appropriate bin


    with open('cellData.json', 'w') as f:
        json.dump(cellData, f, indent=2)

                        



# create placeholder array [same dimensions as pBSDF] -> functions as the lookup table in the end
# table = read_tensor('/Users/carolinehumphreys/Downloads/6_gold_mitsuba/6_gold_raw.pbsdf')

filePath = "/Users/carolinehumphreys/Desktop/Polarization Lab/data"
parseFiles(filePath)


    # populate with nan orginally
    # TODO: check for nan's at the end, look for two or more entries and delete nan
    # file and x,y exist on the MM level of dictionary
# each cell is a bin
# go to CSV file -> know the AOI and AOC, at an x y coordinate -> take out the angles
# TODO: determine which bin
    # convert to degrees
    # round to the nearest degree for theta_d and phi_d
    # theta_h -> solve equation
    # round theta_h in degrees first and then solve equation to get index
    # use find_nearest function using out array using equation
        # have it return index in the out array
    # gives coordinate in the dictionary -> the rounded values of theta_d, phi_d, theta_h -> bin abc in dictionary
# for the determined bin -> write down file 1, x1 , y1 (give it the specific file of the CSV files and the x and y coordinate) -> store in placeholder array



# TODO: in the future maybe rearrange the dictionary by cmmi file -> load one cmmi file at a time instead of a bunch of cmmi files at a time
    # creates final lookup table

# using moving average when averaging the MM data to put into the dictionary