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

additional_information = ["Space does not permit of full details being inserted. The term fancy goods covers, flouncings, edgings, insertions, galloons, plumetis, collars, aprons and handkerchiefs. Lingerie under separate heading.", "(Space does not permit of full details being inserted. The term \"fancy goods\" covers, flouncings, edgings, insertions, galloons, plumetis, collars, aprons and handkerchiefs. Lingerie under separate heading."]
additional_information_list = sorted(additional_information, key=len, reverse=True)

address = readcsv('meta/address.csv')
address_list = sorted(address, key=len, reverse=True)

names = ["FALCONER EVANS CROWE", "MAURICE GALLAND", "ALEXANDER RICHARDSON", "THEO. RUSSELL", "T. EDGAR HARLEY", "E. G. B. MAXSE", "J. LOMAS", "R. HAMILTON", "Sir Milne CHEETHAM", "A. RICHARDSON"]
names_list = sorted(names, key=len, reverse=True)

headline = ["LIST OF MEMBERS of the British Chamber of Commerce for Switzerland", "Page", "Address", "Trade and Name", "INDEX:", "Classified List of the Members of the British Chamber of Commerce for Switzerland", "TRADE INDEX"]
headline_list = sorted(headline, key=len, reverse=True)

titles = readcsv('meta/titles.csv')
titles_list = sorted(titles, key=len, reverse=True)

companies = readcsv('meta/companies.csv')
companies_list = sorted(companies, key=len, reverse=True)

goods = readcsv('meta/goods.csv')
goods_list = sorted(goods, key=len, reverse=True)

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
    match = re.search(r'(H\. B\. M\. Minister|Manager, Lloyds & National Provincial Foreign Bank, Ltd\.|Treasurer Provincial Foreign Bank Ltd\.|H\. B\. M\. Consul-General|H\. B\. M\. Consul|H\.B\.M\. Commercial Hon\. Vice-President Secretary)', text)
    if match:
        result["profession_found"] = True
        result["profession"] = match.group(0)

    # Check each line against a regex for Title
    match = re.search(r'(Officers and Members of the Board|Active Members of the Board|Corresponding Members of the Board|Hon\. Members of the Board|THE BRITISH CHAMBER OF COMMERCE FOR SWITZERLAND|THE COUNCIL IN 1923|OFFICERS OF THE CHAMBER|Council:)', text)
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

    # Check each word against the list headline_list
    for headline in headline_list:
        if headline in text:
            result["headline_found"] = True
            result["headline"] = headline
            break

    # Check each word against the list locations_parser.csv
    for loc in locations_list:
        if loc in text:
            result["location_found"] = True
            result["location"] = loc
            break

    # Check each line against the list titles
    for title in titles_list:
        if title in text:
            result["title_list_found"] = True
            result["title_list"] = title
            break

    # Check each line against a regex for Title
    match = re.search(r'(([A-Z][a-z]{1,10})? ?([A-Z][a-z]{1,10}) \(([A-Z][a-z]{1,10})? ?([a-z]{1,15})?,? ?([a-z]{1,15})\)$|^ ?[A-Z][a-z]{1,20}(( and | und )? ?-?[A-Z][a-z]{1,20})?( and | und )?( ?[A-Z][a-z]{1,20})?( ?\([A-Z][a-z]{1,10}\))?$|^ ?[A-Z][a-z]{1,10} \([A-Z][a-z]{1,10}\) [A-Z][a-z]{1,15}$)', text)
    if match:
        result["title_found"] = True
        result["title"] = match.group(0)

    # Check each line against a regex for Company
    match = re.search(
        r'(^.{1,30} ? (Frères|Brothers|Co\.|& Co\.,|Ltd\.|& Cie.,|S\. A\.,|A\.-G\.,|A\. G\.) ?(S. A.)?|^[A-Z]. [A-Z]. \w{1,10}|^ ?[A-Z][a-z]{1,3}\. \w{1,10}-?\w{1,10}|^\w{1,10} & \w{1,10}|^ ?[A-Z]. \w{1,10}|.{1,100} Co\.)',
        text)
    if match:
        result["company_found"] = True
        result["company"] = match.group(0)

    # Check each line against the list companies
    for company in companies_list:
        if company in text:
            result["company_list_found"] = True
            result["company_list"] = company
            break

    # Check each line against a regex for Goods in brackets
    match = re.search(r'(\(.{1,150}\),? ?)', text)
    if match:
        result["goods_found"] = True
        result["goods"] = match.group(0)

    # Check each line against a regex for Address
    match = re.search(r'([0-9]{1,4}(,|\.) [A-Z].{1,15}(quai|berg|rain|vorstadt|weg|allee|gasse|graben|strasse|platz| Street| Road)|[0-9]{1,4}(,|\.)? (rue de la|Route des|Route de|Boulevard de|Charing|Via|Pall|Avenue de|Rue|Rue de|Grand|Rue du|rue|St.|Avenue|Place|Avenue de la|Rue de la|Ruelle) [A-Z].{1,15},|[A-Z][a-z]{1,10} (E.| W. S.) [0-9]{1,3})', text)
    if match:
        result["address_found"] = True
        result["address"] = match.group(0)

    for my_address in address_list:
        if my_address in text:
            result["address_list_found"] = True
            result["address_list_item"] = my_address
            break

    for info in additional_information_list:
        if info in text:
            result["additional_information_found"] = True
            result["additional_information"] = info
            break

    # Check each line against the list goods_list
    for good in goods_list:
        if good in text:
            result["goods_list_found"] = True
            result["goods_list"] = good
            break

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

    # Check each line against the list company
    for company in companies_list:
        if company in text:
            result["company_list_found"] = True
            result["company_list"] = company
            break

    # Check each line against a regex for Company with & Co. etc
    match = re.search(
        r'([A-Z].{1,30} ? (& C\.|Limited|Frère|Frères|Brothers|Co\.|& Co\.,|Ltd\.|& Cie.,|S\. A\.,|A\.-G\.,|A\. G\.) ?(S. A.)?|^[A-Z]. [A-Z]. \w{1,10}|^[A-Z][a-z]{1,3}\. \w{1,10}-?\w{1,10}|^\w{1,10} & \w{1,10}|^[A-Z]. \w{1,10}|[A-Z].{1,100} Co\.|^.{1,10}\(.{1,10}\)( ?&? ? (Sons)?),? ?|[A-Z].{1,10}-.{1,10}, [A-Z][a-z]?.|^[A-Z][a-z]{1,10}, [A-Z]\.)',
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

    # Check each line against a regex for Company with () etc
    match = re.search(
        r'([A-Z][a-z]{1,10}.{1,10}\([A-Z].{1,10}\) ?&? ?(A. G.|A.G.|Son|Cie.|Co.,?|Frère,?)?,? ?(Ltd.|S. A.)?)',
        text)
    if match:
        result["company3_found"] = True
        result["company3"] = match.group(0)

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
    parse_year('data_1923', 'output_1923')