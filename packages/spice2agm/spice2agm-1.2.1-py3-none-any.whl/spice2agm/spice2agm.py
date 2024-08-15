import argparse
import json
import sys
from typing import Tuple, Iterable, List, Optional

from lxml import etree
from dotenv import dotenv_values
import numpy as np
import spiceypy

FIXED_FRAME_ID = 4
TO_FRAME = "JUICE_SPACECRAFT"
# Map each axis to its vector position
AXIS_MAP = {
    "X": 0,
    "Y": 1,
    "Z": 2,
}
VECTOR_TAG = "dirVector"
VECTOR_FRAME = "SC"
SPICE_HEADER_COMMENTS = [
    ("*" * 52),
    "SPICE DIRECTIONS",
    "as defined by the JUICE SPICE Kernel data set with.",
    "MK_IDENTIFIER = {}",
]
MK_COMMENT_WIDTH = 58


def read_config(config_path: str) -> dict:
    """ Read configuration file

    Configuration is stored in a JSON file and is read into a dictionary

    :param config_path: Path to the configuration file
    :return: Dictionary containing configuration variables
    """
    with open(config_path) as f:
        config = json.load(f)
    return config


def get_parser():
    """ Parse command line arguments

    Metakernel, input file and output file can be passed as command line arguments
    or in the configuration file, which is mandatory.
    """
    parser = argparse.ArgumentParser(description="Generate AGM definitions file")
    parser.add_argument("config", help="Configuration file")
    parser.add_argument("-m", "--metakernel", help="SPICE metakernel to load")
    parser.add_argument("-i", "--input", help="XML AGM definitions file")
    parser.add_argument("-o", "--output", help="Output XML file to write")
    parser.add_argument("-d", "--date", help="Reference UTC date")
    return parser


def get_parameters(arguments: dict, config: dict) -> dict:
    """ Merge parameters from command line arguments and configuration file

    Parameters from the command line take precedence over the configuration file

    :param  dict arguments: arguments parsed from the command line
    :param dict config: parameters read from the configuration file
    :type config: dict

    :return: dictionary with parameter names as keys and the corresponding values.
    :rtype: dict

    :raises SystemExit: if a parameter is not set in either in the command line or
        configuration file.
    """
    parameters = {}
    for parameter in ("metakernel", "input", "output", "date"):
        argument_value = arguments[parameter]
        config_value = config.get(parameter)
        if argument_value and config_value:
            print(f"Warning: {parameter} is set in configuration and command line")
        value = argument_value or config_value
        if not value:
            print(f"Error: {parameter} must be set in configuration or command line")
            sys.exit(1)
        parameters[parameter] = value
    return parameters


def create_snippet(frame: str, direction: str, date:str, mapping:str) -> Tuple[etree.Comment, etree.Element]:
    """ Create XML snippet for a frame and direction

    :param str frame: Name of the frame, e.g. JUICE_UVS_SP
    :param str direction: Direction, with sign and axis (e.g. "+X", "-Y", "+Z")

    :return: Tuple with two elements: the first is a comment with the frame and
        direction; the second is an XML element with the values for all axes.
    """
    vector = get_directions(frame, direction, date)
    comment = etree.Comment(f" {frame} {direction} ")
    direction_camel_case = direction[-1]
    if '-' in direction:
        direction_camel_case = 'm' + direction_camel_case
    if not mapping:
        name = f'{frame}_{direction_camel_case}axis'
    else:
        name = mapping
    vector_element = etree.Element(VECTOR_TAG, name=name, frame=VECTOR_FRAME)
    for label, value in zip(AXIS_MAP, vector):
        element = etree.Element(label.lower())
        element.text = f"{value:.8f}"
        vector_element.append(element)
    return comment, vector_element


def get_directions(frame, direction, date):
    """ Calculate vector from frame and direction

    :param str frame: name of the frame, e.g. JUICE_UVS_SP
    :param str direction: Direction, with sign and axis (e.g. "+X", "-Y", "+Z")

    :return: numpy array with values for each axis (X, Y and Z).
    """
    matrix = spiceypy.pxform(frame, TO_FRAME, spiceypy.utc2et(date))
    direction = translate_direction(direction)
    vector = spiceypy.mxv(matrix, direction)
    return vector


