from datetime import date

from sfdata_cincensus import (
    HEADERS_CHILD_IDENTIFIERS,
    CINFaker,
    PropertyChain,
    write_child_identifiers,
)


def test_write_child_identifiers():
    faker = CINFaker(0)
    c = PropertyChain()
    obj = faker.message(
        children=[
            c.child_identifiers(
                c.la_child_id("child1").person_birth_date(date(2019, 1, 1))
            ),
        ]
    )

    rows = list(write_child_identifiers(obj))

    assert rows == [
        HEADERS_CHILD_IDENTIFIERS,
        ("child1", None, None, None, date(2019, 1, 1), None, None, None),
    ]
