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

def test_header():
    xml = """
    <Header>
        <CollectionDetails>
            <Collection>CIN</Collection>
            <Year>2023</Year>
            <ReferenceDate>2023-03-31</ReferenceDate>
        </CollectionDetails>
        <Source>
            <SourceLevel>L</SourceLevel>
            <LEA>201</LEA>
            <SoftwareCode>Local Authority</SoftwareCode>
            <Release>ver 3.1.21</Release>
            <SerialNo>001</SerialNo>
            <DateTime>2023-05-23T11:14:05</DateTime>
        </Source>
    </Header>
    """
    header = read_header(ET.fromstring(xml))

    assert header.collection == "CIN"
    assert header.year == "2023"
    assert header.reference_date == "2023-03-31"
    assert header.source_level == "L"
    assert header.lea == "201"
    assert header.software_code == "Local Authority"
    assert header.release == "ver 3.1.21"
    assert header.serial_no == "001"
    assert header.date_time == "2023-05-23T11:14:05"

def test_child_identifiers():
    xml = """
    <ChildIdentifiers>
        <LAchildID>CHILD1</LAchildID>
        <UPN>A123456789123</UPN>
        <FormerUPN>X98765432123B</FormerUPN>
        <UPNunknown>UN3</UPNunknown>
        <PersonBirthDate>1965-03-27</PersonBirthDate>
        <ExpectedPersonBirthDate>1986-04-13</ExpectedPersonBirthDate>
        <GenderCurrent>1</GenderCurrent>
        <PersonDeathDate>1980-10-08</PersonDeathDate>
    </ChildIdentifiers>
    """
    child_identifiers = read_child_identifiers(ET.fromstring(xml))

    assert child_identifiers.la_child_id == "CHILD1"
    assert child_identifiers.upn == "A123456789123"
    assert child_identifiers.former_upn == "X98765432123B"
    assert child_identifiers.upn_unknown == "UN3"
    assert child_identifiers.person_birth_date == "1965-03-27"
    assert child_identifiers.expected_person_birth_date == "1986-04-13"
    assert child_identifiers.gender_current == "1"
    assert child_identifiers.person_death_date == "1980-10-08"

def test_child_characteristics():
    xml =  """
    <ChildCharacteristics>
        <Ethnicity>ETHN</Ethnicity>   
        <Disabilities>
            <Disability>D1</Disability>
            <Disability>D2</Disability>
            <Disability>D3</Disability>
        </Disabilities>     
    </ChildCharacteristics>
    """
    child_characteristics = read_child_characteristics(ET.fromstring(xml))

    assert child_characteristics.ethnicity == "ETHN"
    assert child_characteristics.disabilities == ["D1", "D2", "D3",]

def test_cin_details():
    xml = """
    <CINdetails>
        <CINreferralDate>1970-10-06</CINreferralDate>
        <ReferralSource>1A</ReferralSource>
        <PrimaryNeedCode>N4</PrimaryNeedCode>
        <CINclosureDate>1971-02-27</CINclosureDate>
        <ReasonForClosure>RC1</ReasonForClosure>
        <DateOfInitialCPC>1970-12-06</DateOfInitialCPC>
        <ReferralNFA>0</ReferralNFA>
    </CINdetails>
    """
    cin_details = read_cin_details(ET.fromstring(xml))

    assert cin_details.cin_referral_date == "1970-10-06"
    assert cin_details.referral_source == "1A"
    assert cin_details.primary_need_code == "N4"
    assert cin_details.cin_closure_date == "1971-02-27"
    assert cin_details.reason_for_closure == "RC1"
    assert cin_details.date_of_initial_cpc == "1970-12-06"
    assert cin_details.referral_nfa == "0"
    
def test_assessment():
    xml = """
    <Assessments>
        <AssessmentActualStartDate>1970-06-03</AssessmentActualStartDate>
        <AssessmentInternalReviewDate>1970-06-22</AssessmentInternalReviewDate>
        <AssessmentAuthorisationDate>1971-07-18</AssessmentAuthorisationDate>
        <FactorsIdentifiedAtAssessment>
            <AssessmentFactors>2A</AssessmentFactors>
            <AssessmentFactors>2B</AssessmentFactors>
        </FactorsIdentifiedAtAssessment>
    </Assessments>
    """
    assessment = read_assessments(ET.fromstring(xml))

    assert assessment.actual_start_date == "1970-06-03"
    assert assessment.internal_review_date == "1970-06-22"
    assert assessment.authorisation_date == "1971-07-18"
    assert assessment.factors_identified_at_assessment == ["2A", "2B"]

def test_cin_plan_dates():
    xml = """
    <CINPlanDates>
        <CINPlanStartDate>1971-01-24</CINPlanStartDate>
        <CINPlanEndDate>1971-01-26</CINPlanEndDate>
    </CINPlanDates>
    """
    cin_plan_dates = read_cin_plan_dates(ET.fromstring(xml))
    
    assert cin_plan_dates.start_date == "1971-01-24"
    assert cin_plan_dates.end_date == "1971-01-26"

def test_section_47():
    xml= """
    <Section47>
        <S47ActualStartDate>1970-06-02</S47ActualStartDate>
        <InitialCPCtarget>1970-06-23</InitialCPCtarget>
        <DateOfInitialCPC>1970-06-17</DateOfInitialCPC>
        <ICPCnotRequired>false</ICPCnotRequired>
    </Section47>
    """
    section_47 = read_section_47(ET.fromstring(xml))

    assert section_47.actual_start_date == "1970-06-02"
    assert section_47.initial_cpc_target == "1970-06-23"
    assert section_47.date_of_initial_cpc == "1970-06-17"
    assert section_47.icpc_not_required == "false"

def test_child_protection_plans():
    xml = """
    <ChildProtectionPlans>
        <CPPstartDate>1970-02-17</CPPstartDate>
        <CPPendDate>1971-03-14</CPPendDate>
        <InitialCategoryOfAbuse>PHY</InitialCategoryOfAbuse>
        <LatestCategoryOfAbuse>PHY</LatestCategoryOfAbuse>
        <NumberOfPreviousCPP>10</NumberOfPreviousCPP>
        <Reviews>
            <CPPreviewDate>1971-02-15</CPPreviewDate>
            <CPPreviewDate>1973-02-15</CPPreviewDate>
        </Reviews>
    </ChildProtectionPlans>
    """
    child_protection_plans = read_child_protection_plans(ET.fromstring(xml))

    assert child_protection_plans.start_date == "1970-02-17"
    assert child_protection_plans.end_date == "1971-03-14"
    assert child_protection_plans.initial_category_of_abuse == "PHY"
    assert child_protection_plans.latest_category_of_abuse == "PHY"
    assert child_protection_plans.number_of_previous_cpp == "10"
    assert child_protection_plans.review_dates == ["1971-02-15", "1973-02-15"]
    
