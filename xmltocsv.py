#!venv/bin/python

import xml.etree.ElementTree as ET
import os
import pandas as pd
import pathlib
import argparse
import csv
import os

def xmlParse(location_input, location_output, tag, attribute):
    count = 1
    temp_list = []
    with open(location_output, 'w', newline='') as file:
        writer = csv.writer(file)
        if tag and not attribute:
            writer.writerow([tag])
            for event, elem in ET.iterparse(location_input):
                if elem.tag == tag:
                    value = elem.text
                    if value not in temp_list:
                        os.system('clear')
                        print(count)
                        count += 1
                        temp_list.append(value)
                        writer.writerow([value])
                elem.clear()

        elif attribute and not tag:
            writer.writerow([attribute])
            for event, elem in ET.iterparse(location_input):
                value = elem.attrib.get(attribute)
                if value and (value not in temp_list):
                    os.system('clear')
                    print(count)
                    count += 1
                    temp_list.append(value)
                    writer.writerow([value])
                elem.clear()
        else:
            writer.writerow([f'{tag}:{attribute}'])
            for event, elem in ET.iterparse(location_input):
                value = elem.attrib.get(attribute)
                if elem.tag == tag and value and (value not in temp_list):
                    os.system('clear')
                    print(count)
                    count += 1
                    temp_list.append(value)
                    writer.writerow([value])
                elem.clear()
    file.close()

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
    parser.add_argument('-o', '--output', required=True,
                        help="CSV Output File Location")
    parser.add_argument('-f', '--full', default=False, help="Full Conversion (Only works on small-sized XML files)")
    parser.add_argument('-t', '--tag', default=False, help="Specify Tag")
    parser.add_argument('-a', '--attribute', default=False, help="Specify Attribute")

    args = parser.parse_args()

    location_input = args.input
    location_output = args.output
    tag = args.tag
    attribute = args.attribute

    if not location_input.lower().endswith('.xml'):
        location_input += '.xml'
    if '/' not in location_input:
        location_input = f'{path}/{location_input}'

    if not location_output.endswith('.csv'):
        location_output += '.csv'
    if '/' not in location_output:
        location_output = f'{path}/{location_output}'

    if args.full:
        xmlToCSV(location_input, location_output)
    else:
        xmlParse(location_input, location_output, tag, attribute)