def translate_direction(direction: str):
    """
    Transforms direction represented as an axis string into corresponding vector

    :param str direction: Direction, with sign and axis (e.g. "+X", "-Y", "+Z")

    :raises ValueError: If direction is invalid

    :return: vector corresponding to an axis (e.g. [0, 0, 1] for direction "+Z")
    """
    sign, axis = direction
    if sign not in ("+", "-") or axis not in ("X", "Y", "Z"):
        raise ValueError
    vector = np.zeros(shape=3, dtype=np.int8)
    position = AXIS_MAP[axis]
    vector[position] = 1 if sign == "+" else -1
    return vector


def insert_snippets(document, snippets):
    """ Insert XML snippets in AGM document

    First, the insertion position is determined; if there is none, the snippets are
    appended to the root of the document; otherwise they are added next to the
    insertion point, in reverse order so they end up in the order in which they are
    passed.

    If there is an existing section with SPICE directions, it is removed before adding
    the snippets.

    :param etree.ElementTree document: Document where snippets will be inserted.
    :param List[Iterable] snippets: XML snippets as a list; each item in the list is
        an iterable of XML objects, so the list has to be iterated twice to add them.
    """

    # Finding the insertion element must be done first, because it uses an existing
    # SPICE section, if present
    insertion_element = find_insertion_element(document)
    remove_spice_section(document)
    if insertion_element is None:
        root = document.getroot()
        for snippet in snippets:
            for element in snippet:
                root.append(element)
    else:
        for snippet in snippets[::-1]:
            for element in snippet[::-1]:
                insertion_element.addnext(element)


def find_insertion_element(document) -> Optional[etree.Element]:
    """ Find element after which the SPICE directions section is to be inserted

    This element will be the one immediately preceding an existing SPICE DIRECTIONS
    section start, or, if that doesn't exist, the element immediately preceding a
    comment with a line of "*"s, which marks the start of another section. If neither
    exist, there is no insertion point and the function returns None.

    :param etree.ElementTree document: Document where insertion point will be searched.
    :return: Element after which snippets will be inserted, or None
    """
    try:
        element = document.xpath("//comment()[.=' SPICE DIRECTIONS ']")[0]
    except IndexError:
        for comment in document.xpath("//comment()"):
            if "***" in comment.text:
                element = comment.getprevious()
                break
        else:
            return
    else:
        # go back two elements because there's the SPICE DIRECTIONS comment and
        # another comment with a line of "*"s marking the section start
        element = element.getprevious().getprevious()
    return element


def remove_spice_section(document):
    """ Remove SPICE directions section from document

    This function removes all the elements from the comments starting a
    SPICE directions - including those comments - until the next comment with a
    line of "*"s, or the end of the document, if such a comment does not exist.
    """
    if not document.xpath("//comment()[.=' SPICE DIRECTIONS ']"):
        return
    parent = document.getroot()
    inside_spice_section = False
    for element in parent.iterchildren():
        if element.text == " SPICE DIRECTIONS ":
            inside_spice_section = True
        if inside_spice_section:
            parent.remove(element.getprevious())
            try:
                if element.text.startswith(" ***"):
                    break
            except AttributeError:
                continue
    else:
        parent.remove(element)


def get_valid_frames(class_id=FIXED_FRAME_ID) -> List[int]:
    """ Retrieve fixed JUICE frames

    :param int class_id: ID of the frame class to consider valid
    :return: List of frames that are considered valid according to class ID and range
    """
    fixed_frames = spiceypy.kplfrm(class_id)
    valid_frames = [frame for frame in fixed_frames if -29_000 < frame <= -28_000]
    return valid_frames


def get_spice_header():
    """ Generate SPICE comments with metakernel identifier """
    comments = []
    for comment in SPICE_HEADER_COMMENTS:
        if "MK_IDENTIFIER" in comment:
            mk_identifier = get_mk_identifier()
            comment = comment.format(mk_identifier)
        comment = comment.ljust(MK_COMMENT_WIDTH - 1).rjust(MK_COMMENT_WIDTH)
        comment_element = etree.Comment(comment)
        comments.append(comment_element)
    return comments


