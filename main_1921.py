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
locations_list = sorted(locations, key=len, reverse=True)
locations_extended = [locations[i] + "." for i in range(len(locations))]
locations_extended_list = sorted(locations_extended, key=len, reverse=True)

personal_titles = ["Esq.","Esq.,", "C.B.,", "C.V. O.,"]
personal_titles_list = sorted(personal_titles, key=len, reverse=True)

address = ["Castle Mills", "Trafalgar", "Trafalgar Square", "Imperial Buildings", "Cambridge Street"]
address_list = sorted(address, key=len, reverse=True)

names = ["FALCONER EVANS CROWE", "MAURICE GALLAND", "ALEXANDER RICHARDSON", "THEO. RUSSELL", "T. EDGAR HARLEY", "E. G. B. MAXSE", "J. LOMAS", "R. HAMILTON"]
names_list = sorted(names, key=len, reverse=True)

headline = ["LIST OF MEMBERS of the British Chamber of Commerce for Switzerland", "Page", "Address", "Trade and Name", "TRADE INDEX Classified List of the Members of the British Chamber of Commerce for Switzerland"]
headline_list = sorted(headline, key=len, reverse=True)

titles = readcsv('meta/titles.csv')
titles_list = sorted(titles, key=len, reverse=True)

companies = readcsv('meta/companies.csv')
companies_list = sorted(companies, key=len, reverse=True)

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
        print("Unknown range_definition: ", meta_data)
        return {}

def parse_board_member_page(text, words):
    text = text.strip()
    result = {'transcription': text}

    # Check each word against the list names
    for name in names_list:
        if name in text:
            result["name_found"] = True
            result["name_list"] = name
            break
    # Check each line against a regex for name
    match = re.search(r'(^[A-Z]\. ([A-Z]\.)? ?\w{1,100}|^[A-Z]{1,10} [A-Z]{1,10}[?:THE])', text)
    if match:
        result["name_found"] = True
        result["name"] = match.group(0)

    # Check each line against a regex for Profession
    match = re.search(r'(H\. B\. M\. Minister|Treasurer Provincial Foreign Bank Ltd\.|H\. B\. M\. Consul-General|H\. B\. M\. Consul|H\.B\.M\. Commercial Hon\. Vice-President Secretary)', text)
    if match:
        result["profession_found"] = True
        result["profession"] = match.group(0)

    # Check each line against a regex for Title
    match = re.search(r'(Officers and Members of the Board|Active Members of the Board|Corresponding Members of the Board|Hon\. Members of the Board|THE BRITISH CHAMBER OF COMMERCE FOR SWITZERLAND)', text)
    if match:
        result["title_found"] = True
        result["title"] = match.group(0)

    # Check each word against the list locations_parser.csv
    for location in locations_extended:
        if location in text:
            result["location_found"] = True
            result["location"] = location
            break

    # Check each word against the list personal_titles
    for title in personal_titles_list:
        if title in text:
            result["personal_title_found"] = True
            result["personal_title"] = title
            break

    # Check each line against a regex for function
    match = re.search(r'(Hon\. President|Hon\. Vice-President|President|Hon\. Treasurer|Vice-President|Secretary-General, Head Office|Hon\. Secretary, Lausanne Branch|THE HON PRESIDENT|THE HON. VICE PRESIDENT)', text)
    if match:
        result["function_found"] = True
        result["function"] = match.group(0)

    return result

def parse_new_member_page(text, words):
    return {}

