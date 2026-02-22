import pytest
from pathlib import Path
from pet.macros.data.yaml import yaml

FIXTURE = Path(__file__).parent / "yaml" / "config.yaml"


@pytest.fixture
def cfg():
    return yaml(str(FIXTURE))


# --- scalar values -----------------------------------------------------------

def test_top_level_string(cfg):
    assert cfg.get('server.host') == 'localhost'

def test_top_level_integer(cfg):
    assert cfg.get('server.port') == 8080

def test_nested_scalar(cfg):
    assert cfg.get('database.credentials.username') == 'admin'


# --- nested dict returns wrapper ---------------------------------------------

def test_nested_dict_returns_yaml(cfg):
    result = cfg.get('server')
    assert isinstance(result, yaml)

def test_nested_dict_further_query(cfg):
    server = cfg.get('server')
    assert server.get('host') == 'localhost'
    assert server.get('port') == 8080


# --- list of dicts -----------------------------------------------------------

def test_list_of_dicts_returns_list(cfg):
    result = cfg.get('dependencies')
    assert isinstance(result, list)
    assert len(result) == 2

def test_list_elements_are_wrapped(cfg):
    deps = cfg.get('dependencies')
    assert all(isinstance(d, yaml) for d in deps)

def test_iterate_list_and_query(cfg):
    names = [dep.get('name') for dep in cfg.get('dependencies')]
    assert names == ['requests', 'flask']

def test_list_index_access(cfg):
    assert cfg.get('dependencies.0.name') == 'requests'
    assert cfg.get('dependencies.1.version') == '2.3.0'


# --- list of scalars ---------------------------------------------------------

def test_list_of_scalars(cfg):
    assert cfg.get('tags') == ['web', 'api', 'rest']


# --- missing path ------------------------------------------------------------

def test_missing_key_returns_none(cfg):
    assert cfg.get('nonexistent') is None

def test_missing_nested_key_returns_none(cfg):
    assert cfg.get('server.nonexistent') is None

def test_out_of_bounds_index_returns_none(cfg):
    assert cfg.get('dependencies.99.name') is None


# --- __str__ -----------------------------------------------------------------

def test_str_of_scalar(cfg):
    assert str(cfg.get('server.port')) == '8080'

def test_str_of_dict_wrapper_is_empty(cfg):
    assert str(cfg.get('server')) == ''


# --- __iter__ ----------------------------------------------------------------

def test_iter_over_dict_wrapper(cfg):
    values = list(cfg.get('server'))
    assert 'localhost' in values
    assert 8080 in values


# --- error handling ----------------------------------------------------------

def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        yaml("no_such_file.yaml")
