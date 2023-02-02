import os
import re

from alto_parser import AltoFileParser

my_locations = ["London", "Lugano"]

def parsing_function(text, words):
    result = {'transcription': text}

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
    if len(words)>0 and words[0] == "SWISS":
        result["swiss_found"] = True

    return result


if __name__ == "__main__":
    # Open the data folder and create a AltoFileParser object for each file in the folder.
    # The AltoParser object will parse the file and store the results in a list of dictionaries.
    for file in os.listdir('data'):
        print("Parsing file: " + file)
        parser = AltoFileParser('data/' + file)
        parser.parse_file(parsing_function)
        for line in range(parser.get_number_of_lines()):
            parser.print_line_summary(line)
            pass
        print("Done parsing file: " + file)
