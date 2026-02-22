import pytest
from pathlib import Path
from pet.macros.data.env import env

FIXTURE = Path(__file__).parent / "env" / "sample.env"


@pytest.fixture
def e():
    return env(str(FIXTURE))


# --- unquoted values ---------------------------------------------------------

def test_unquoted_string(e):
    assert e.get('DATABASE_URL') == 'postgres://localhost/mydb'

def test_unquoted_boolean(e):
    assert e.get('DEBUG') == 'true'

def test_unquoted_integer(e):
    assert e.get('PORT') == '3000'

def test_unquoted_log_level(e):
    assert e.get('LOG_LEVEL') == 'INFO'


# --- quoted values -----------------------------------------------------------

def test_double_quoted_value(e):
    assert e.get('APP_NAME') == 'my-app'

def test_single_quoted_value(e):
    assert e.get('SECRET_KEY') == 'supersecret'


# --- comment lines are ignored -----------------------------------------------

def test_hash_comment_not_a_key(e):
    assert e.get('# Application environment') is None


# --- missing key -------------------------------------------------------------

def test_missing_key_returns_none(e):
    assert e.get('NONEXISTENT') is None


# --- iteration ---------------------------------------------------------------

def test_iter_yields_tuples(e):
    pairs = list(e)
    assert all(isinstance(k, str) and isinstance(v, str) for k, v in pairs)

def test_iter_contains_expected_keys(e):
    keys = [k for k, _ in e]
    assert 'DATABASE_URL' in keys
    assert 'APP_NAME' in keys
    assert 'SECRET_KEY' in keys

def test_iter_count(e):
    assert len(list(e)) == 6


# --- __str__ -----------------------------------------------------------------

def test_str_is_empty(e):
    assert str(e) == ''


# --- error handling ----------------------------------------------------------

def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        env("no_such_file.env")
