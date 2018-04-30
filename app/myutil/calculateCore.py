__author__ = 'FrankZ'
import time
"""This is for calculating the speedlevel for grab the information frequently"""

class calculateCore(object):
    def __init__(self):
        pass

    # according to the speedlevel to getAsinByCalculate determine
    def getAsinByCalculate(resultFromDB):
        AsinList = list()
        for item in resultFromDB:
            level = item[2]
            if level == "A":
                gaptime = (time.time() - int(item[3]))/86400
                if gaptime > 1:
                    AsinList.append(item[0])
            if level == "B":
                gaptime = (time.time() - int(item[3])) / 86400
                if gaptime > 3:
                    AsinList.append(item[0])
            if level == "C":
                gaptime = (time.time() - int(item[3])) / 86400
                if gaptime > 5:
                    AsinList.append(item[0])
            if level == "D":
                gaptime = (time.time() - int(item[3])) / 86400
                if gaptime > 3:
                    AsinList.append(item[0])
        return AsinList
    # convert level to time
    def levelCalculate(self,level,time):
        pass






