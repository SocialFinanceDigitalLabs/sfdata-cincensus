from decimal import setcontext
from functools import wraps
from typing import Optional, Union
from xml.etree.ElementTree import Element

from ._data import *

__tag_lookup = {}

E = Union[Optional[Element], list[Element]]


def element_handler(func):
    @wraps(func)
    def inner(element: E):
        if element is None:
            return None
        elif isinstance(element, list):
            return [inner(e) for e in element]
        elif isinstance(element, Element):
            return func(element)
        else:
            raise TypeError(f"Expected Element or list, got {type(element)}")

    return inner


def xml_reader(tag: str):
    def wrapper(func):
        @wraps(func)
        @element_handler
        def inner(element: Element):
            assert element.tag == tag, f"Expected {tag} element, got {element.tag}"
            return func(element)

        __tag_lookup[tag] = inner
        return inner

    return wrapper


@element_handler
def read_text(element: Element):
    return element.text


@element_handler
def read_xml(element: Element):
    return __tag_lookup[element.tag](element)


@xml_reader("Header")
def read_header(element: Element) -> Header:
    header = Header()
    header.collection = read_text(element.find("CollectionDetails/Collection"))
    header.year = read_text(element.find("CollectionDetails/Year"))
    header.reference_date = read_text(element.find("CollectionDetails/ReferenceDate"))
    header.source_level = read_text(element.find("Source/SourceLevel"))
    header.lea = read_text(element.find("Source/LEA"))
    header.software_code = read_text(element.find("Source/SoftwareCode"))
    header.release = read_text(element.find("Source/Release"))
    header.serial_no = read_text(element.find("Source/SerialNo"))
    header.date_time = read_text(element.find("Source/DateTime"))

    return header


@xml_reader("ChildIdentifiers")
def read_child_identifiers(element: Element) -> ChildIdentifiers:
    child_identifiers = ChildIdentifiers()
    child_identifiers.la_child_id = read_text(element.find("LAchildID"))
    child_identifiers.upn = read_text(element.find("UPN"))
    child_identifiers.former_upn = read_text(element.find("FormerUPN"))
    child_identifiers.upn_unknown = read_text(element.find("UPNunknown"))
    child_identifiers.person_birth_date = read_text(element.find("PersonBirthDate"))
    child_identifiers.expected_person_birth_date = read_text(
        element.find("ExpectedPersonBirthDate")
    )
    child_identifiers.gender_current = read_text(element.find("GenderCurrent"))
    child_identifiers.person_death_date = read_text(element.find("PersonDeathDate"))
    """,  "",  , """
    return child_identifiers


@xml_reader("ChildCharacteristics")
def read_child_characteristics(element: Element) -> ChildCharacteristics:
    child_characteristics = ChildCharacteristics()
    child_characteristics.ethnicity = read_text(element.find("Ethnicity"))
    child_characteristics.disabilities = read_text(
        element.findall("Disabilities/Disability")
    )
    return child_characteristics


@xml_reader("CINdetails")
def read_cin_details(element: Element) -> CinDetails:
    cin_details = CinDetails()
    cin_details.cin_referral_date = read_text(element.find("CINreferralDate"))
    cin_details.referral_source = read_text(element.find("ReferralSource"))
    cin_details.primary_need_code = read_text(element.find("PrimaryNeedCode"))
    cin_details.cin_closure_date = read_text(element.find("CINclosureDate"))
    cin_details.reason_for_closure = read_text(element.find("ReasonForClosure"))
    cin_details.date_of_initial_cpc = read_text(element.find("DateOfInitialCPC"))
    cin_details.referral_nfa = read_text(element.find("ReferralNFA"))
    return cin_details


@xml_reader("Assessments")
def read_assessments(element: Element) -> Assessment:
    assessment = Assessment()
    assessment.actual_start_date = read_text(element.find("AssessmentActualStartDate"))
    assessment.internal_review_date = read_text(
        element.find("AssessmentInternalReviewDate")
    )
    assessment.authorisation_date = read_text(
        element.find("AssessmentAuthorisationDate")
    )
    assessment.factors_identified_at_assessment = read_text(
        element.findall("FactorsIdentifiedAtAssessment/AssessmentFactors")
    )

    return assessment


@xml_reader("CINPlanDates")
def read_cin_plan_dates(element: Element) -> CinPlanDates:
    cin_plan_dates = CinPlanDates()
    cin_plan_dates.start_date = read_text(element.find("CINPlanStartDate"))
    cin_plan_dates.end_date = read_text(element.find("CINPlanEndDate"))

    return cin_plan_dates


@xml_reader("Section47")
def read_section_47(element: Element) -> Section47:
    section_47 = Section47()
    section_47.actual_start_date = read_text(element.find("S47ActualStartDate"))
    section_47.initial_cpc_target = read_text(element.find("InitialCPCtarget"))
    section_47.date_of_initial_cpc = read_text(element.find("DateOfInitialCPC"))
    section_47.icpc_not_required = read_text(element.find("ICPCnotRequired"))

    return section_47


@xml_reader("ChildProtectionPlans")
def read_child_protection_plans(element: Element) -> ChildProtectionPlans:
    child_protection_plans = ChildProtectionPlans()
    child_protection_plans.start_date = read_text(element.find("CPPstartDate"))
    child_protection_plans.end_date = read_text(element.find("CPPendDate"))
    child_protection_plans.initial_category_of_abuse = read_text(
        element.find("InitialCategoryOfAbuse")
    )
    child_protection_plans.latest_category_of_abuse = read_text(
        element.find("LatestCategoryOfAbuse")
    )
    child_protection_plans.number_of_previous_cpp = read_text(
        element.find("NumberOfPreviousCPP")
    )
    child_protection_plans.review_dates = read_text(
        element.findall("Reviews/CPPreviewDate")
    )

    return child_protection_plans


@xml_reader("Child")
def read_child(element: E) -> Child:
    child = Child()
    child.child_identifiers = read_child_identifiers(element.find("ChildIdentifiers"))
    child.child_characteristics = read_child_characteristics(
        element.find("ChildCharacteristics")
    )
    child.cin_details = read_cin_details(element.findall("CINdetails"))
    return child
