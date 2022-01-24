import os
import sys
import json
from dataloader import loadSample
from dataloader import Config

def main(args):
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

    # pull the sample directory name from the command line arguments, arguement #1
    sampleDirectoryName = args[1]
    
    # build the path to the sample directory 
    sampleDirectoryPath = os.path.join(config.rootSampleDirectory, sampleDirectoryName)

    # load the sample
    loadSample(sampleDirectoryPath, config)
          
if __name__ == "__main__":
    main(sys.argv)
