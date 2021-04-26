# Style Guide
This document describes the syntax and good practices used for the development of the Data Mass project. Only the practices that we consider essential to maintain a clean and maintainable code are listed, with no strict criteria of code style, since the intention is to be receptive to contributions from third parties. No one has a duty to know every single good Python practice.

## Contents:
  - [Overview](#overview)
  - [Docstring standard](#docstring-standard)
    - [Examples](#examples)
    - [VSCode Python Docstring Generator plugin](#vscode-python-docstring-generator-plugin)
  - [Import convention](#import-convention)
  - [String formatting](#string-formatting)
  - [Long code line](#long-code-line)
  - [Line per module](#line-per-module)
  - [Terminal appearance customization](#terminal-appearance-customization)
  - [Others good practices](#others-good-practices)
  - [Pre-commit validations](#pre-commit-validations)

## [Overview](#overview)
We mostly follow the standard Python style conventions as described here:
 - [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
 - [Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)

Use a code checker:
[pylint](https://pypi.org/project/pylint/): a Python static code analysis tool.
[flake8](https://pypi.python.org/pypi/flake8/): a tool that glues together `pycodestyle`, `pyflakes`, `mccabe` to check the style and quality of Python code.

### [Docstring standard](#docstring-standard)
In the project, the numpy standard was adopted for writing documentation of the methods, which provides for consistency, while also allowing a toolchain to produce well-formatted reference guides. You can read more about this standard on the [official website](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard) of the project.

#### [Examples](#examples-of-docstring)
**Parameters**
Description of the function arguments, keywords and their respective types.
```python
Parameters
----------
x : type
	Description of parameter `x`.
y
	Description of parameter `y` (with type not specified). 
```
Enclose variables in single backticks. The colon must be preceded by a space, or omitted if the type is absent.

For the parameter types, be as precise as possible. Below are a few examples of parameters and their types.
```python
Parameters
----------
filename : str
copy : bool
dtype : data-type
iterable : iterable object
shape : int or tuple of int
files : list of str
```
If it is not necessary to specify a keyword argument, use `optional`:
```python
x : int, optional
```

**Returns**
Explanation of the returned values and their types. Similar to the **Parameters** section, except the name of each return value is optional. The type of each return value is always required:
```python
Returns
-------
int
    Description of anonymous integer return value.
```

If both the name and type are specified, the **Returns** section takes the same form as the **Parameters** section:
```python
Returns
-------
err_code : int
    Non-zero value indicates error code, or zero on success.
err_msg : str or None
    Human readable error message, or None on success.
```

**Raises**
An optional section detailing which errors get raised and under what conditions:
```python
Raises
------
KeyError
    If the key does not exists.
```
This section should be used judiciously, i.e., only for errors that are non-obvious or have a large chance of getting raised.

**Notes**
An optional section that provides additional information about the code, possibly including a discussion of the algorithm.
```python
Notes
-----
The FFT is a fast implementation of the discrete Fourier transform:
```
#### [VSCode Python Docstring Generator Plugin](#vscode-plugin)
If you are a Visual Studio Code user, install [**Python Docstring Generator**](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) plugin that automatically generates docstring patterns, including numpy. To install and configure just follow these steps:

**Plug-in installation**:

Through terminal:
1. Open VSCode and press `Ctrl + P` and type the following command:
```terminal
ext install njpwerner.autodocstring
```
Through UI:
1. Open VSCode press `Ctrl + Shift + X`, search for **Python Docstring Generator**
2.  Install the plugin

**Plug-in configuration**:

1. With VSCode open, press `Ctrl +,` (plus comma)
2. In the search bar, search for "@ext: njpwerner.autodocstring"
3. In the "Auto Docstring: Docstring Format" section, change to "numpy"

**Using the plug-in**:

When defining a function, type three quotes and press "Enter" and the plugin will generate the docstring.

### [Import convention](#import-convention)
When importing any module created within `data_mass`, choose to [use absolute import instead of relative import](https://www.python.org/dev/peps/pep-0328/#guido-s-decision). Relative assets are confusing, as they vary from the path you are in, and thus there are major changes to a bug being generated.

Use
```Python
from data_mass.user.authentication import authenticate_user_iam
```
Over :
```Python
from ..user.authentication import authenticate_user_iam 
```
Also, imports should usually be on separate lines:
```python
# Correct:
import os
import sys

# Wrong:
import sys, os
```
If you need to import many methods and do not fit the line limit, that is, 79 characters, you may break into multiple lines:
```python
from data_mass.user.assertion import (
	assert_logon_request,
	assert_response_error,
	assert_email_request,
)
```

### [String formatting](#string-formatting)
When displaying the value of a variable in the middle of a print statement, choose to use the [f-string](https://docs.python.org/3/tutorial/inputoutput.html) instead of the `.format()` and the standard concatenation (using the "+" symbol). With this, we prevent our modules from having very long lines.
```python
name, last_name =  "foo",  "barz"

# Bad
print("Hello {name} {last_name}".format(name=name, last_name=last_name))

# Also Bad
print("Hello " + name + " " + last_name)

# Good
print(f"Hello {name} {last_name}")
```

### [Long code line](#long-code-line)
According to PEP8, [the recommended length for each 79-character line](https://www.python.org/dev/peps/pep-0008/#maximum-line-length). Limiting the required editor window width makes it possible to have several files open side by side, and works well when using code review tools that present the two versions in adjacent columns.
```python
with open('/path/to/some/file/you/want/to/read') as file_1, \
     open('/path/to/some/file/being/written', 'w') as file_2:
    file_2.write(file_1.read())
```
With binary operator:
```python
# Correct:
# easy to match operators with operands
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)
```

### [Line per module](#line-per-module)
A good practice is to maintain a legal module, either by formatting the code and by the number of lines contained in it. We recommend that each module has up to 300 lines, however, if the logic of the extra code fits only to that module, then there is no problem in extending this limit. Now, if your module has reached the maximum (in the maximum limit, seriously) of 1000 lines, it is essential to create another module, or even a package.

### [Terminal appearance customization](#terminal-appearance-customization)
If it is necessary to add some style to the terminal (e.g. bold character, color red on the words, tabulate data viewer, etc), it is mandatory to use the [rich](https://github.com/willmcgugan/rich) library, which offers all these features.

### [Others good practices](#others-good-practices)
- Do not leave commented source code
- If the implemented logic is a little confusing, we encourage you to make the necessary amount of comments in the code
- When representing a truth value of an expression (i.e. True and False), choose to use the built-in type boolean instead of string. Example:
	```python
	# Bad
	is_integer_value = lambda num: "true" if int(num) else "false"
	# Good
	is_integer_value = lambda num: True if int(num) else False
	```
- Methods that are called from other .py files MUST have Docstring

### [Pre-commit validations](#pre-commit-validations)
To keep the code clean and maintainable, we added some validation of code linter before a commit is uploaded. For that, it was necessary to use Pyhon's [pre-commit library](https://github.com/pre-commit/pre-commit). The modules and packages that are in the evaluations, can be found in the file `.pre-commit-config.yaml` at the root of the project. Basically, the modules and packages added are those that have already been refactored by the Data Mass team.

**Do you have any tips or doubt? Tell us through Slack!**
