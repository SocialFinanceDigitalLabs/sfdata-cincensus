from functools import wraps
from typing import Optional, Union
from xml.etree.ElementTree import Element

from ._data import *

__tag_lookup = {}

E = Union[Optional[Element], list[Element]]


def element_handler(func):
    @wraps(func)
    def inner(element: E):
        if element is None:
            return None
        elif isinstance(element, list):
            return [inner(e) for e in element]
        elif isinstance(element, Element):
            return func(element)
        else:
            raise TypeError(f"Expected Element or list, got {type(element)}")

    return inner


def xml_reader(tag: str):
    def wrapper(func):
        @wraps(func)
        @element_handler
        def inner(element: Element):
            assert element.tag == tag, f"Expected {tag} element, got {element.tag}"
            return func(element)

        __tag_lookup[tag] = inner
        return inner

    return wrapper


@element_handler
def read_text(element: Element):
    return element.text


@element_handler
def read_xml(element: Element):
    return __tag_lookup[element.tag](element)


@xml_reader("ChildIdentifiers")
def read_child_identifiers(element: Element) -> ChildIdentifiers:
    child_identifiers = ChildIdentifiers()
    child_identifiers.la_child_id = read_text(element.find("LAchildID"))
    return child_identifiers


@xml_reader("ChildCharacteristics")
def read_child_characteristics(element: Element) -> ChildCharacteristics:
    child_characteristics = ChildCharacteristics()
    child_characteristics.ethnicity = read_text(element.find("Ethnicity"))
    child_characteristics.disabilities = read_text(element.findall("Disability"))
    return child_characteristics


@xml_reader("CINdetails")
def read_cin_details(element: Element) -> CinDetails:
    cin_details = CinDetails()
    return cin_details


@xml_reader("Child")
def read_child(element: E) -> Child:
    child = Child()
    child.child_identifiers = read_child_identifiers(element.find("ChildIdentifiers"))
    child.child_characteristics = read_child_characteristics(
        element.find("ChildCharacteristics")
    )
    child.cin_details = read_cin_details(element.findall("CINdetails"))
    return child
