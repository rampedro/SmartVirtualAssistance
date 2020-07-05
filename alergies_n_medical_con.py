import http.client
import mimetypes
import json




conn = http.client.HTTPSConnection("secure.advcare.info")
payload = "{\"action\":\"allglist\", \"tokenid\":\"Lk20Q52k02lKds2W3kdsfp2Ro3okf04D\", \"user\":\"apptester1\",\"pass\":\"123456\",\"limit\":\"1000\",\"from\":\"1\"}\r\n\r\n\r\n\r\n\r\n\r\n"
headers = {
  'Content-Type': 'application/json',
  'Cookie': 'PHPSESSID=tjdefna4ka4i6afefmesg11kq4'
}
conn.request("POST", "/mobapp/v1.1/adv/", payload, headers)
res = conn.getresponse()
data = res.read()

decoded_data = data.decode("utf-8")
responseObjectAllergy = json.loads(data)


AllergyNames = []

#print(responseObject['data'])

for item in responseObjectAllergy['data']:
    AllergyNames.append(item['NAME'])
    #print(item['NAME'])


####################################



payload = "{\"action\":\"medconlist\", \"tokenid\":\"Lk20Q52k02lKds2W3kdsfp2Ro3okf04D\", \"user\":\"apptester1\",\"pass\":\"123456\",\"limit\":\"1000\",\"from\":\"1\"}\r\n\r\n\r\n\r\n\r\n\r\n"
headers = {
  'Content-Type': 'application/json',
  'Cookie': 'PHPSESSID=tjdefna4ka4i6afefmesg11kq4'
}
conn.request("POST", "/mobapp/v1.1/adv/", payload, headers)
res = conn.getresponse()
data = res.read()

decoded_data = data.decode("utf-8")
responseObjectConditions = json.loads(data)



conditionsNames = []

#print(responseObjectConditions)

for item in responseObjectConditions['data']:
    conditionsNames.append(item['NAME'])
    print(item['NAME'])


####################################






