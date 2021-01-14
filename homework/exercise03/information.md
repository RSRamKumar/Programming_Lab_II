### Background Information
#### [Typing](https://docs.python.org/3/library/typing.html)

##### Overview

In comparison to statically-typed languages (e.g. Java), Python is a dynamically-typed language that allows variables to be coerced to different data types. While this allows a large amount of freedom, it can cause headaches when you are expecting a function to return a string and it gives you an integer instead. Python does not force users to declare variable types, but as helpful, courteous programmers we will make sure to define each argument type in our functions and what type of data structure to expect to be returned. For example:

```python
def add_one(my_number: int) -> int:
  return mynumber + 1
```

In the above example we declare that the positional argument `my_number` should be an integer and that the function should also return an integer. When python runs the code, it will not check the data types, but PyCharm will warn you if it detects a clash between what is passed vs what is expected. It also helps to more quickly provide information to your teammates and users.

**Hint -** Typing can be used with all argument types and even when no return is expected:
```python
def greet_me(name: str, greeting: str = "Good morning") -> None:
  print(greeting + " " + name)
```

##### Pandas
Typing can be used with any data type!
```python
import pandas as pd

def simple_df() -> pd.DataFrame:
  return pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))

simple_df()
#    A  B
# 0  1  2
# 1  3  4
```

##### Advanced Typing
###### [Typing Library](https://docs.python.org/3/library/typing.html)
You will often come across the fact that the basic data python structures (`int`, `str`, `list`, `dict`, `set`, etc) don't suffice or you want to be more specific. The [`typing` library](https://docs.python.org/3/library/typing.html) can help to give you more control:

```python
from typing import List, Iterable, Union

# You return a LIST that should contain a specific data type within
def sequence(start: int, stop: int) -> List[int]:
  """Returns a list of integers between start and stop"""
  return [i for i in range(start, stop)]

# Iterable can be any iterable data structure (e.g. list, set, etc)
def sequence(start: int, stop: int) -> Iterable[int]:
  """Returns a set of integers between start and stop"""
  return {i for i in range(start, stop)}

# Union is used for when multiple data types are acceptable
def lets_count(number: Union[str, int]) -> None:
  print(f"Let's count to {7}")
  print(f"Let's count to {'7'}")  # Exactly the same output

```

#### [Documentation](https://realpython.com/documenting-python-code/)
Ever wonder why the people on StackOverflow know so much about all of these methods you use every day? They read the documentation! Documenting your code is vital not only for describing to new users how to properly use your code, but also so others in your group know how to use the code you wrote.  

Documenting your code is something that you should as you write the code (often you write a method and a week later you forget what it does/generates). A [docstring](https://www.python.org/dev/peps/pep-0257/) is a multi-line string (triple quotes!) that appears directly after your function name (inside the function). At a minimum, it should describe what the function does:

```python
def say_my_name(name: str) -> None:
  """Prints the name passed to the function."""
  print(f"You are {name}")

say_my_name("Groot")

>>> You are Groot
```

For such a simple example, a description is usually enough, but when you have more complicated functions it is best to give detailed descriptions of what the function does, each of the parameters, and what it should return:

```python
def square_it(start: int, stop: int) -> dict:
  """Iterates through a range of integers from start to stop and generates a dictionary with each integer and its square value.

  :param start: Number to start iterating from.
  :type start: int
  :param stop: Number to stop at.
  :type stop: int

  :return: Dictionary of integers (keys) and their squares (values) ranging from the start value to the stop value.
  :rtype: dict
  """
  return {i: i*i for i in range(start, stop)}
```

This style of writing your docstring is known as the `reStructuredText` format, however there are many others including `Numpy` and `Google`. For this class, you should use the `reStructuredText` format, but if you wish to read more, check out this [site](https://realpython.com/documenting-python-code/).

#### [Decorators](https://www.programiz.com/python-programming/decorator)
Decorators are essentially nested functions that serve to modify the behavior of a different, associated function. They are very useful as they simply the way we generate new methods that require some kind of input or output formatting. For example, say we wish to simply enclose a the output string from a given method:

```python
def enclose(func):

    def wrapper(val):

        print("***************************")
        func(val)
        print("***************************")

    return wrapper

@enclose
def extract_evidence(document_string: str) -> str:
  # Code that parses a document's content and extracts an evidence sentence
  print(evidence)

extract_evidence(content)
```
```
***************************
My line of evidence.
***************************
```
What is happening here, is that the `enclose` method takes some function (`func`) as input and performs some action on it (here it is adding print statments of `*` around our line of evidence). The `enclose` method is then used as a decorator (shown here as `@enclose`) for the `extract_evidence` function. While this may seem like extra work, it allows one to modify another method or class without permanently changing what that method/class actually does. Users do not have to build multiple versions of a function to achieve different results if they know how to design decorators.

##### [Click](https://click.palletsprojects.com/en/7.x/)
The click library is an incredibly useful python library for generating advanced and sophisticated command line interfaces (CLIs) in a short amount of time. This library heavily relies on the use of decorators for modifying the CLI commands themselves. Users can use Click to quickly add input parameters, help documentation, boolean flags, and many other features to their CLI.
