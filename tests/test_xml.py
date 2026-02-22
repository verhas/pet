import pytest
from pathlib import Path
from pet.macros.data.xml import xml

FIXTURE = Path(__file__).parent / "xml" / "pom.xml"


@pytest.fixture
def pom():
    return xml(str(FIXTURE))


# --- single leaf element: returns text string --------------------------------

def test_single_leaf_returns_string(pom):
    assert pom.xml('version') == '1.2.3'

def test_single_leaf_dot_prefix(pom):
    assert pom.xml('./artifactId') == 'my-app'

def test_single_leaf_nested(pom):
    assert pom.xml('properties/java.version') == '17'

def test_single_leaf_deeply_nested(pom):
    assert pom.xml('build/plugins/plugin/version') == '3.11.0'


# --- single complex element: returns xml wrapper -----------------------------

def test_single_complex_element_is_xml(pom):
    result = pom.xml('dependencies')
    assert isinstance(result, xml)

def test_single_complex_sub_query(pom):
    deps = pom.xml('dependencies')
    # query inside the returned wrapper
    assert deps.xml('dependency[1]/artifactId') == 'slf4j-api'


# --- iterate over a complex element's children -------------------------------

def test_iterate_complex_element(pom):
    # pom.xml('dependencies') returns the <dependencies> wrapper;
    # iterating yields each <dependency> as an xml wrapper
    deps = list(pom.xml('dependencies'))
    assert len(deps) == 3

def test_iterate_and_query_children(pom):
    result = [(dep.xml('groupId'), dep.xml('version'))
              for dep in pom.xml('dependencies')]
    assert result == [
        ('org.slf4j',          '2.0.0'),
        ('org.junit.jupiter',  '5.10.0'),
        ('com.google.guava',   '32.1.3-jre'),
    ]


# --- multiple matches: returns list ------------------------------------------

def test_multiple_leaf_matches_returns_list(pom):
    result = pom.xml('dependencies/dependency/artifactId')
    assert result == ['slf4j-api', 'junit-jupiter', 'guava']

def test_multiple_complex_matches_returns_list(pom):
    result = pom.xml('dependencies/dependency')
    assert isinstance(result, list)
    assert len(result) == 3

def test_multiple_complex_matches_are_xml_wrappers(pom):
    deps = pom.xml('dependencies/dependency')
    assert all(isinstance(d, xml) for d in deps)

def test_iterate_list_and_query(pom):
    versions = [dep.xml('version') for dep in pom.xml('dependencies/dependency')]
    assert versions == ['2.0.0', '5.10.0', '32.1.3-jre']


# --- predicate: find by sibling value ----------------------------------------

def test_predicate_by_groupId(pom):
    assert pom.xml("dependencies/dependency[groupId='org.slf4j']/version") == '2.0.0'

def test_predicate_by_scope_attribute(pom):
    # scope is an XML attribute, so use [@scope=...] not [scope=...]
    assert pom.xml("dependencies/dependency[@scope='test']/version") == '5.10.0'

def test_predicate_by_artifactId(pom):
    assert pom.xml("dependencies/dependency[artifactId='guava']/version") == '32.1.3-jre'


# --- positional index --------------------------------------------------------

def test_positional_first(pom):
    assert pom.xml('dependencies/dependency[1]/artifactId') == 'slf4j-api'

def test_positional_third(pom):
    assert pom.xml('dependencies/dependency[3]/artifactId') == 'guava'


# --- missing element ---------------------------------------------------------

def test_no_match_returns_none(pom):
    assert pom.xml('nonexistent') is None

def test_no_match_predicate_returns_none(pom):
    assert pom.xml("dependencies/dependency[groupId='no.such']/version") is None


# --- namespace transparency --------------------------------------------------

def test_namespace_not_required(pom):
    assert pom.xml('modelVersion') == '4.0.0'


# --- attr(): read XML attributes ---------------------------------------------

def test_attr_single_element(pom):
    # <dependency scope="test"> — scope is an XML attribute, not a child tag
    assert pom.attr('dependencies/dependency[2]', 'scope') == 'test'

def test_attr_compile_scope(pom):
    assert pom.attr('dependencies/dependency[3]', 'scope') == 'compile'

def test_attr_optional(pom):
    assert pom.attr('dependencies/dependency[3]', 'optional') == 'true'

def test_attr_absent_returns_none(pom):
    # first dependency has no scope attribute
    assert pom.attr('dependencies/dependency[1]', 'scope') is None

def test_attr_multiple_elements_returns_list(pom):
    # all three dependencies — first has no scope, second 'test', third 'compile'
    assert pom.attr('dependencies/dependency', 'scope') == [None, 'test', 'compile']

def test_attr_no_match_returns_none(pom):
    assert pom.attr('nonexistent', 'scope') is None


# --- filter by attribute in xml() XPath -------------------------------------

def test_filter_by_attribute_presence(pom):
    # [@optional] selects elements that have the optional attribute
    dep = pom.xml('dependencies/dependency[@optional]')
    assert isinstance(dep, xml)
    assert dep.xml('artifactId') == 'guava'

def test_filter_by_attribute_value(pom):
    assert pom.xml("dependencies/dependency[@scope='test']/artifactId") == 'junit-jupiter'

def test_filter_by_attribute_value_version(pom):
    assert pom.xml("dependencies/dependency[@scope='compile']/version") == '32.1.3-jre'


# --- __str__ on complex element ----------------------------------------------

def test_str_of_complex_element(pom):
    # complex elements have no meaningful text; __str__ returns empty string
    assert str(pom.xml('dependencies')) == ''


# --- error handling ----------------------------------------------------------

def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        xml("no_such_file.xml")
