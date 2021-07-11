# [Tests](https://docs.python-guide.org/writing/tests/)

<!-- TOC depthFrom:2 depthTo:3 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Terminology](#terminology)
- [Choosing a Test Runner](#choosing-a-test-runner)
	- [[unittest](https://docs.python.org/3/library/unittest.html)](#unittesthttpsdocspythonorg3libraryunittesthtml)
	- [[nose](https://pythontesting.net/framework/nose/nose-introduction/)](#nosehttpspythontestingnetframeworknosenose-introduction)
	- [[pytest](https://docs.pytest.org/en/latest/contents.html)](#pytesthttpsdocspytestorgenlatestcontentshtml)
	- [Final Pick:](#final-pick)
- [Structuring the `tests` Directory](#structuring-the-tests-directory)
- [Writing Tests](#writing-tests)
	- [Using Classes](#using-classes)
- [Running Tests](#running-tests)
	- [Run All vs Run Single Class vs Run Single Test](#run-all-vs-run-single-class-vs-run-single-test)
	- [Running Tests in PyCharm](#running-tests-in-pycharm)

<!-- /TOC -->

## Terminology
Tests for your code can be written to check either a small snippet of code or to check whether multiple modules are working together properly. A test that checks a single component or method is called a **unit test** while a test that checks the output as a result of multiple functions or modules is called an **integration test**. Here we will focus on unit tests, but you may also right integration tests should you so choose.

## Choosing a Test Runner
There are multiple test runners for Python, but the three most popular are:
* [`unittest`](#unittest)
* [`nose`](#nose) or `nose2`
* [`pytest`](#pytest)

### [unittest](https://docs.python.org/3/library/unittest.html)
#### Advantages
* builtin library

#### Disadvantages
* Strict requirements for writing tests

### [nose](https://pythontesting.net/framework/nose/nose-introduction/)
#### Advantages
* Can recognize and run all tests written for `unittest`
* Allows for more flexible writing of tests

#### Disadvantages
* `nose` is no longer maintained so everyone is now switching to `nose2`
* `nose2` does not have the best documentation

### [pytest](https://docs.pytest.org/en/latest/contents.html)
#### Advantages
* Great support and widely used
* Highest functionality
* Simplest testing runner to pick up and use

#### Disadvantages
* Not a builtin library so must be installed separately

### Final Pick:
For this class, we will be using `pytest` due to its popularity and great documentation.


## Structuring the `tests` Directory
You will find that cookiecutter already made a `tests` folder in your package template directory. Inside you will find an `__init__` file to indicate that it is a python module as well as a `test_*.py` file. The name of this file will vary depending on your package name. Here we will discuss how you should restructure your `tests` folder so that it follows the proper guidelines.

The typical convention for creating tests in a software package is that all directories, files, and methods that are/contain a test should be named with `test_` at the beginning or end in `_test`. If you have different folders in your package (e.g. a preprocessing folder containing modules related to preprocessing and a sql folder with modules pertaining to querying your database) then you should also structure your tests as such. Here is an example of a software package with tests (the docs folder was rmeove to shrink the output a bit):
```
$ cd my_new_package/
$ tree
├── AUTHORS.rst
├── CONTRIBUTING.rst
├── HISTORY.rst
├── LICENSE
├── MANIFEST.in
├── my_new_package
│   ├── cli.py
│   ├── database
│   │   ├── __init__.py
│   │   └── query.py
│   ├── __init__.py
│   └── preprocessing
│       ├── download.py
│       ├── __init__.py
│       ├── insert.py
│       └── normalize.py
├── README.rst
├── requirements_dev.txt
├── setup.cfg
├── setup.py
├── tests
│   ├── __init__.py
│   ├── test_database
│   │   ├── __init__.py
│   │   └── test_database.py
│   └── test_preprocessing
│       ├── __init__.py
│       └── test_preprocessing.py
└── tox.ini
```

**IMPORTANT** Here you will notice the actual software package has 3 modules in the `preprocessing` folder: `download`, `insert`, and `normalize`, but we only have one test file for all three: `test_preprocessing.py`. You can choose to gather all tests for a submodule into separate files (e.g. `test_download.py`, `test_insert.py`, and `test_normalize.py`) or have all of your tests in one file but separate the tests for each submodule within this one file using classes. We will discuss this in the [next section](#writing-tests).

## Writing Tests
Once we have created the proper structure for our tests, we can open up one of the test files and begin writing the actual tests themselves.

`assert` is the primary method of testing components in python. Assertions written within a test function return either a True or False value and when an assertion fails in a test method, then that method execution is stopped there. The remaining code in that test method is not executed, and `pytest` will continue with the next test method.

First, let's say we want to test our `download_file` method in our preprocessing module as defined here:
```python
"""Module for downloading necessary files"""
import os
import requests  # Library for downloading files

from ..constants import DATA_DIR  # Import file path where downloaded data is stored
# DATA_DIR in this example == '/home/bschultz/tmp/'


def download_file(url: str) -> str:
    file_name = os.path.basename(url)
    r = requests.get(url)

    downloaded_file_path = os.path.join(DATA_DIR, file_name)

    with open(downloaded_file_path, 'wb') as d_file:
      d_file.write(r.content)

    return downloaded_file_path
```

Now to write a test function in our `test_download.py` file that checks:
* The returned path is what we expect
* A file exists at the returned path
* The downloaded file path contains information

```python
import os

from my_new_package.preprocessing.download import download_file

def test_download_file():
    test_url = "http://www.informatics.jax.org/downloads/reports/MRK_ENSEMBL.rpt"  # Mouse genes
    download_path = download_file(test_url)

    assert download_path == "/home/bschultz/tmp/MRK_ENSEMBL.rpt"  # Check if path is right
    assert os.path.exists(download_path) is True  # Check if file is there
    assert os.stat(download_path).st_size != 0  # Check if file is not empty
```

### Using Classes
In our [above example](#structuring-the-tests-directory) we had 3 modules in our preprocessing subdirectory. While we could make three separate test files which includes tests for each of the preprocessing modules respectively, we could instead include tests for all of them in one test file (`test_preprocessing.py`) and separate them using classes.

The naming convention for test classes is to use camel case and each class with testing functions should start with `Test` followed by the module name. So if we were to structure our tests like this, our `test_preprocessing.py` would like something like this:

```python
"""Collection of tests for all preprocessing modules"""
import os

from my_new_package.preprocessing.download import download_file

class TestDownload:

    def test_download_file(self):
        test_url = "http://www.informatics.jax.org/downloads/reports/MRK_ENSEMBL.rpt"  # Mouse genes
        download_path = download_file(test_url)

        assert download_path == "/home/bschultz/tmp/MRK_ENSEMBL.rpt"  # Check if path is right
        assert os.path.exists(download_path) is True  # Check if file is there
        assert os.stat(download_path).st_size != 0  # Check if file is not empty


class TestNormalize:

    def test_some_normalizing_function(self):
        ...
```

## Running Tests
Finally, we want to run all of our tests. Perform the following:
* Activate your virtual environment
* Make sure you have `pytest` install (`pip install pytest`)
* Navigate to the root directory of your package
* Make sure your `tests` is located in the root directory and structured properly

### Run All vs Run Single Class vs Run Single Test

* all tests:
```
pytest
```
* only 1 test file
```
pytest path/to/file.py
```
* only 1 class in 1 test file
```
pytest path/to/file.py::ClassName
```
* only 1 method of a class in 1 test file
```
pytest path/to/file.py::ClassName::methodName
```

### Running Tests in PyCharm
To set up PyCharm to run your tests, perform the following steps:
* Go to Settings (Ctrl+Alt+S) --> Tools --> Python Integrated Tools
* Choose `pytest` as the "Default test runner"
* Click "Apply"/"OK"
* Close the Settings Window

Next:
* Click on your "tests" folder so it is highlighted in your Project pane
* Click on the top: Run --> Edit Configurations...
* Click: "Python tests" then click the "+" symbol in the top left
* Python tests --> pytest
* A window should pop up. On the right side enter the path of your "tests" folder in the Target box (you can click the folder symbol to choose the directory)
* Click OK

Now in PyCharm, you should be able to select "pytest in tests" from the drop down menu in the top right and run it.

#### Running a Single Test in PyCharm
If you wish to run a single test in PyCharm:
* Go to the test in the file
* Right click the test function
* Click "Run 'pytest for test_...'"
* Done!
