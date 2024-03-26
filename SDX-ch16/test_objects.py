from io import StringIO
from textwrap import dedent

from objects import SaveObjects, LoadObjects

def test_save_bool_single(s, l):
    output = StringIO()
    s.save(output, True)
    assert output.getvalue() == "bool:True\n"


def test_save_dict_empty(s, l):
    output = StringIO()
    s.save(output, {})
    assert output.getvalue() == "dict:0\n"


def test_save_dict_flat(s, l):
    fixture = {"alpha": "beta", 1: 2}
    expected = dedent("""\
    dict:2
    str:1
    alpha
    str:1
    beta
    int:1
    int:2
    """)
    output = StringIO()
    s.save(output, fixture)
    assert output.getvalue() == expected


def test_save_float_single(s, l):
    output = StringIO()
    s.save(output, 1.23)
    assert output.getvalue() == "float:1.23\n"


def test_save_int_single(s, l):
    output = StringIO()
    s.save(output, -456)
    assert output.getvalue() == "int:-456\n"


# [test_save_list_flat]
def test_save_list_flat(s, l):
    fixture = [0, False]
    expected = dedent("""\
    list:2
    int:0
    bool:False
    """)
    output = StringIO()
    s.save(output, fixture)
    assert output.getvalue() == expected
# [/test_save_list_flat]


def test_save_str_single(s, l):
    fixture = dedent("""\
    a
    b
    c
    """)
    expected = dedent("""\
    str:4
    a
    b
    c

    """)
    output = StringIO()
    s.save(output, fixture)
    assert output.getvalue() == expected


def test_save_set_flat(s, l):
    fixture = {1, "a"}
    first = dedent("""\
    set:2
    int:1
    str:1
    a
    """
    )
    second = dedent("""\
    set:2
    str:1
    a
    int:1
    """
    )
    output = StringIO()
    s.save(output, fixture)
    actual = output.getvalue()
    assert actual in {first, second}


def test_load_bool_single(s, l):
    fixture = StringIO("bool:True\n")
    assert l.load(fixture) == True


def test_load_dict_empty(s, l):
    fixture = StringIO("dict:0\n")
    assert l.load(fixture) == {}


def test_load_dict_flat(s, l):
    fixture = StringIO(
        dedent("""\
        dict:2
        str:1
        alpha
        str:1
        beta
        int:1
        int:2
        """)
    )
    assert l.load(fixture) == {"alpha": "beta", 1: 2}


def test_load_float_single(s, l):
    fixture = StringIO("float:1.23\n")
    assert l.load(fixture) == 1.23


def test_load_int_single(s, l):
    fixture = StringIO("int:-456\n")
    assert l.load(fixture) == -456


def test_load_list_flat(s, l):
    fixture = StringIO(
        dedent(
            """\
    list:2
    int:0
    bool:False
    """
        )
    )
    assert l.load(fixture) == [0, False]


def test_load_str_single(s, l):
    fixture = StringIO(
        dedent(
            """\
    str:4
    a
    b
    c

    """
        )
    )
    expected = dedent(
        """\
    a
    b
    c
    """
    )
    assert l.load(fixture) == expected


def test_load_set_flat(*s, l):
    fixture = StringIO(
        dedent(
            """\
    set:2
    int:1
    str:1
    a
    """
        )
    )
    assert l.load(fixture) == {1, "a"}


def test_roundtrip(s, l):
    fixture = ["a", {"b": 987.6}, {"c", True}]
    output = StringIO()
    s.save(output, fixture)
    archive = output.getvalue()
    result = l.load(StringIO(archive))
    assert result == fixture

### Test runner
import time

def run_tests():
    results = {"pass": 0, "fail": 0, "error": 0}
    s = SaveObjects()
    l = LoadObjects()
    for (name, test) in globals().items():
        if not name.startswith("test_"):
            continue
        try:
            test(s, l)
            results["pass"] += 1
        except AssertionError:
            results["fail"] += 1
        except Exception:
            results["error"] += 1
    print(f"pass {results['pass']}")
    print(f"fail {results['fail']}")
    print(f"error {results['error']}")

if __name__ == '__main__':
    run_tests()
