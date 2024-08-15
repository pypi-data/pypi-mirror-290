""" open_ortho: a collection of static open-ortho.org codes.

Used whenever a code is necessary, for various implementations.
"""
from . import Code
PREFIX = 'OPOR'

def make_code(s):
    """
    Convert a string of ASCII characters to a single string of their equivalent integer values concatenated together.

    Args:
    s (str): A string to convert.

    Returns:
    str: A string consisting of the ASCII integer values concatenated together without any spaces.
    """
    # Convert each character to its ASCII integer, then to a string, and concatenate
    return ''.join(str(ord(char)) for char in s)

class NAMESPACES:
    root_uid = "1.3.6.1.4.1.61741.11.3"
    url =  "http://open-ortho.org/terminology"

IV01 = Code(
    system=NAMESPACES.url,
    code=f"{NAMESPACES.root_uid}.{make_code('IV01')}",
    display='Intraoral Right Buccal Segment, Centric Occlusion, Direct View',
    synonyms=[''])
""" Used for ... """

