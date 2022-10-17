from sfdata_cincensus import *
from sfdata_cincensus import write_child_characteristics


def test_write_child_characteristics():
    obj = ChildCharacteristics(ethnicity="ETHN", disabilities=("DIS1", "DIS2"))
    element = write_child_characteristics(obj)
    value = ET.tostring(element, encoding="unicode")
    assert (
        value
        == "<Child><Ethnicity>ETHN</Ethnicity><Disabilities><Disability>DIS1</Disability><Disability>DIS2</Disability></Disabilities></Child>"
    )
