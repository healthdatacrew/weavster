from weavster.utils import to_snake_case


def test_camel_case_to_snake_case():
    """
    Test conversion of a camelCase string to snake_case.
    """
    assert to_snake_case("myCamelCaseString") == "my_camel_case_string"


def test_pascal_case_to_snake_case():
    """
    Test conversion of a PascalCase string to snake_case.
    """
    assert to_snake_case("MyPascalCaseString") == "my_pascal_case_string"


def test_already_snake_case():
    """
    Test that an already snake_case string remains unchanged.
    """
    assert to_snake_case("already_snake_case") == "already_snake_case"


def test_single_word_string():
    """
    Test conversion of a single-word string.
    """
    assert to_snake_case("singleword") == "singleword"
    assert to_snake_case("Word") == "word"


def test_empty_string():
    """
    Test conversion of an empty string.
    """
    assert to_snake_case("") == ""


def test_string_with_numbers():
    """
    Test conversion of a string containing numbers.
    """
    assert to_snake_case("myString123Test") == "my_string123_test"
    assert to_snake_case("Test123Case") == "test123_case"


def test_string_with_acronyms():
    """
    Test conversion of a string with consecutive uppercase letters (acronyms).
    Note: The current regex treats each capital letter individually.
    """
    assert to_snake_case("HTTPRequest") == "h_t_t_p_request"
    assert to_snake_case("APICall") == "a_p_i_call"
    assert to_snake_case("CLIParser") == "c_l_i_parser"


def test_string_with_leading_and_trailing_spaces():
    """
    Test handling of strings with leading or trailing spaces (though the function doesn't trim).
    """
    assert to_snake_case("  TrimMe") == "  _trim_me"  # Expected based on current regex
    assert to_snake_case("  TrimMe  ") == "  _trim_me  "
    assert to_snake_case("NoSpaces") == "no_spaces"  # Baseline for comparison


def test_string_with_mixed_cases_and_symbols():
    """
    Test a more complex string with mixed cases and symbols (though symbols won't change).
    """
    assert to_snake_case("fileName.txt") == "file_name.txt"
    assert to_snake_case("another-FileName") == "another-_file_name"  # Hyphens and existing underscores are untouched
