import requests
from xml.etree import ElementTree as ET
import json

rxcui = ""
response = requests.get("https://rxnav.nlm.nih.gov/REST/rxcui?name=lipitor")
print(response.text)
root = ET.fromstring(response.text)

for child in root.find('idGroup'):
    if child.tag == 'rxnormId':
        rxcui = child.text
print(rxcui)

# for child in root:
#     print(child[1].text)

# for child in root.iterfind('idGroup'):
#     print(child.find('rxnormId').text)