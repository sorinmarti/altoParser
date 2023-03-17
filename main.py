import csv
import os
import re

from alto_parser import AltoFileParser

class MyAltoFileParser(AltoFileParser):
    def __init__(self, filename, meta_data):
        super().__init__(filename, meta_data)

    def clean_data(self, data):
        if data is None:
            return

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
locations = readcsv('meta/locations_parser.csv')
locations_extended = [locations[i] + "." for i in range(len(locations))]
personal_titles = ["Esq.", "C.B.", "C.V. O."]
address = ["Castle Mills", "Trafalgar", "Trafalgar Square", "Imperial Buildings", "Cambridge Street"]
names = ["FALCONER EVANS CROWE", "MAURICE GALLAND", "0ALEXANDER RICHARDSON", "THEO. RUSSELL"]
titles = readcsv('meta/titles.csv')

def parsing_function(text, words, meta_data):

    if meta_data['range_definition'] == 'board_member':
        return parse_board_member_page(text, words)

    elif meta_data['range_definition'] == 'alphabetical':
        return parse_alphabetical_index_page(text, words)

    elif meta_data['range_definition'] == 'new_member':
        return parse_new_member_page(text, words)

    elif meta_data['range_definition'] == 'index':
        return parse_index_page(text, words)

    else:
        print("Unknown range_definition: " + meta_data['range_definition'])
        return {}


def parse_board_member_page(text, words):

    result = {'transcription': text}

    # Check each line against a regex for name
    match = re.search(r'(^[A-Z]\. ([A-Z]\.)? ?\w{1,100}|^[A-Z]{1,10} [A-Z]{1,10})', text)
    if match:
        result["name_found"] = True
        result["name"] = match.group(0)

    # Check each line against a regex for Title
    match = re.search(r'(Officers and Members of the Board|Active Members of the Board|Corresponding Members of the Board|Hon. Members of the Board)', text)
    if match:
        result["title_found"] = True
        result["title"] = match.group(0)

    # Check each word against the list locations_parser.csv
    for word in words:
        if word in locations:
            result["location_found"] = True
            result["location"] = word

    # Check each word against the list personal_titles
    for word in text:
        if word in personal_titles:
            result["personal_title_found"] = True
            result["personal_title"] = word

    # Check each line against a regex for function
    match = re.search(r'(Hon\. President|Hon\. Vice-President|President|Hon\. Treasurer|Vice-President|Secretary-General, Head Office|Hon\. Secretary, Lausanne Branch)', text)
    if match:
        result["function_found"] = True
        result["function"] = match.group(0)

    # Check each line against a regex for Profession
    match = re.search(r'(H\. B\. M\. Minister|Treasurer Provincial Foreign Bank Ltd\.|H\. B\. M\. Consul-General|H\. B\. M\. Consul)', text)
    if match:
        result["profession_found"] = True
        result["profession"] = match.group(0)

    # Check each word against the list names
    for word in words:
        if word in names:
            result["name_found"] = True
            result["name"] = word


    return result

def parse_new_member_page(text, words):
    return {}

def parse_index_page(text, words):

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
    """match = re.search(
        r'^(\w{1,20} ?(\w{1,10})) (\(\w*[^.]\))$|^\w{1,20}$|^\w{1,10} \w{1,10}$|^\w{1,10} \w{1,10} \w{1,15}$|^\w{1,10} \(\w{1,10}, .{1,25}\)$',
        text)
    if match:
        result["title_found"] = True
        result["title"] = match.group(0)

    # Check each line against the list titles
    for text in words:
        if text in titles:
            result["title_found"] = True
            result["title"] = word"""

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

    # Check each line against a regex for Company
    match = re.search(
        r'(^.{1,30} ? (Frères|Brothers|Co\.|& Co\.,|Ltd\.|& Cie.,|S\. A\.,|A\.-G\.,|A\. G\.) ?(S. A.)?|^[A-Z]. [A-Z]. \w{1,10}|^[A-Z][a-z]{1,3}\. \w{1,10}-?\w{1,10}|^\w{1,10} & \w{1,10}|^[A-Z]. \w{1,10}|.{1,100} Co\.)',
        text)
    if match:
        result["company_found"] = True
        result["company"] = match.group(0)

    return result

