import json
#import pycountry
import urllib.request as urllib
import urllib
import re
import jellyfish as jel


entityExampleName = []
syno = []
mydata = []
saved = []
recentGenericNames = ["null"]
savedGenericNames = []
savedBrandNames = []
savedOtherNames = []


############################################
## Drug names json file imported
##########################################

f = open('rrr.json')
thisFile = json.loads(f.read())

############################################
## Going through the json file and extract generic,brand and other names
##########################################

num = len(thisFile["results"])
for j in range(num):
    print(j)
    savedGenericNames = []
    savedBrandNames = []
    savedOtherNames = []
    
    if 'generic_name' in thisFile["results"][j]:
        sepList = thisFile["results"][j]['generic_name']
        sepList = re.split(r',|^and$| and|/| - ', sepList)
        for k in range(len(sepList)):
            if len(sepList[k]) > 1 and len(sepList[k])<64:
                if sepList[k].lower() not in savedGenericNames:
                    savedGenericNames.append(sepList[k].lower())

    if 'brand_name' in thisFile["results"][j]:
        sepList = thisFile["results"][j]['brand_name']
        sepList = re.split(r',|^and$| and ', sepList)
        for k in range(len(sepList)):
            if sepList[k].lower() not in savedBrandNames and sepList[k] != '' and len(sepList[k]) < 64:
                savedBrandNames.append(sepList[k].lower())

    if 'active_ingredients' in thisFile["results"][j]:
        for i in range(len(thisFile["results"][j]["active_ingredients"])):
            sepList =thisFile["results"][j]["active_ingredients"][i]['name']
            sepList = re.split(r',|^and$| and ', sepList)
        for k in range(len(sepList)):
            if sepList[k].lower() not in savedOtherNames and sepList[k] != '' and len(sepList[k]) < 64:
                savedOtherNames.append(sepList[k].lower())


    if savedGenericNames not in recentGenericNames:
        saved.append([{"generic":savedGenericNames,"brand":savedBrandNames,"other":savedOtherNames}])
    recentGenericNames.append(savedGenericNames)

def returnMap():
    return saved

