import pytest
from pathlib import Path
from pet.macros.data.properties import properties

FIXTURE = Path(__file__).parent / "properties" / "sample.properties"


@pytest.fixture
def cfg():
    return properties(str(FIXTURE))


# --- scalar values -----------------------------------------------------------

def test_equals_separator(cfg):
    assert cfg.get('server.host') == 'localhost'

def test_integer_as_string(cfg):
    assert cfg.get('server.port') == '8080'

def test_dotted_key_is_literal(cfg):
    assert cfg.get('app.name') == 'my-app'

def test_app_version(cfg):
    assert cfg.get('app.version') == '1.0.0'

def test_db_url(cfg):
    assert cfg.get('db.url') == 'jdbc:postgresql://localhost/mydb'


# --- colon separator ---------------------------------------------------------

def test_colon_separator(cfg):
    assert cfg.get('log.level') == 'INFO'

def test_colon_separator_path(cfg):
    assert cfg.get('log.file') == '/var/log/app.log'


# --- comment lines are ignored -----------------------------------------------

def test_hash_comment_not_a_key(cfg):
    assert cfg.get('# Application configuration') is None

def test_bang_comment_not_a_key(cfg):
    assert cfg.get('! database settings') is None


# --- missing key -------------------------------------------------------------

def test_missing_key_returns_none(cfg):
    assert cfg.get('nonexistent') is None

def test_no_dot_splitting(cfg):
    # 'server' alone is not a key; dots are NOT navigation separators
    assert cfg.get('server') is None


# --- iteration ---------------------------------------------------------------

def test_iter_yields_tuples(cfg):
    pairs = list(cfg)
    assert all(isinstance(k, str) and isinstance(v, str) for k, v in pairs)

def test_iter_contains_expected_keys(cfg):
    keys = [k for k, _ in cfg]
    assert 'server.host' in keys
    assert 'log.level' in keys

def test_iter_count(cfg):
    assert len(list(cfg)) == 9


# --- __str__ -----------------------------------------------------------------

def test_str_is_empty(cfg):
    assert str(cfg) == ''


# --- error handling ----------------------------------------------------------

def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        properties("no_such_file.properties")
