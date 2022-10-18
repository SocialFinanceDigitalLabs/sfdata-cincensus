from datetime import date

from sfdata_cincensus import Faker


def test_date_offset():
    reference_date = date(2019, 1, 1)

    faker = Faker(0)
    assert faker.random_date(reference_date) == date(2019, 1, 1)
    assert faker.random_date(reference_date, years=1) == date(2019, 8, 4)
    assert faker.random_date(reference_date, years=-1) == date(2018, 12, 12)

    assert faker.random_date(reference_date, months=1) == date(2019, 1, 9)
    assert faker.random_date(reference_date, months=-1) == date(2018, 12, 2)

    assert faker.random_date(reference_date, days=7) == date(2019, 1, 8)
    assert faker.random_date(reference_date, days=-7) == date(2018, 12, 26)
