from datetime import date

from sfdata_cincensus import CINFaker, PropertyChain


def test_child_identifiers():
    faker = CINFaker(0)

    obj = faker.child_identifiers(
        la_child_id="child1",
        person_birth_date=date(2019, 1, 1),
    )
    assert obj.la_child_id == "child1"
    assert obj.person_birth_date == date(2019, 1, 1)


def test_cin_details():
    faker = CINFaker(0)

    obj = faker.cin_details(
        cin_referral_date=date(2019, 1, 1),
    )
    assert obj.cin_referral_date == date(2019, 1, 1)


def test_nested():
    faker = CINFaker(0)
    c = PropertyChain()
    message = faker.message(
        children=[
            c.child_identifiers(
                c.la_child_id("child1").person_birth_date(date(2019, 1, 1))
            ),
        ]
    )

    obj = message.children[0]

    assert obj.child_identifiers.la_child_id == "child1"
    assert obj.child_identifiers.person_birth_date == date(2019, 1, 1)
