import random
from collections import defaultdict
from datetime import timedelta

from ._data import *


class Chain(dict):
    def __getattr__(self, item):
        def func(val):
            self[item] = val
            return Chain(self)

        return func


class PropertyChain(dict):
    def __getattr__(self, item):
        def func(val):
            chain = Chain()
            chain[item] = val
            return chain

        return func


class SubArgs(dict):
    def __init__(self, kwargs):
        self.__kwargs = defaultdict(dict)
        main_args = {}
        for k, v in kwargs.items():
            if "__" in k:
                group, key = k.split("__", 1)
                self.__kwargs[group][key] = v
            else:
                main_args[k] = v
        super().__init__(self, **main_args)

    def __getattr__(self, name):
        return self.__kwargs[name]


class Faker:
    def __init__(self, seed=0):
        self._random = random.Random()
        self._random.seed(0)

    @property
    def random(self):
        return self._random

    def random_date(
        self,
        reference_date: date = None,
        days: int = 0,
        months: int = 0,
        years: int = 0,
    ):
        if reference_date is None:
            reference_date = date.today()

        args = [x for x in (days, months, years) if x != 0]
        if len(args) > 1:
            raise ValueError("Only one of days, months, years can be non-zero")
        if years != 0:
            days = years * 365
        elif months != 0:
            days = months * 30

        offset = self.randint(0, abs(days))
        if days < 0:
            offset = -offset

        return reference_date + timedelta(days=offset)

    def __getattr__(self, item):
        return getattr(self.random, f"{item}")


class CINFaker:
    def __init__(self, seed=0):
        self._random = Faker(seed)

    @property
    def random(self):
        return self._random

    def child_identifiers(self, auto=True, reference_date: date = None, **kwargs):
        if reference_date is None:
            reference_date = self.random.random_date(years=18)

        props = {}
        if auto:
            props["la_child_id"] = self.random.randint(1000000000, 9999999999)
            props["person_birth_date"] = reference_date

        props.update(kwargs)
        return ChildIdentifiers(**props)

    def cin_details(self, auto=True, reference_date: date = None, **kwargs):
        if reference_date is None:
            reference_date = self.random.random_date(years=18)

        props = {}
        if auto:
            props["cin_referral_date"] = self.random.random_date(
                reference_date, years=17
            )

        props.update(kwargs)
        return CinDetails(**props)

    def child(self, auto=True, **kwargs):
        props = {}
        if auto:
            pass
        props.update(kwargs)

        props = SubArgs(props)

        if isinstance(props.get("child_identifiers"), dict):
            props["child_identifiers"] = self.child_identifiers(
                auto=auto, **props["child_identifiers"]
            )
        elif "child_identifiers" not in props:
            props["child_identifiers"] = self.child_identifiers(
                auto=auto, **props.child_identifiers
            )

        return Child(**props)

    def message(self, auto=True, **kwargs):
        props = {}
        if auto:
            pass
        props.update(kwargs)
        props = SubArgs(props)

        if isinstance(props.get("children"), list):
            props["children"] = [self.child(auto=auto, **x) for x in props["children"]]
        elif isinstance(props.get("children"), int):
            props["children"] = [
                self.child(auto=auto) for _ in range(props["children"])
            ]
        elif "children" not in props:
            props["children"] = [
                self.child(auto=auto) for _ in range(self.random.randint(1, 250))
            ]

        return Message(**props)
