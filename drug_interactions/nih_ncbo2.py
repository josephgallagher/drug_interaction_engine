import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
from xml.etree import ElementTree as ET
from pprint import pprint


medications = []
rxcui_list = []
interactions = []


# Read in the file of medications
medication_csv = pd.read_csv('drugs.csv')
for med in medication_csv:
    medications.append(med.strip())


# Get the RxCUI code(s) for drug of a given name
for med in medications:
    rx_response = requests.get("https://rxnav.nlm.nih.gov/REST/rxcui?name=" + med)
    # print(rx_response.text)
    root = ET.fromstring(rx_response.text)

    for child in root.find('idGroup'):
        if child.tag == 'rxnormId':
            rxcui_list.append(child.text)
print(rxcui_list)


try:
    url = "https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis=" + '+'.join(rxcui_list)
    print(url)

    response = requests.get(url)
    data = json.loads(response.text)
    drugs = data['fullInteractionTypeGroup'][0]['fullInteractionType']
    for index, item in enumerate(drugs):
        print(drugs[index]['interactionPair'][0])

    # for drug in drugs:
    #     interactions.append({drug['interactionConcept'][1]['sourceConceptItem']['name']: drug['description']})
    #
    # print(interactions)
except KeyError:
    print("Could not locate medication by RxCUI. Check spelling")
    pass

# pprint(data['interactionTypeGroup'][0]['interactionType'][0]['interactionPair'])
# print(response.content)
# print(response.json())
