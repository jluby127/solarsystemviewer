# SysView
# utility functions
import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import os

def parseData(filelist):
    """ Parse Data

    Read and parse the relevant data from the Horizons@JPL (https://ssd.jpl.nasa.gov/horizons/app.html#/) curl command

    Args:
        filelist (array of strings): an array where each element is the name of the file pulled from Horizons for the ith planet

    Returns:
        allplanets (list of dictionaries): Each planet gets a dictionary with its relevant information
                                            [RA, DEC, HELRANGE (Sun-Planet distance), EARTHRANGE (Earth-Planet distance)],
                                            and each dictionary is stored in this list.
    """
    allplanets = []

    for f in filelist:
        lines = []
        with open(f+'.csv','r') as dataFile:
            for line in dataFile:
                line = line.strip()
                lines.append(line)
        for i in range(len(lines)):
            if lines[i] == "$$SOE": # The data we are interested in is stored in csv format in the line after this keyword
                data = lines[i+1]
                break

        datastrip = data.split(',')
        dataformatted = []
        for d in datastrip:
            dataformatted.append(d)

        datadict = {"RA":float(dataformatted[3]), "DEC":float(dataformatted[4]), "HELRANGE":float(dataformatted[5]), "EARTHRANGE":float(dataformatted[7])}
        allplanets.append(datadict)

    return allplanets

def gen_ephem_today(yyyy='2022',mm='06',dd='22'):
    '''Ephemeris generator for given date

    Generates the equatorial coordinates and distance to a planet as observed from Earth, and its distance to the Sun.

    Args: 
	yyyy (string): Year in YYYY format
	mm   (string): Month in MM format
	dd   (string): Day in DD format

    Output: 
	list: A list of dictionaries each containing the Julian Date of observation, equatorial coordinates and heliocentric and geocentric distances
    '''
    planets = [199,299,10,499,599,699,799,899]
    files = ['mercury','venus','earth','mars','jupiter','saturn','uranus','neptune']

    date_in = '{}-'.format(int(yyyy))+mm+'-{}'.format(int(dd))
    date_next = '{}-'.format(int(yyyy))+mm+'-{}'.format(int(dd)+1)
    # year_next = '{}-'.format(y+1)+mm+'-{}'.format(d)


    for i in range(8):
        URL_pre = 'https://ssd.jpl.nasa.gov/api/horizons.api?format=text&'
        planet = 'COMMAND=\'{}\'&'.format(planets[i])
        ephem_setting = 'OBJ_DATA=\'YES\'&MAKE_EPHEM=\'YES\'&EPHEM_TYPE=\'OBSERVER\'&'
        obs = 'CENTER=\'50\'&'
        duration='START_TIME=\''+date_in+'\'&STOP_TIME=\''+date_next+'\'&STEP_SIZE=\'1%20d\'&'
        data = 'QUANTITIES=\'2,19,20\'&'
        ang = 'ANG_FORMAT=\'DEG\'&'
        csv_format = 'CSV_FORMAT=\'YES\''
        URL = str(URL_pre+planet+ephem_setting+obs+duration+data+ang+csv_format)
        r = requests.get(url = URL)
        data = r.content
        data = data.decode()
        type(data)
        f = open(files[i]+'.csv','w')
        f.write(data)
        f.close()

    return parseData(files)



PlanetDist = np.array([0.39, 0.72, 1, 1.52, 5.20, 9.58, 19.20, 30.05])
#Define cosine calculation function \n",
def CosCalc(ep, hp):
    """ Cosine Angle Calculation

    Calculate the angle between earth-planet line and sun-planet line using cosine rules.

    Args:
        ep(float): Number. The distance between the earth and the planet.
        hp(float): Number. The distance between the sun and the planet. 
    
    Returns: 
        float: value of angle theta in radian 

    """
    costop = (ep**2-1-hp**2)
    cosbot = 2*hp
    theta = np.arccos(costop/cosbot)
    theta *= (180/np.pi)
    return theta


# def isUP(allplanets):
#     ups = []
#     for i in range(len(allplanets)):
#         print(allplanets[i]['RA'])
#         if i != 2:
#             if abs(allplanets[2]['RA'] - allplanets[i]['RA']) < 90:
#                 ups.append(1)
#             else:
#                 ups.append(0)
#         else:
#             ups.append(0)
#     print("Planets Above Horizon at Midnight: ")
#     names = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
#     for n in range(len(names)):
#         if ups[n] == 1:
#             print(names[n])