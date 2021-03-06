# Query the database and have result exported as CSV
# Querying  by phi_d, theta_h, theta_d, material, wavelength

import os
import json
import sys
import csv
from database import Config
from database import createDBConnection
from database import readQuery

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

    # create DB connection
    connection = createDBConnection(config.hostName,config.userName,config.userPassword,config.dbName)

    # pull the lower bound for phi_d from the command line arguements, arguement #1
    lower_phi_d = args[1]

    # pull the upper bound for phi_d from the command line arguements, arguements #2
    upper_phi_d = args[2]

    # pull the lower bound for theta_d from the command line arguements, arguement #1
    lower_theta_d = args[5]

    # pull the upper bound for theta_d from the command line arguements, arguements #2
    upper_theta_d = args[6]

    # pull the lower bound for theta_h from the command line arguements, arguement #1
    lower_theta_h = args[3]

    # pull the upper bound for theta_h from the command line arguements, arguements #2
    upper_theta_h = args[4]
    
    # pull the material name from the command line arguments, arguement #1
    materialName = args[10]

    # pull the wavelength from the command line arguments, arguments #2
    wavelength = args[8]

    # pull the AOI from the command line arguments, arguments #3
    AOI = args[7]

    # pull the AOC from the command line arguments, arguments #4
    AOC = args[8]

    query = """SELECT m00, m01, m02, m03, m10, m20, m30, m11, m12, m13, m21, m22, m23, m31, m32, m33, cpd.AOI, cpd.AOC
                FROM cmmi_pixel_data as cpd
                INNER JOIN mm_samples as mm ON cpd.sample_no = mm.sample_no AND cpd.AOI = mm.AOI AND cpd.AOC = mm.AOC
                INNER JOIN material_samples as m ON m.sample_no = cpd.sample_no
                INNER JOIN scattering_geometry_pixel_map as sgpm ON cpd.pixel_x = sgpm.pixel_x AND cpd.pixel_y = sgpm.pixel_y AND cpd.AOI = sgpm.AOI AND cpd.AOC = sgpm.AOC
                WHERE sgpm.phi_d BETWEEN  %s AND %s
                AND sgpm.theta_h BETWEEN %s and %s
                AND sgpm.theta_d BETWEEN %s and %s
                AND sgpm.AOI = %s 
                AND sgpm.AOC = %s
                AND material_name = %s;"""
    data = (lower_phi_d,upper_phi_d,lower_theta_h,upper_theta_h,lower_theta_d,upper_theta_d,AOI,AOC,materialName)
    result = readQuery(connection, query,data)

    # loop over result and write to file
    with open("out2.csv", "w", newline='') as csv_file:  # Python 3 version    
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(result)
          
if __name__ == "__main__":
    main(sys.argv)

# Query with all inner joins
# SELECT m00, m01, m02, m03, m10, m20, m30, m11, m12, m13, m21, m22, m23, m31, m32, m33
# FROM cmmi_pixel_data as cpd
# INNER JOIN mm_samples as mm ON cpd.sample_no = mm.sample_no 
# AND cpd.AOI = mm.AOI 
# AND cpd.AOC = mm.AOC
# AND cpd.wavelength = mm.wavelength
# INNER JOIN material_samples as m ON m.sample_no = cpd.sample_no
# INNER JOIN scattering_geometry_pixel_map as sgpm ON cpd.pixel_x = sgpm.pixel_x 
# AND cpd.pixel_y = sgpm.pixel_y 
# AND cpd.AOI = sgpm.AOI 
# AND cpd.AOC = sgpm.AOC
# WHERE material_name = %s AND cpd.AOI = %s AND cpd.AOC = %s AND cpd.wavelength = %s;

# extra SQL query statements
# SELECT mm_samples.date, mm_samples.exposure
#                 FROM mm_samples
#                 INNER JOIN material_samples
#                 ON mm_samples.sample_no = material_samples.sample_no
#                 WHERE material_samples.material_name = %s AND mm_samples.wavelength = %s