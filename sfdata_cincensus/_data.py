from dataclasses import dataclass
from datetime import date, datetime
from typing import List


@dataclass
class Header:
    collection: str = None
    year: int = None
    reference_date: date = None
    source_level: str = None
    lea: str = None
    software_code: str = None
    release: str = None
    serial_no: str = None
    date_time: datetime = None


@dataclass
class ChildIdentifiers:
    la_child_id: str = None
    upn: str = None
    former_upn: str = None
    upn_unknown: str = None
    person_birth_date: date = None
    expected_person_birth_date: date = None
    gender_current: str = None
    person_death_date: date = None


@dataclass
class ChildCharacteristics:
    ethnicity: str = None
    disabilities: List[str] = None


@dataclass
class Assessment:
    actual_start_date: date = None
    internal_review_date: date = None
    authorisation_date: date = None
    factors_identified_at_assessment: List[
        str,
    ] = None


@dataclass
class CinPlanDates:
    start_date: date = None
    end_date: date = None


@dataclass
class Section47:
    actual_start_date: date = None
    initial_cpc_target: date = None
    date_of_initial_cpc: date = None
    icpc_not_required: str = None


@dataclass
class ChildProtectionPlans:
    start_date: date = None
    end_date: date = None
    initial_category_of_abuse: str = None
    latest_category_of_abuse: str = None
    number_of_previous_cpp: str = None
    review_dates: List[date] = None


@dataclass
class CinDetails:
    cin_referral_date: date = None
    referral_source: str = None
    primary_need_code: str = None
    cin_closure_date: date = None
    reason_for_closure: str = None
    date_of_initial_cpc: date = None
    referral_nfa: str = None
    assessments: List[Assessment] = None


@dataclass
class Child:
    child_identifiers: ChildIdentifiers = None
    child_characteristics: ChildCharacteristics = None
    cin_details: List[CinDetails] = None


@dataclass
class Message:
    header: Header = None
    children: List[Child] = None
