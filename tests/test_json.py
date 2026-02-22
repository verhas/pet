import pytest
from pathlib import Path
from pet.macros.data.json import json

FIXTURE = Path(__file__).parent / "json" / "package.json"


@pytest.fixture
def pkg():
    return json(str(FIXTURE))


# --- scalar values -----------------------------------------------------------

def test_top_level_string(pkg):
    assert pkg.get('name') == 'my-app'

def test_top_level_version(pkg):
    assert pkg.get('version') == '1.0.0'

def test_nested_scalar(pkg):
    assert pkg.get('scripts.build') == 'webpack'

def test_nested_scalar_test_script(pkg):
    assert pkg.get('scripts.test') == 'jest'


# --- nested object returns wrapper -------------------------------------------

def test_nested_object_returns_json(pkg):
    result = pkg.get('scripts')
    assert isinstance(result, json)

def test_nested_object_further_query(pkg):
    scripts = pkg.get('scripts')
    assert scripts.get('build') == 'webpack'


# --- list of objects ---------------------------------------------------------

def test_list_of_objects_returns_list(pkg):
    result = pkg.get('dependencies')
    assert isinstance(result, list)
    assert len(result) == 2

def test_list_elements_are_wrapped(pkg):
    deps = pkg.get('dependencies')
    assert all(isinstance(d, json) for d in deps)

def test_iterate_list_and_query(pkg):
    names = [dep.get('name') for dep in pkg.get('dependencies')]
    assert names == ['lodash', 'express']

def test_list_index_access(pkg):
    assert pkg.get('dependencies.0.name') == 'lodash'
    assert pkg.get('dependencies.1.version') == '4.18.0'


# --- list of scalars ---------------------------------------------------------

def test_list_of_scalars(pkg):
    assert pkg.get('tags') == ['web', 'api', 'rest']


# --- missing path ------------------------------------------------------------

def test_missing_key_returns_none(pkg):
    assert pkg.get('nonexistent') is None

def test_missing_nested_key_returns_none(pkg):
    assert pkg.get('scripts.nonexistent') is None

def test_out_of_bounds_index_returns_none(pkg):
    assert pkg.get('dependencies.99.name') is None


# --- __str__ -----------------------------------------------------------------

def test_str_of_scalar(pkg):
    assert str(pkg.get('version')) == '1.0.0'

def test_str_of_object_wrapper_is_empty(pkg):
    assert str(pkg.get('scripts')) == ''


# --- error handling ----------------------------------------------------------

def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        json("no_such_file.json")
