from functools import wraps
from typing import Union
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

from ._data import *


def xml_writer(tag: str):
    def wrapper(func):
        @wraps(func)
        def inner(value, parent=None):
            if value is None:
                return None
            element = ET.SubElement(parent, tag) if parent else ET.Element(tag)
            return func(value, element)

        return inner

    return wrapper


def write_text(value: Union[str, list, tuple], tag: str, element: Element):
    if value is None:
        return
    elif isinstance(value, (list, tuple)):
        for v in value:
            write_text(v, tag, element)
    else:
        ET.SubElement(element, tag).text = value


@xml_writer("Child")
def write_child_characteristics(child_characteristics: ChildCharacteristics, element):
    write_text(child_characteristics.ethnicity, "Ethnicity", element)
    if child_characteristics.disabilities:
        disabilities = ET.SubElement(element, "Disabilities")
        write_text(child_characteristics.disabilities, "Disability", disabilities)
    return element


@xml_writer("Child")
def write_child(child: Child, element: Element):
    write_child_characteristics(child.child_characteristics, element)
    return element
