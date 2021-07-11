# [Cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.0/first_steps.html)

Cookiecutter is a python library that allows you to download project templates from git repos and use them to quickly assemble a folder with the proper layout for a python package.

We will be using a simple project template found on [GitHub](https://github.com/wdm0006/cookiecutter-pipproject)

## Instructions
### Install cookiecutter
```
# First activate your virtual environment
$ pip install cookiecutter
```

### Download and Build Project Template
```
$ cookiecutter https://github.com/audreyr/cookiecutter-pypackage
```

If you have already downloaded it before:
```
$ cookiecutter cookiecutter-pypackage
```

```
author_name [Louis Taylor]:    // Enter full name
email []:                      // Your email
github_username [wdm0006]:     // Can leave this blank
project_name []:               // Full project name (e.g. Drug to Disease Compiler)
project_slug []:               // Short project name (e.g. drug2tf)
project_short_description []:  // Brief description of project
pypi_username []:              // PyPI username (optional)
version [0.1.0]:               // Starting version number
```
Present `Enter` through the rest.  

You should now see a folder with the "project_slug" name wherever you executed cookiecutter from.  

**IMPORTANT** Replace the `setup.py` and and `setup.cfg` files in the created folder with those found in the [template folder](templates)
