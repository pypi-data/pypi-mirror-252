import json
import os
from os.path import isdir, join, isfile
from datetime import datetime

metadata_file = "metadata.json"


def getMetaDataFile():
    """
    Return the used name for metadata files in AstecManager

    :returns: name of the file
    """
    return metadata_file


def loadMetaData(embryoPath):
    """
    Using an embryo path , this function load the metadata file corresponding to the embryo , and returns it

    :param embryoPath: string, path to the embryo folder
    :returns: list of dicts , the content of the json metadatas  , or None if it doesn't exist
    """
    if not isdir(embryoPath):
        print(" ! Embryo path not found !")
        return None

    jsonMetaData = join(embryoPath, getMetaDataFile())

    if not isfile(jsonMetaData):
        print(" ! Embryo metadata file not existing !")
        return None

    with open(jsonMetaData, 'r') as openJson:
        jsonObject = json.load(openJson)
    return jsonObject


def createMetaDataFile(embryoPath):
    if not isdir(embryoPath):
        os.makedirs(embryoPath)
    if not isfile(join(embryoPath, getMetaDataFile())):
        with open(isfile(join(embryoPath, getMetaDataFile())), "w+") as outfile:
            json.dump({}, outfile)
            return True
    return False


def writeMetaData(embryoPath, jsonDict):
    """
    Using an embryo path , this function write to the metadata file corresponding to the embryo the json dict

    :param embryoPath: string, path to the embryo folder
    :param jsonDict: dict, data to write (overwrite the content)
    """
    jsonMetaData = join(embryoPath, getMetaDataFile())
    if not isdir(embryoPath) or not isfile(jsonMetaData):
        createMetaDataFile(embryoPath)

    jsonMetaData = join(embryoPath, getMetaDataFile())

    with open(jsonMetaData, 'w') as openJson:
        json.dump(jsonDict, openJson)


def addDictToMetadata(embryoPath, jsonDict, addDate=True):
    """
    Add a dict to the json metadata file

    :param embryoPath: string, path to the embryo folder
    :param jsonDict: dict, dict to add to the metadata
    :param addDate: boolean,  if True, a new key is added to the dict , corresponding to now's date
    :returns: bool , True if the dict was added to the json metadata , False otherwise
    """
    if jsonDict is None:
        print("! Input json dict is None , can not add it to file")
        return False

    if type(jsonDict) is not dict:
        print(" ! input json is not a dictionary ! ")
        return False

    jsonMetadata = loadMetaData(embryoPath)
    if jsonMetadata is None:
        createMetaDataFile(embryoPath)

    if addDate:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        jsonDict["date"] = now
    jsonMetadata.append(jsonDict)
    writeMetaData(embryoPath, jsonMetadata)
