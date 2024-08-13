"""Some utility functions for querying XML."""

import re
import ast
import html
from lxml import etree as ET

_XPATH_ID_PATTERN = re.compile(r".*@id='([^']*)'")


def extract_id_from_xpath(xpath: str):
    return re.match(_XPATH_ID_PATTERN, xpath.rsplit("/", 1)[-1]).group(1)


def xml_to_primitive(value: str):
    """Converts a string attribute value to an appropriate Python type using ast.literal_eval."""
    try:
        # Safely evaluate value as a Python literal
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        # Return the original value if it's not a valid Python literal
        return value


def xml_element_to_string(
    element: ET.ElementBase, unescape: bool = True, with_tail: bool = False
):
    """Converts an lxml Element into a string."""
    result = ET.tostring(
        element,
        encoding=str,
        with_tail=with_tail,
    )
    if unescape:
        return html.unescape(result)
    else:
        return result