def get_mk_identifier() -> str:
    """ Retrieve MK_IDENTIFIER of the loaded metakernel """
    try:
        mk_identifier = spiceypy.gcpool("MK_IDENTIFIER", 0, 1)[0]
    except (IndexError, spiceypy.exceptions.NotFoundError):
        print("WARNING: Could not find MK_IDENTIFIER.")
        mk_identifier = ""
    return mk_identifier


def format_document(document: etree.ElementTree):
    """ Add blank lines before comments and indent document with four spaces

    :param etree.ElementTree document: Document to format.
    """
    etree.indent(document, space="    ")
    for comment in document.xpath(".//comment()"):
        element = comment.getprevious()
        if element is None:
            continue
        if element.text.strip() in SPICE_HEADER_COMMENTS:
            continue
        if element.text.startswith(" ***"):
            continue
        element.tail = "\n\n    "


class Spice2AGM:
    def __init__(
        self,
        config: dict,
        metakernel: str = None,
        input: str = None,
        output: str = None,
        date: str = None,
    ):
        arguments = {"metakernel": metakernel, "input": input, "output": output, "date":date}
        parameters = get_parameters(arguments, config)
        mk = parameters["metakernel"]
        if "$KERNELS_JUICE" in mk:
            env_values = dotenv_values()
            kernels_dir = env_values['KERNELS_JUICE']
            mk = mk.replace("$KERNELS_JUICE",kernels_dir)
        spiceypy.furnsh(mk)
        self.valid_frames = get_valid_frames()
        self.input = parameters["input"]
        self.output = parameters["output"]
        self.date = parameters["date"]
        self.directions = config.get("directions")
        try:
            self.mapping = config.get("mapping")
        except:
            self.mapping = None

    def write_agm(self):
        """ Create AGM XML file and write it to output file """
        document = self.create_agm()
        format_document(document)
        self.write_document(document)

    def create_agm(self) -> etree.ElementTree:
        """ Create AGM document with SPICE directions

        This method generates XML snippets for each frame and corresponding direction,
        read from the configuration file, and inserts them into the AGM template.

        :return: AGM XML document with snippets inserted.
        """
        snippets = self.create_snippets()
        document = self.read_template()
        insert_snippets(document, snippets)
        return document

    def create_snippets(self) -> List[Iterable]:
        """ Process directions for each frame to generate XML snippets

        :return: List of iterables containing etree elements comprising the snippets
        """
        snippets: List[Iterable] = [get_spice_header()]
        for frame, directions in self.directions.items():
            if not self.is_frame_valid(frame):
                print(f"WARNING: {frame} is not a FIXED frame")
                pass
            for direction in directions:
                try:
                    if f'{frame} {direction}' in self.mapping.keys():
                        mapping = self.mapping[f'{frame} {direction}']
                    else:
                        mapping = None
                    snippet = create_snippet(frame, direction, self.date, mapping)
                except ValueError:
                    print(f"Could not calculate direction {direction} in frame {frame} at {self.date}")
                    continue
                except spiceypy.exceptions.SpiceNOFRAMECONNECT:
                    print(f"Could not calculate frame {frame}")
                    continue
                except spiceypy.exceptions.SpiceUNKNOWNFRAME:
                    print(f"{frame} is not a valid frame")
                    continue
                snippets.append(snippet)
        return snippets

    def is_frame_valid(self, frame) -> bool:
        """ Verify that frame is fixed and within -29,000 - -28,000 range

         :param str frame: Name of the frame to verify
         :return: bool
         """
        frame_id = spiceypy.namfrm(frame)
        return True if frame_id in self.valid_frames else False

    def read_template(self) -> etree.ElementTree:
        """ Read XML file template

        Blank text is removed to facilitate formatting of the document after snippets
        are inserted.

        :return: XML Document
        :rtype: etree.ElementTree
        """
        parser = etree.XMLParser(remove_blank_text=True)
        doc = etree.parse(self.input, parser)
        return doc

    def write_document(self, document: etree.ElementTree):
        """ Write AGM XML document to output file

        :param etree.ElementTree document: Document to write
        """
        document.write(self.output, encoding="utf-8", pretty_print=True)


def main():
    args = get_parser().parse_args()
    pars = vars(args)
    conf_path = pars.pop("config")
    conf = read_config(conf_path)
    converter = Spice2AGM(conf, **pars)
    converter.write_agm()


if __name__ == "__main__":
    main()
