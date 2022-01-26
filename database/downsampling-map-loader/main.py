import os
import sys
import json
from dataloader import loadSample
from dataloader import Config

def main():
    # load the configuration
    scriptDir = os.path.dirname(__file__)
    configPath = os.path.join(scriptDir, 'config.json')

    with open(configPath, "r") as json_data_file:
        jsonData = json.load(json_data_file)

    # get the directory where the CMMI files are stored
    config = Config()
    config.rootSampleDirectory = jsonData["rootSampleDirectory"]
    config.hostName = jsonData["hostName"]
    config.userName = jsonData["userName"] 
    config.userPassword = jsonData["userPassword"]
    config.dbName = jsonData["dbName"]


    # TODO: create another table that table that holds the degree increments or do the math in the python script
    # TODO: loop over scattering_geometry_pixel_map table to select specific pixels

    # loop over all of the sample folders in the input directory
    # for sampleDirectoryName in os.listdir(config.rootSampleDirectory):
    #     # build the path to the sample directory 
    #     sampleDirectoryPath = os.path.join(config.rootSampleDirectory, sampleDirectoryName)

    #     # load the sample
    #     loadSample(sampleDirectoryPath, config)
          
if __name__ == "__main__":
    main()
