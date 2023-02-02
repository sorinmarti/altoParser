import xml.etree.ElementTree as ETree
from abc import abstractmethod


class AltoFileParser:
    """This class parses 1 ALTO file sand returns structured JSON data"""

    filename = None
    line_strings = []
    line_bounding_boxes = []
    structured_data = []

    def __init__(self, filename):
        self.filename = filename

    def parse_file(self, parsing_function):
        xml_tree, xmlns = AltoFileParser.xml_parse_file(self.filename)
        for text_region in xml_tree.iterfind('.//{%s}TextBlock' % xmlns):
            for text_line in text_region.iterfind('.//{%s}TextLine' % xmlns):
                for text_bit in text_line.findall('{%s}String' % xmlns):
                    line_content = text_bit.attrib.get('CONTENT')
                    self.line_strings.append(line_content)
                    self.structured_data.append(parsing_function(line_content, line_content.split()))
                    self.line_bounding_boxes.append(text_bit.attrib.get('HPOS') + ',' + text_bit.attrib.get('VPOS') + ',' +
                                                    text_bit.attrib.get('WIDTH') + ',' + text_bit.attrib.get('HEIGHT'))

    def get_file_json(self):
        return self.structured_data

    def get_line_json(self, line):
        return self.structured_data[line]

    def get_number_of_lines(self):
        return len(self.structured_data)

    def print_line_summary(self, line):
        print(self.line_strings[line])
        print(self.line_bounding_boxes[line])
        print(self.structured_data[line])

    def save_csv_file(self, filename, delimiter=';'):
        csv_file = ''
        for line in range(self.get_number_of_lines()):
            csv_file += self.line_strings[line] + delimiter + \
                        self.line_bounding_boxes[line] + "\n"

        # write to file
        with open(filename, 'w') as f:
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
            raise e

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

