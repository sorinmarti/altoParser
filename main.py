import os
import re

from alto_parser import AltoFileParser

my_locations = ["London", "Lugano", "Bern", "Bradford."]
personal_titles = ["Esq."]
trash = ["Addrens"]

def parsing_function(text, words):
    print("Structuring line: " + text)

    result = {'transcription': text}

    # Regex match for the whole line
    if re.match(r'^(\w{1,20} ?(\w{1,10})) (\(.*[^.]\))$|^(\w{1,10})$|^(\w{1,10}) ?(\w{1,10})$', text):
        result["title_found"] = True
        result["title"] = (text)

    # Check each word against a list of values
    for word in words:
        if word in my_locations:
            result["location_found"] = True
            result["location"] = word

    return result
"""
    # Find the last word in the text
    if len(words) > 0:
        result["last_location"] = words[-1]

    # Regex match for the whole line
    if re.match(r'^\d+$', text):
        result["number_found"] = True
        result["number"] = int(text)

    # Check each word against a list of values
    for word in words:
        if word in my_locations:
            result["location_found"] = True
            result["location"] = word

    # Check the first word
    if len(words) > 0 and words[0] == "SWISS":
        result["swiss_found"] = True

    for word in words:
        if word in personal_titles:
            result["personal_title_found"] = True
            result["personal_title"] = word

    for word in words:
        if word in trash:
            result["trash_found"] = True
            result["trash"] = word
    return result
"""


if __name__ == "__main__":
    # Open the data folder and create a AltoFileParser object for each file in the folder.
    # The AltoParser object will parse the file and store the results in a list of dictionaries.
    for file in os.listdir('data_test'):
        if file.endswith(".xml") or file.endswith(".alto"):
            print("Parsing file: " + file)
            parser = AltoFileParser('data_test/' + file)
            parser.parse_file(parsing_function)
            for line in range(parser.get_number_of_lines()):
                parser.print_line_summary(line)
                pass

            csv_filename = file.split('.')[0] + '.csv'
            parser.save_csv_file("./" + csv_filename)
            print("Done parsing file: " + file)

