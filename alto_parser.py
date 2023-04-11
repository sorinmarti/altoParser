import xml.etree.ElementTree as ETree
from abc import abstractmethod


class AltoFileParser:
    """This class parses 1 ALTO file sand returns structured JSON data"""

    add_meta_data = True
    filename = None
    line_strings = []
    line_bounding_boxes = []
    structured_data = []
    meta_data = {}

    def __init__(self, filename, meta_data):
        self.filename = filename
        self.structured_data = []
        self.line_strings = []
        self.line_bounding_boxes = []
        self.meta_data = meta_data
        if self.meta_data is None:
            self.meta_data = {}

    def parse_file(self, parsing_function, auto_clean=True):
        xml_tree, xmlns = AltoFileParser.xml_parse_file(self.filename)
        if xml_tree is None:
            return

        for text_region in xml_tree.iterfind('.//{%s}TextBlock' % xmlns):
            merged_line = ""
            for text_line in text_region.iterfind('.//{%s}TextLine' % xmlns):
                for text_bit in text_line.findall('{%s}String' % xmlns):
                    line_content = text_bit.attrib.get('CONTENT')
                    merged_line += " " + line_content

            data = parsing_function(merged_line, merged_line.split(), self.meta_data)
            if auto_clean:
                self.clean_data(data)

            if self.add_meta_data:
                data = data | self.meta_data

            self.structured_data.append(data)
            self.line_bounding_boxes.append(text_region.attrib.get('HPOS') + ',' + text_region.attrib.get('VPOS') + ',' +
                                            text_region.attrib.get('WIDTH') + ',' + text_region.attrib.get('HEIGHT'))
            self.line_strings.append(merged_line)

    def get_file_json(self):
        return self.structured_data

    def get_line_json(self, line):
        return self.structured_data[line]

    def get_number_of_lines(self):
        return len(self.structured_data)

    def print_file_summary(self):
        summary = f"File: {self.filename} has {self.get_number_of_lines()} lines."
        if len(self.structured_data) > 0:
            summary += f" First line: {self.structured_data[0]}"
        return summary

    def print_line_summary(self, line):
        print(self.line_strings[line])
        print(self.line_bounding_boxes[line])
        print(self.structured_data[line])

    def export_file(self, export_function):
        line_number = 0
        for line in self.structured_data:
            export_function(line, self.line_bounding_boxes[line_number])
            line_number += 1

    def save_csv_file(self, filename, delimiter='\t'):
        csv_file = ''
        list_of_keys = []
        for line in self.structured_data:
            for key in line:
                if key not in list_of_keys:
                    list_of_keys.append(key)

        # write header
        for key in list_of_keys:
            csv_file += key + delimiter
        csv_file = csv_file[:-len(delimiter)]
        csv_file += '\n'

        for line in self.structured_data:
            for key in list_of_keys:
                if key in line:
                    csv_file += str(line[key]) + delimiter
                else:
                    csv_file += delimiter
            csv_file = csv_file[:-len(delimiter)]
            csv_file += '\n'

        # write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(csv_file)

    @abstractmethod
    def xml_parse_file(filename):
        """ This function uses the Etree xml parser to parse an alto file. It should not be called from outside this
            class. The parse_file() method calls it."""

        namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO',
                     'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
                     'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#',
                     'alto-4': 'http://www.loc.gov/standards/alto/ns-v4#'}

        try:
            xml_tree = ETree.parse(filename)
        except ETree.ParseError as e:
            print("Error parsing file: " + filename)
            return None, None

        if 'http://' in str(xml_tree.getroot().tag.split('}')[0].strip('{')):
            xmlns = xml_tree.getroot().tag.split('}')[0].strip('{')
        else:
            try:
                ns = xml_tree.getroot().attrib
                xmlns = str(ns).split(' ')[1].strip('}').strip("'")
            except IndexError:
                xmlns = 'no_namespace_found'

        if xmlns not in namespace.values():
            raise IndexError('No valid namespace has been found.')

        return xml_tree, xmlns

    def clean_data(self, data):
        """This function cleans the data from the parsing function. It should not be called from outside this class.
            The parse_file() method calls it."""

        for key in data:
            data[key].strip()

        return data

    def export_data(self, type='csv', filename='export.csv', delimiter='\t'):
        if type == 'csv':
            self.save_csv_file(filename, delimiter)
        else:
            raise ValueError("Export type not supported.")

