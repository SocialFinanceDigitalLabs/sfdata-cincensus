from ._data import *

HEADERS_CHILD_IDENTIFIERS = (
    "LAchildID",
    "UPN",
    "FormerUPN",
    "UPNunknown",
    "PersonBirthDate",
    "ExpectedPersonBirthDate",
    "GenderCurrent",
    "PersonDeathDate",
)

HEADERS_CIN_DETAILS = (
    "LAchildID",
    "CINdetailsID",
    "CINreferralDate",
    "ReferralSource",
    "PrimaryNeedCode",
    "CINclosureDate",
    "ReasonForClosure",
    "DateOfInitialCPC",
    "ReferralNFA",
)

HEADERS_CHILD_CHARACTERISTICS = ("Ethnicity", "Disabilities")

HEADERS_CIN_PLAN_DATES = ("LAchildID", "CINdetailsID", "CINPlanStartDate", "CINPlanEndDate")


def write_child_identifiers(message: Message, headers=True):
    if headers:
        yield HEADERS_CHILD_IDENTIFIERS
    for child in message.children:
        yield (
            child.child_identifiers.la_child_id,
            child.child_identifiers.upn,
            child.child_identifiers.former_upn,
            child.child_identifiers.upn_unknown,
            child.child_identifiers.person_birth_date,
            child.child_identifiers.expected_person_birth_date,
            child.child_identifiers.gender_current,
            child.child_identifiers.person_death_date,
        )


"""def table_write_child_characteristics(message: Message, headers= True):
    if headers:
        yield HEADERS_CHILD_CHARACTERISTICS
    for child in message.children:
        yield(
                child.child_characteristics.ethnicity,
                child.child_characteristics.disabilities,
            )
"""


def table_write_cin_plan_dates(message: Message, headers=True):
    if headers:
        yield HEADERS_CIN_PLAN_DATES
    for child in message.children:
        for ix, cin_detail in enumerate(child.cin_details):
            for cin_plan_date in cin_detail.cin_plan_dates:
                yield (
                    child.child_identifiers.la_child_id,
                    ix,
                    cin_plan_date.start_date, 
                    cin_plan_date.end_date
                    )


def write_cin_details(message: Message, headers=True):
    if headers:
        yield HEADERS_CIN_DETAILS
    for child in message.children:
        for ix, cin in enumerate(child.cin_details):
            yield (
                child.child_identifiers.la_child_id,
                ix,
                cin.cin_referral_date,
                cin.referral_source,
                cin.primary_need_code,
                cin.cin_closure_date,
                cin.reason_for_closure,
                cin.date_of_initial_cpc,
                "",  # TODO: Referral NFA
            )
