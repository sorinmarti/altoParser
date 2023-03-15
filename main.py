import os
import re

from alto_parser import AltoFileParser

class MyAltoFileParser(AltoFileParser):
    def __init__(self, filename):
        super().__init__(filename)

    def clean_data(self, data):
        for key in data:
            if data[key] is not None and isinstance(data[key], str):
                data[key] = data[key].strip().strip(",").strip('\n').strip('\r').strip('\t')

                if key == 'company':
                    company_ending_list = ['Ltd.', 'Co.', 'S. A.', 'S.A.', 'S.A.']
                    has_company_ending = False
                    for item in company_ending_list:
                        if data[key].endswith(item):
                            has_company_ending = True
                            break
                    if not has_company_ending:
                        data[key] = data[key].strip('.')
                if key == 'goods':
                    data[key] = data[key].lstrip('(').rstrip(')')


# Read the locations from locations_parser.csv file
def readcsv(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]

# Dictionaries
locations = readcsv('data/locations_parser.csv')
locations_extended = [locations[i] + "." for i in range(len(locations))]
personal_titles = ["Esq."]
address = ["Castle Mills", "Trafalgar", "Trafalgar Square", "Imperial Buildings", "Cambridge Street"]
titles = readcsv('data/titles.csv')

def parsing_function(text, words):
    # print("Structuring line: " + text)

    result = {'transcription': text}

    # Check each word against the list locations_parser.csv
    for word in words:
        if word in locations:
            result["location_found"] = True
            result["location"] = word

    # Check each word against the list my_locations_extended list
    for word in words:
        if word in locations_extended:
            result["location_extended_found"] = True
            result["location_extended"] = word

    # Check each line against a regex for Title
    match = re.search(r'^(\w{1,20} ?(\w{1,10})) (\(\w*[^.]\))$|^\w{1,20}$|^\w{1,10} \w{1,10}$|^\w{1,10} \w{1,10} \w{1,15}$|^\w{1,10} \(\w{1,10}, .{1,25}\)$', text)
    if match:
        result["title_found"] = True
        result["title"] = match.group(0)

    # Check each line against a regex for Company
    match = re.search(r'(^.{1,30} ? (Frères|Brothers|Co\.|& Co\.,|Ltd\.|& Cie.,|S\. A\.,|A\.-G\.,|A\. G\.) ?(S. A.)?|^[A-Z]. [A-Z]. \w{1,10}|^[A-Z][a-z]{1,3}\. \w{1,10}-?\w{1,10}|^\w{1,10} & \w{1,10}|^[A-Z]. \w{1,10}|.{1,100} Co\.)', text)
    if match:
        result["company_found"] = True
        result["company"] = match.group(0)


    # Check each line against a regex for Goods in brackets
    match = re.search(r'(\(.{1,150}\),)', text)
    if match:
        result["goods_found"] = True
        result["goods"] = match.group(0)

    # Check each line against a regex for Address
    match = re.search(r'((([0-9]{1,4})\/?—??—?\/?[0-9]{1,4}, [A-Z].[^,]{1,20},)|S. W. [0-9].)', text)
    if match:
        result["address_found"] = True
        result["address"] = match.group(0)

    return result


if __name__ == "__main__":
    # Open the data folder and create a AltoFileParser object for each file in the folder.
    # The AltoParser object will parse the file and store the results in a list of dictionaries.
    for file in os.listdir('data/'):
        if file.endswith(".xml") or file.endswith(".alto"):
            print("Parsing file: " + file)
            parser = MyAltoFileParser('data/' + file)
            parser.parse_file(parsing_function)
            for line in range(parser.get_number_of_lines()):
                parser.print_line_summary(line)
                pass

            csv_filename = file.split('.')[0] + '.csv'
            parser.save_csv_file("./" + csv_filename)
            print("Done parsing file: " + file)