def parse_index_page(text, words):

    result = {'transcription': text}

    # Check each word against the list headline
    for head in headline_list:
        if head in text:
            result["headline_found"] = True
            result["headline"] = head
            break

    # Check each word against the list locations_parser.csv
    for loc in locations_list:
        if loc in text:
            result["location_found"] = True
            result["location"] = loc
            break

    # Check each word against the list my_locations_extended list
    for loc_ext in locations_extended_list:
        if loc_ext in text:
            result["location_extended_found"] = True
            result["location_extended"] = loc_ext
            break
    """
    # Check each line against a regex for Title
    match = re.search(
        r'^(\w{1,20} ?(\w{1,10})) (\(\w*[^.]\))$|^\w{1,20}$|^\w{1,10} \w{1,10}$|^\w{1,10} \w{1,10} \w{1,15}$|^\w{1,10} \(\w{1,10}, .{1,25}\)$',
        text)
    if match:
        result["title_found"] = True
        result["title"] = match.group(0)
    """

    # Check each line against a regex for Title
    match = re.search(r'(^ ?[A-Z]{1,50} ?-?\(?[A-Z]{1,20} ?[A-Z]{1,20} ?[A-Z]{1,20}\)?)', text)
    if match:
        result["title_found"] = True
        result["title"] = match.group(0)

    # Check each line against the list titles
    for title in titles_list:
        if title in text:
            result["title_found"] = True
            result["title"] = title

    for my_address in address_list:
        if my_address in text:
            result["address_list_found"] = True
            result["address_list_item"] = my_address
            break

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

    # Check each word against the list headings
    for heading in headline:
        if heading in text:
            result["heading_found"] = True
            result["heading"] = heading
            break
    """
    # Check each word against the list locations_parser.csv
    for location in locations:
        if location in text:
            result["location_found"] = True
            result["location"] = location

    # Check each word against the list my_locations_extended list
    for location2 in locations_extended_sorted:
        if location2 in text:
            result["location_extended_found"] = True
            result["location_extended"] = location2
    """

    # Check each line against the list company
    for company in companies_list:
        if company in text:
            result["company_list_found"] = True
            result["company_list"] = company
            break

    # Check each line against a regex for Company with & Co. etc
    match = re.search(
        r'([A-Z].{1,30} ? (& C\.|Limited|Frères|Brothers|Co\.|& Co\.,|Ltd\.|& Cie.,|S\. A\.,|A\.-G\.,|A\. G\.) ?(S. A.)?|^[A-Z]. [A-Z]. \w{1,10}|^[A-Z][a-z]{1,3}\. \w{1,10}-?\w{1,10}|^\w{1,10} & \w{1,10}|^[A-Z]. \w{1,10}|[A-Z].{1,100} Co\.|^.{1,10}\(.{1,10}\)( ?&? ? (Sons)?)|[A-Z].{1,10}-.{1,10}, [A-Z][a-z]?.|^[A-Z][a-z]{1,10}, [A-Z]\.)',
        text)
    if match:
        result["company_found"] = True
        result["company"] = match.group(0)

    # Check each line against a regex for Company with () etc
    match = re.search(
        r'(([A-Z][a-z]{1,10},? &? ?[A-Z][a-z]{1,10}|[A-Z][a-z]{1,10},? [A-Z]\. ?[A-Z]?\.?|[A-Z][a-z]{1,8},? ?\([A-Z][a-z]{1,8}\)( ?&? ? (Sons)?)|[A-Z][a-z]{1,10} ?,?&? ?))',
        text)
    if match:
        result["company2_found"] = True
        result["company2"] = match.group(0)

    # Check each line against a regex for Page Numbers
    match = re.search(r'(([0-9]{1,5},? ?){1,15}$|^ ?([0-9]{1,5},? ?){1,15})', text)
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
            # print("Parsing file: " + file)
            meta_data = get_meta_data(file)
            if not meta_data.get('excluded', False):
                parser = MyAltoFileParser(f'{data_folder}/' + file, meta_data)
                parser.parse_file(parsing_function)
                for line in range(parser.get_number_of_lines()):
                    # parser.print_line_summary(line)
                    pass
                csv_filename = file.split('.')[0] + '.csv'
                # print(parser.print_file_summary())
                parser.save_csv_file(f"./{output_folder}/" + csv_filename)
                # print("Done parsing file: " + file)
            else:
                print("File is excluded: " + file)

if __name__ == "__main__":
    parse_year('data_1921', 'output_1921')

