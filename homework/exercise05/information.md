### Background Information
#### Utility Methods
Often when designing software, there are certain functions which you want to utilize throughout your package development. These types of tasks include parsing strings for information, casting commonly used data structures to a different one, downloading or reading files, or performing calculations on specific objects. If you find yourself using the same method across multiple modules/files, rather than creating several specific, slightly modified version of the same function in each module, it is better practice to design a general form of the method and store it in a file of other general methods. Typically, this file is called `utils.py` and is comprised of a collection of general helper functions.

#### Tracking Progress using [tqdm](https://tqdm.github.io/)
Iterating through a list in python is a routine task, but often when executing code on a large array of items, it may become useful to track its progress. One very useful library in Python is called `tqdm`, and is used to create a visual progress bar that tracks how far along in the loop the code has progressed. Tqdm can be used with almost any iterable object in Python, and though the library is often quite good at determining the total number of items in an array, it sometimes is necessary to explicitly state the total number of items using the `total=` parameter. Below is an example of how to use tqdm.

```python
from tqdm import tqdm

for i in tqdm(range(100)):
    # execute some code
    pass

for person in tqdm(names_list, desc="Parsing people", total=len(names_list)):
    # Iterate through names_list and execute code on person
    pass
```


#### [Logging](https://realpython.com/python-logging/)
##### Severity Levels
Logging specific information has several advantages, and depending on the type of information, one can set the "severity" level of the logging entry in order to quickly identify the important lines in their log file as well as control what is printed to the terminal.

```python
import logging

logging.debug("This is a debug message")
logging.info("This is an informational message")
logging.warning("Careful! Something does not look right")
logging.error("You have encountered an error")
logging.critical("You are in trouble")
```

When we run the above code, we get something like this.

```
> WARNING:root:Careful! Something does not look right
> ERROR:root:You have encountered an error
> CRITICAL:root:You are in trouble
```

Notice how logs with debug and info didn’t get printed. This is because warning is the default level of logging. Any severity below `WARNING` is going to be ignored, unless we override the default level. To achieve that, we have to use the `basicConfig(**kwargs)` method in logging. In that method, we have to pass an argument called `level` and set it to the level on which we would like to see our logs.

##### Capturing Stack Traces (the error messages)
There are often times when you can anticipate when an error will occur in your code so you implement a `try/except` clause. When you use `except`, it is best practice to except a *specific* error class because using the general `Exception` class will "except" all errors,  but this indicates that you are unsure what the problem may be and therefore need to redesign some part of you code.  

Regardless, when an error does occur, it is useful to log it. using the `ERROR` logging class is a good start, but saving the actual error message i.e. stack trace to the log file will allow you to check later on and properly debug your code. To do this, one must use the `exc_info=` optional parameter during logging. Below is an example:

```python
import logging

try:
  c = a / b
except ZeroDivisionError as e:
    logging.error("Exception occurred", exc_info=True)  
```

##### [requests](https://requests.readthedocs.io/en/master/)
The `requests` library is a very popular method in Python for interfacing with web applications via HTTP. This library enables one to quickly utilize RESTful APIs programmatically via its built-in functions. The main page of its documentation actually shows all the nicest features that the library includes:

```bash
>>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
>>> r.status_code
200
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> r.encoding
'utf-8'
>>> r.text
'{"type":"User"...'
>>> r.json()
{'private_gists': 419, 'total_private_repos': 77, ...}
```
