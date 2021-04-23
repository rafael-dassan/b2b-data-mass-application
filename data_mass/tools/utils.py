"""Utils tools for Data Mass use."""
import json
import sys
from datetime import date
from os import devnull, system
from typing import Any, Hashable, Union

from jsonpath_rw import Fields, Index
from jsonpath_rw_ext import parse


def clear_terminal() -> None:
    """
    Clear the terminal
    """
    system("clear")


def finish_application() -> None:
    """
    Kill the application.
    """
    sys.exit()


def update_value_to_json(
        json_object: dict,
        json_path: str,
        new_value: Any) -> dict:
    """
    Update value to JSON using JSONPath.

    Parameters
    ----------
    json_object: dict
        JSON as a dictionary object.
    json_path: str
        JSONpath expression.
    new_value: Any
        Value to update.

    Returns
    -------
    dict
        The new `json_object`.
    """
    json_path_expr = parse(json_path)

    for match in json_path_expr.find(json_object):
        path = match.path
        if isinstance(path, Index):
            match.context.value[match.path.index] = new_value
        elif isinstance(path, Fields):
            match.context.value[match.path.fields[0]] = new_value
    return json_object


def convert_json_to_string(json_object: dict) -> str:
    """
    Convert JSON object to string.

    Parameters
    ---------
    json_object: dict
        JSON as a dictionary object.

    Returns
    -------
    str
        JSON to string.
    """
    # TODO: stop using this method and use `json.dumps` directly
    return json.dumps(json_object)


def create_list(*items) -> list:
    """
    Create a list from a series of given values.

    Returns
    -------
    list
        A list containing given items.

    Notes
    -----
    The returned list can be assigned both to ``${scalar}`` and ``@{list}`` \
    variables.
    """
    # TODO: stop using this method and use list conversion directly
    return [items]


def is_blank(string: str) -> bool:
    """
    Check if a given string is empty.

    Parameters
    ----------
    string : str

    Returns
    -------
    bool
        Whenever a string is empty or not.
    """
    # TODO: stop using this method use Python's Falsy value check
    return not (string and string.strip())


def return_first_and_last_date_year_payload():
    """
    Return first and last day in the year.

    Returns
    -------
    dict
        A dict with the start and end date.
    """
    first_date = date(date.today().year, 1, 1)
    first_date = first_date.strftime("%Y-%m-%d")
    last_date = date(date.today().year, 12, 31)
    last_date = last_date.strftime("%Y-%m-%d")

    return {"startDate": first_date, "endDate": last_date}


def set_to_dictionary(
        dictionary: dict,
        *key_value_pairs: Hashable,
        **items: Any) -> dict:
    """
    Adds the given `key_value_pairs` and `items` to the `dictionary`. \
    Giving items as `key_value_pairs` means giving keys and values \
    as separate arguments.

    Parameters
    ----------
    dictionary : dict
    *key_value_pairs

    Returns
    -------
    dict
        A new dictionary.

    Examples
    -------
    | Set To Dictionary | ${D1} | key | value | second | ${2} |
    =>
    | ${D1} = {'a': 1, 'key': 'value', 'second': 2}
    | Set To Dictionary | ${D1} | key=value | second=${2} |

    The latter syntax is typically more convenient to use, but it has
    a limitation that keys must be strings.
    If given keys already exist in the dictionary, their values are updated.
    """

    if len(key_value_pairs) % 2 != 0:
        raise ValueError(
            "Adding data to a dictionary failed."
            "There should be even number of key-value-pairs."
        )

    for i in range(0, len(key_value_pairs), 2):
        dictionary[key_value_pairs[i]] = key_value_pairs[i + 1]

    dictionary.update(items)

    return dictionary


def block_print():
    """
    Overwrite standard output (stdout).
    """
    sys.stdout = open(devnull, 'w')


def find_values(key: Hashable, json_str: str) -> Union[None, Any]:
    """
    Find values in a dictionary.

    Parameters
    ----------
    key : Hashable
    json_str : str

    Returns
    -------
    None
        If the key does not exist.
    json_str[key] : Any
        The key's value.
    """
    # TODO: use builtin methods to check if there is a
    # key in a dict instead of that method.
    results = []

    def _decode_dict(a_dict):
        try:
            results.append(a_dict[key])
        except KeyError:
            pass
        return a_dict

    json.loads(json_str, object_hook=_decode_dict)

    if len(results) == 0:
        return None

    return results[0]


def remove_from_dictionary(dictionary: dict, *keys: Any) -> None:
    """
    Removes the given `keys` from the `dictionary`.

    Parameters
    ----------
    dictionary : dict

    Example
    -------
    | Remove From Dictionary | ${D3} | b | x | y |
    =>
    | ${D3} = {'a': 1, 'c': 3}

    Notes
    -----
    If the given `key` cannot be found from the `dictionary`, it \
    is ignored.
    """
    if is_string(dictionary) or isinstance(dictionary, (int, float)):
        raise TypeError(
            "Expected argument to be a dictionary or "
            f"dictionary-like, got {type(dictionary)} instead."
        )

    for key in keys:
        if key in dictionary:
            dictionary.pop(key)


def is_string(string: Any) -> bool:
    """
    Verify if a given value is type of str.

    Parameters
    ----------
    string : str

    Returns
    -------
    bool
        Whevener a given value is str.
    """
    return isinstance(string, str)
