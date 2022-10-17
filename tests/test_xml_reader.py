import xml.etree.ElementTree as ET

from sfdata_cincensus import *


def test_xml():
    obj = read_xml(ET.fromstring("<Child/>"))
    assert isinstance(obj, Child)

    obj = read_xml(ET.fromstring("<ChildIdentifiers/>"))
    assert isinstance(obj, ChildIdentifiers)


def test_read_multiple():
    root = ET.fromstring("<Children><Child /><Child /></Children>")
    children = read_child(root.findall("Child"))
    assert len(children) == 2


def test_read_child():
    xml = """
    <Child>
        <ChildIdentifiers><LAchildID>CHILD1</LAchildID></ChildIdentifiers>
        <ChildCharacteristics><Ethnicity>ETHN</Ethnicity></ChildCharacteristics>
        <CINdetails></CINdetails>
        <CINdetails></CINdetails>
    </Child>
    """
    child = read_child(ET.fromstring(xml))

    assert child.child_identifiers.la_child_id == "CHILD1"
    assert child.child_characteristics.ethnicity == "ETHN"
    assert len(child.cin_details) == 2
