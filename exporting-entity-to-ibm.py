import json
from ibm_cloud_sdk_core.authenticators.authenticator import Authenticator
#from common import get_sdk_headers
from datetime import datetime
from enum import Enum
from ibm_cloud_sdk_core import BaseService
from ibm_cloud_sdk_core import DetailedResponse
from ibm_cloud_sdk_core import datetime_to_string, string_to_datetime
from ibm_cloud_sdk_core.get_authenticator import get_authenticator_from_environment
from typing import Dict
from typing import List
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from assistant_v1 import AssistantV1
from assistant_v1 import CreateEntity
from assistant_v1 import CreateValue
from populating import returnMap



############################################
## Setting up the authentication
##########################################


authenticator = IAMAuthenticator('bZnob8FwfXfB7XRB1qG-11fW_Ai608DlBa8QmcTCQy48')

myService = AssistantV1(
    version='2020-06-16',
    authenticator=authenticator)

############################################
## Adding new entity with its values and synonyms to work space
##########################################
# all is needed is to create an array of dictionary that look like this arr = [{'value': str },{'otherName1':list[srt]},{'otherName2':list[str]} and then add the value to the value parameter of CreateValue and add up otherName1 and otherName2 and pass it to parameter synonyms of CreateValue

# This can write up better for later versions


drug=[]
myValue = []
names = returnMap()
used = []
otherNames = []
newValue = []
for j in names:
    if len(j[0]['brand']) >= 1 or len(j[0]['other']) >=1:
        otherNames = j[0]['brand'] + j[0]['other']
    otherNames = list(set(otherNames))
    if (len(j[0]['generic']) >= 1) and j[0]['generic'][0].lower() not in used :
        used.append(j[0]['generic'][0].lower())
        drug.append([j[0]['generic'][0],otherNames])



for i in drug:
    newValue += [CreateValue(value=i[0],synonyms=i[1])] #synonyms take list of strigns


newEntity = [CreateEntity(entity="drugs",values=newValue)] #value takes list of CreateValue


workSpace = myService.get_workspace("05ef9fdd-6848-4471-bea4-fb09d49ca9fd")

updating_workSapce = myService.update_workspace("05ef9fdd-6848-4471-bea4-fb09d49ca9fd",entities=newEntity, append=True)




###########################################
## (FYI) adding to a specific entity 
###########################################


if False:

    drug=[]
    myValue = []
    names = returnMap()
    used = []
    otherNames = []
    for j in names:
        if len(j[0]['brand']) >= 1 or len(j[0]['other']) >=1:
            otherNames = j[0]['brand'] + j[0]['other']
        otherNames = list(set(otherNames))
        if (len(j[0]['generic']) >= 1) and j[0]['generic'][0].lower() not in used :
            used.append(j[0]['generic'][0].lower())
            drug.append([j[0]['generic'][0],otherNames])

    for p in range(len(drug)):
        print(drug[p])



synonyms = []
count = 0


if False:
    for i in drug:
        if (len(i[1]) < 1):
            synonyms = None
        else:
            synonyms = i[1]

        myValue.append(myService.create_value(workspace_id="05ef9fdd-6848-4471-bea4-fb09d49ca9fd",entity="drugs",value=i[0],synonyms=synonyms))
        count += 1

    print("Number of drgus added",count)
    myService.update_entity(workspace_id="05ef9fdd-6848-4471-bea4-fb09d49ca9fd",entity='drugs',new_values=myValue)


print("======Exported=======")