def parse_alphabetical_index_page(text, words):
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

    # Check each line against a regex for Company with & Co. etc
    match = re.search(
        r'(^.{1,30} ? (Frères|Brothers|Co\.|& Co\.,|Ltd\.|& Cie.,|S\. A\.,|A\.-G\.,|A\. G\.) ?(S. A.)?|^[A-Z]. [A-Z]. \w{1,10}|^[A-Z][a-z]{1,3}\. \w{1,10}-?\w{1,10}|^\w{1,10} & \w{1,10}|^[A-Z]. \w{1,10}|.{1,100} Co\.|^.{1,10}\(.{1,10}\)( ?&? ? (Sons)?)|.{1,10}-.{1,10}, [A-Z][a-z]?.|^[A-Z][a-z]{1,10}, [A-Z]\.)',
        text)
    if match:
        result["company_found"] = True
        result["company"] = match.group(0)

    # Check each line against a regex for Company with () etc
    match = re.match(
        r'(^[A-Z][a-z]{1,8},? ?\([A-Z][a-z]{1,8}\)( ?&? ? (Sons)?))',
        text)
    if match:
        result["company2_found"] = True
        result["company2"] = match.group(0)

    # Check each line against a regex for Page Numbers
    match = re.search(r'(([0-9]{1,2},? ?){1,15}$|^([0-9]{1,2},? ?){1,15})', text)
    if match:
        result["page_numbers_found"] = True
        result["page_numbers"] = match.group(0)

    return result

def get_meta_data(file):
    # The file variable gets split by _ and the first part is the year
    year = file.split('_')[0]
    page = int(file.split('_')[1].split('.')[0])
    meta_data = {}
    # load page_info.csv as csv file. Search for the year in the first column
    # and return the second column as the page number
    with open('meta/page_info.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == year:
                meta_data['year'] = year
                meta_data['page'] = page

                range_definition = "unknown"
                try:
                    if page in range(int(row[1]), int(row[2]) + 1):
                        range_definition = "board_member"
                except ValueError:
                    pass

                try:
                    if page in range(int(row[3]), int(row[4]) + 1):
                        range_definition = "index"
                except ValueError:
                    pass

                try:
                    if page in range(int(row[5]), int(row[6]) + 1):
                        range_definition = "new_member"
                except ValueError:
                    pass

                try:
                    if page in range(int(row[7]), int(row[8]) + 1):
                        range_definition = "alphabetical"
                except ValueError:
                    pass

                meta_data['range_definition'] = range_definition

                excluded = [int(x) for x in row[12].replace("'", "").split(',')]
                if page in excluded:
                    meta_data['excluded'] = True

    return meta_data

def parse_year(data_folder, output_folder):
    # Open the data folder and create a AltoFileParser object for each file in the folder.
    # The AltoParser object will parse the file and store the results in a list of dictionaries.
    for file in sorted(os.listdir(f'{data_folder}/')):
        if file.endswith(".xml") or file.endswith(".alto"):
            print("Parsing file: " + file)
            meta_data = get_meta_data(file)
            if not meta_data.get('excluded', False):
                parser = MyAltoFileParser(f'{data_folder}/' + file, meta_data)
                parser.parse_file(parsing_function)
                for line in range(parser.get_number_of_lines()):
                    # parser.print_line_summary(line)
                    pass
                csv_filename = file.split('.')[0] + '.csv'
                print(parser.print_file_summary())
                parser.save_csv_file(f"./{output_folder}/" + csv_filename)
                print("Done parsing file: " + file)
            else:
                print("File is excluded: " + file)

if __name__ == "__main__":
    parse_year('data_1921', 'output_1921')

