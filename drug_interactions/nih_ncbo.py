import requests
import json
from xml.etree import ElementTree as ET
from pprint import pprint

rxcui = ""
interactions = []

# Get the RxCUI code for a drug of a given name
rx_response = requests.get("https://rxnav.nlm.nih.gov/REST/rxcui?name=haldol")
# print(rx_response.text)
root = ET.fromstring(rx_response.text)

for child in root.find('idGroup'):
    if child.tag == 'rxnormId':
        rxcui = child.text

try:
    url = "https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=" + str(rxcui)
    print(url)

    response = requests.get(url)
    data = json.loads(response.text)
    drugs = data['interactionTypeGroup'][0]['interactionType'][0]['interactionPair']

    for drug in drugs:
        interactions.append({drug['interactionConcept'][1]['sourceConceptItem']['name']: drug['description']})

    print(interactions)
except KeyError:
    print("Could not locate medication by RxCUI. Check spelling")
    pass

# pprint(data['interactionTypeGroup'][0]['interactionType'][0]['interactionPair'])
# print(response.content)
# print(response.json())
