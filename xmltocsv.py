import xml.etree.ElementTree as ET
import os
import pandas as pd
import pathlib
import argparse

def parseData(element, temp_dict):
    if len(list(element)) != 0:
        for child in element:
            parseData(child, temp_dict)
    else:
        if element.tag not in temp_dict.keys():
            temp_dict[element.tag] = [element.text]
        else:
            temp_dict[element.tag].append(element.text)
    return temp_dict

def xmlToCSV(location_input, location_output):
    tree = ET.parse(location_input)
    root = tree.getroot()
    temp_dict = {}
    data = parseData(root, temp_dict)
    df = pd.DataFrame.from_dict(data, orient='index').T
    df.to_csv(location_output, index=False)

if __name__ == "__main__":
    path = str(pathlib.Path(__file__).parent.absolute())

    # Specified the CLI Parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True,
                        help="XML File Location")
    parser.add_argument('-o', '--output', default=False,
                        help="CSV Output File Location")
    args = parser.parse_args()
    
    location_input = args.input
    location_output = args.output

    if not location_input.lower().endswith('.xml'):
        location_input += '.xml'
    if '/' not in location_input:
        location_input = f'{path}/{location_input}'

    if not location_output.endswith('.csv'):
        location_output += '.csv'
    if '/' not in location_output:
        location_output = f'{path}/{location_output}'

    xmlToCSV(location_input, location_output)
