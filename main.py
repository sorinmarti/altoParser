import csv
import os
import re
from typing import Dict, Any

from alto_parser import AltoFileParser
from search_helper import SearchHelper


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
location_searcher = SearchHelper("location")
location_searcher.set_search_list(locations_extended_list)

personal_titles = ["Esq.","Esq.,", "C.B.,", "C.V. O.,"]
personal_titles_list = sorted(personal_titles, key=len, reverse=True)
personal_titles_searcher = SearchHelper("personal_titles")
personal_titles_searcher.set_search_list(personal_titles_list)

additional_information = ["Further Advisory Committees will be appointed as occasion arises.", "Space does not permit of full details being inserted. The term fancy goods covers, flouncings, edgings, insertions, galloons, plumetis, collars, aprons and handkerchiefs. Lingerie under separate heading.", "(Space does not permit of full details being inserted. The term \"fancy goods\" covers, flouncings, edgings, insertions, galloons, plumetis, collars, aprons and handkerchiefs. Lingerie under separate heading."]
additional_information_list = sorted(additional_information, key=len, reverse=True)
additional_information_searcher = SearchHelper("additional_information")
additional_information_searcher.set_search_list(additional_information_list)

address = readcsv('meta/address.csv')
address_list = sorted(address, key=len, reverse=True)
address_searcher = SearchHelper("address")
address_searcher.set_search_list(address_list)
address_searcher.set_pattern_list([r'([0-9]{1,4}(,|\.) [A-Z].{1,15}(sprung|quai|berg|rain|vorstadt|weg|allee|gasse|graben|strasse|platz| Street| Road)|[0-9]{1,4}(,|\.)? (rue de la|Route des|Route de|Boulevard de|Charing|Via|Pall|Avenue de|Rue|Rue de|Grand|Rue du|rue|St.|Avenue|Place|Avenue de la|Rue de la|Ruelle) [A-Z].{1,15},|[A-Z][a-z]{1,10} (E.| W. S.) [0-9]{1,3})', ])

names = readcsv('meta/names.csv')
names_list = sorted(names, key=len, reverse=True)
name_searcher = SearchHelper("name")
name_searcher.set_search_list(names_list)
name_searcher.set_pattern_list([r'((Mr\. )?([A-Z]{1,2}\.) ([A-Z]{1,2}\. )?[A-Z]{1,10})', ])

headline = ["TRADE IRIDE", "LIST OF MEMBERS of the British Chamber of Commerce for Switzerland", "Page", "Address", "Trade and Name", "INDEX:", "Classified List of the Members of the British Chamber of Commerce for Switzerland", "TRADE INDEX", "INDEX"]
headline_list = sorted(headline, key=len, reverse=True)
headline_searcher = SearchHelper("headline")
headline_searcher.set_search_list(headline_list)

titles = readcsv('meta/titles.csv')
titles_list = sorted(titles, key=len, reverse=True)
title_searcher = SearchHelper("title")
title_searcher.set_search_list(titles_list)
title_searcher.set_pattern_list([r'(([A-Z][a-z]{1,10})? ?([A-Z][a-z]{1,10}) \(([A-Z][a-z]{1,10})? ?([a-z]{1,15})?,? ?([a-z]{1,15})\)$|^ ?[A-Z][a-z]{1,20}(( and | und )? ?-?[A-Z][a-z]{1,20})?( and | und )?( ?[A-Z][a-z]{1,20})?( ?\([A-Z][a-z]{1,10}\))?$|^ ?[A-Z][a-z]{1,10} \([A-Z][a-z]{1,10}\) [A-Z][a-z]{1,15}$)', ])

companies = readcsv('meta/companies.csv')
companies_list = sorted(companies, key=len, reverse=True)
company_searcher = SearchHelper("company")
company_searcher.set_search_list(companies_list)
company_searcher.set_pattern_list([r'(^.{1,30} ? (Frères|Brothers|Co\.|& Co\.,|Ltd\.|& Cie.,|S\. A\.,|A\.-G\.,|A\. G\.) ?(S. A.)?|^[A-Z]. [A-Z]. \w{1,10}|^ ?[A-Z][a-z]{1,3}\. \w{1,10}-?\w{1,10}|^\w{1,10} & \w{1,10}|^ ?[A-Z]. \w{1,10}|.{1,100} Co\.)', ])
company_searcher_2 = SearchHelper("company_2")
company_searcher_2.set_pattern_list([r'(([A-Z][a-z]{1,10},? &? ?[A-Z][a-z]{1,10}|[A-Z][a-z]{1,10},? [A-Z]\. ?[A-Z]?\.?|[A-Z][a-z]{1,8},? ?\([A-Z][a-z]{1,8}\)( ?&? ? (Sons)?)|[A-Z][a-z]{1,10} ?,?&? ?))', ])
company_searcher_3 = SearchHelper("company_3")
company_searcher_3.set_pattern_list([r'([A-Z][a-z]{1,10}.{1,10}\([A-Z].{1,10}\) ?&? ?(A. G.|A.G.|Son|Cie.|Co.,?|Frère,?)?,? ?(Ltd.|S. A.)?)', ])

