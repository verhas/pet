import pytest
from pathlib import Path
from pet.macros.data.toml import toml

FIXTURE = Path(__file__).parent / "toml" / "config.toml"


@pytest.fixture
def cfg():
    return toml(str(FIXTURE))


# --- scalar values -----------------------------------------------------------

def test_top_level_string(cfg):
    assert cfg.get('project.name') == 'my-app'

def test_top_level_version(cfg):
    assert cfg.get('project.version') == '1.0.0'

def test_nested_scalar(cfg):
    assert cfg.get('server.host') == 'localhost'

def test_nested_integer(cfg):
    assert cfg.get('server.port') == 8080


# --- nested table returns wrapper --------------------------------------------

def test_nested_table_returns_toml(cfg):
    result = cfg.get('server')
    assert isinstance(result, toml)

def test_nested_table_further_query(cfg):
    server = cfg.get('server')
    assert server.get('host') == 'localhost'
    assert server.get('port') == 8080


# --- array of tables (TOML [[section]]) -------------------------------------

def test_array_of_tables_returns_list(cfg):
    result = cfg.get('dependencies')
    assert isinstance(result, list)
    assert len(result) == 2

def test_array_elements_are_wrapped(cfg):
    deps = cfg.get('dependencies')
    assert all(isinstance(d, toml) for d in deps)

def test_iterate_array_and_query(cfg):
    names = [dep.get('name') for dep in cfg.get('dependencies')]
    assert names == ['requests', 'flask']

def test_array_index_access(cfg):
    assert cfg.get('dependencies.0.name') == 'requests'
    assert cfg.get('dependencies.1.version') == '2.3.0'


# --- list of scalars ---------------------------------------------------------

def test_list_of_scalars(cfg):
    assert cfg.get('tags.values') == ['web', 'api', 'rest']


# --- real pyproject.toml -----------------------------------------------------

def test_reads_own_pyproject():
    root = Path(__file__).parent.parent / "pyproject.toml"
    proj = toml(str(root))
    assert proj.get('project.name') == 'pet-doc'
    assert proj.get('build-system.build-backend') == 'hatchling.build'


# --- missing path ------------------------------------------------------------

def test_missing_key_returns_none(cfg):
    assert cfg.get('nonexistent') is None

def test_missing_nested_key_returns_none(cfg):
    assert cfg.get('server.nonexistent') is None

def test_out_of_bounds_index_returns_none(cfg):
    assert cfg.get('dependencies.99.name') is None


# --- __str__ -----------------------------------------------------------------

def test_str_of_scalar(cfg):
    assert str(cfg.get('project.version')) == '1.0.0'

def test_str_of_table_wrapper_is_empty(cfg):
    assert str(cfg.get('server')) == ''


# --- error handling ----------------------------------------------------------

def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        toml("no_such_file.toml")
