from datetime import date

from sfdata_cincensus import *
from sfdata_cincensus import (
    HEADERS_CHILD_IDENTIFIERS,
    HEADERS_CIN_PLAN_DATES,
    CINFaker,
    PropertyChain,
    table_write_cin_plan_dates,
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


def test_table_write_cin_plan_dates():
    child = Child()
    child.child_identifiers = ChildIdentifiers(la_child_id="child15")
    child.cin_details = [
        CinDetails(
            cin_plan_dates=[
                CinPlanDates(start_date=date(2019, 1, 1), end_date=date(2019, 5, 1))
            ]
        )
    ]
    rows = list(table_write_cin_plan_dates(Message(children=[child])))

    assert rows == [
        HEADERS_CIN_PLAN_DATES,
        ("child15", 0, date(2019, 1, 1), date(2019, 5, 1)),
    ]