goods = readcsv('meta/goods.csv')
goods_list = sorted(goods, key=len, reverse=True)
goods_searcher = SearchHelper("goods")
goods_searcher.set_search_list(goods_list)
goods_searcher.set_pattern_list([r'(?!\((Grands Magasins Innovation, S.A.)\)|\(agent\)|\(Egypt\)|\(J. Baumgartner\)|\(O. Hauser\)|\(Ch. Mayer, Prop.\)|\(Stockport\)|\(Switzerland\)|\(Burg\)|\(Continental\)|\(1920\)|\(Bury\)|\(England\))\(.{1,150}\),? ?', ])

page_number_searcher = SearchHelper("page_number")
page_number_searcher.set_pattern_list([r'((Mr\. )?([A-Z]{1,2}\.) ([A-Z]{1,2}\. )?[A-Z]{1,10})', ])

board_title_searcher = SearchHelper("board_title")
board_title_searcher.set_pattern_list([r'(Council :|Council|ADVISORY COMMITTEES|Finance Commillee.|Propaganda Commillee.|Rhine Navigation Commillee.|Committee jor French Switzerland.|Watch Industries Commillee.|MEMBERS OF THE COUNCIL|THE COUNCIL IN 1922|Officers and Members of the Board|Active Members of the Board|Corresponding Members of the Board|Hon\. Members of the Board|THE BRITISH CHAMBER OF COMMERCE FOR SWITZERLAND|THE COUNCIL IN 1923|OFFICERS OF THE CHAMBER|Council:)', ])

profession_searcher = SearchHelper("profession")
profession_searcher.set_pattern_list([r'(His Britannic Majestys Minister to the Swiss Confederation|Lloyds & National Provincial Foreign Bank Ltd.|C.B., C.V. O., II. B.M., Minister|H. B. M. Commercial Secretary)', ])

function_searcher = SearchHelper("function")
function_searcher.set_pattern_list([r'(\(Chairman\)|\(Secretary\)|Hon\. President|Hon\. Vice-President|President|Hon\. Treasurer|Vice-President|Secretary-General, Head Office|Hon\. Secretary, Lausanne Branch|THE HON PRESIDENT|THE HON. VICE PRESIDENT)', ])


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

    result = {'transcription': text}

    board_title_result = board_title_searcher.search(text, SearchHelper.LIST_BF_PATTERN)
    result = result | board_title_result

    additional_information_result = additional_information_searcher.search(text, SearchHelper.LIST_BF_PATTERN)
    result = result | additional_information_result

    if not board_title_result:

        location_result = location_searcher.search_in_list(text)
        result = result | location_result

        profession_result = profession_searcher.search(text, SearchHelper.LIST_BF_PATTERN)
        result = result | profession_result

        personal_titles_result = personal_titles_searcher.search_in_list(text)
        result = result | personal_titles_result

        function_result = function_searcher.search(text, SearchHelper.LIST_BF_PATTERN)
        result = result | function_result

        name_result = name_searcher.search(text, SearchHelper.LIST_BF_PATTERN)
        result = result | name_result

    return result

def parse_new_member_page(text, words):
    return {}

def parse_index_page(text, words):

    result = {'transcription': text}

    # Check each word against the list headline_list
    headline_result = headline_searcher.search_in_list(text)
    result = result | headline_result

    title_result = title_searcher.search(text, SearchHelper.LIST_BF_PATTERN)
    result = result | title_result

    additional_information_result = additional_information_searcher.search_in_list(text)
    result = result | additional_information_result


    if not headline_result and not title_result and not additional_information_result:
        # If no headline found, check each word against the location names
        location_result = location_searcher.search_in_list(text)
        result = result | location_result

        company_result = company_searcher.search(text, SearchHelper.LIST_BF_PATTERN,
                                                 matching_strategy=SearchHelper.MATCHING_STRATEGY_LONGEST)
        result = result | company_result

        goods_result = goods_searcher.search(text, SearchHelper.LIST_BF_PATTERN)
        result = result | goods_result

        address_result = address_searcher.search(text, priority=SearchHelper.LIST_BF_PATTERN,
                                                 exit_after_match=False)
        result = result | address_result

    return result

def parse_alphabetical_index_page(text, words):
    # print("Structuring line: " + text)

    result = {'transcription': text}

    # Check each word against the list headings
    headline_result = headline_searcher.search_in_list(text)
    result = result | headline_result

    additional_information_result = additional_information_searcher.search_in_list(text)
    result = result | additional_information_result

    if not headline_result and not additional_information_result:

        page_number_result = page_number_searcher.search_in_pattern(text)
        result = result | page_number_result

        company_1_result = company_searcher.search(text, SearchHelper.LIST_BF_PATTERN,
                                                   matching_strategy=SearchHelper.MATCHING_STRATEGY_LONGEST)
        result = result | company_1_result

        company_2_result = company_searcher_2.search(text, SearchHelper.LIST_BF_PATTERN,
                                                    matching_strategy=SearchHelper.MATCHING_STRATEGY_LONGEST)
        result = result | company_2_result

        company_result_3 = company_searcher_3.search(text, SearchHelper.LIST_BF_PATTERN,
                                                    matching_strategy=SearchHelper.MATCHING_STRATEGY_LONGEST)
        result = result | company_result_3

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
    parse_year('data_1922', 'output_1922')
    parse_year('data_1923', 'output_1923')
    parse_year('data_1925', 'output_1925')
    parse_year('data_1925', 'output_1925')
    parse_year('data_1927', 'output_1927')
    parse_year('data_1929', 'output_1929')
    parse_year('data_1931', 'output_1931')