### Background Information
#### Creating and Using a Repository
A Git repository is a specialized folder that tracks all changes made to files in your project. These tracked changes will build a history over time and you can trace every change made, **to every file**, back to the time and person who made them. This is incredibly useful for when you accidentally delete important code or if you want to retrieve previously written code that is no longer in your software. Using a repository to develop your code is standard practice by most programming teams and we will be using repositories extensively in this course.

#### Virtual Environments
Virtual environments in python are essentially isolated environments in which one can run their code. Typically, a programmer will install several different packages using `pip` over the course of their career. When you install a package, you are installing a specific version of it (e.g. version 5.3.2), but as with most packages, updates are pushed out over time causing some functions or methods in the package to become deprecated or removed entirely, and in other cases, new functions will be added. As you design your own packages, your code may rely on specific methods from other packages so it is important to specify what version of a package yours depends on in order to ensure that the required methods exist.  

As you begin to work on multiple projects, you may find that one project depends on version X.X.X of some package, while a different project uses version Y.Y.Y of that same package. It is quite annoying to have to reinstall specific versions of a package whenever you switch between projects, therefore it is often more ideal to work on projects within their own *virtual environment*.  

A virtual environment (venv) is in essence a folder on your machine. When you are not working in a venv, packages that you install using `pip` are downloaded and stored in a library folder wherever your base python interpreter is located. Whenever you call on that package in your code, it searches this library directory for that package. When you create a venv, you generate a new folder that that allows one to download and install packages via `pip` that are completely separate from your "global" packages (i.e. the packages you've downloaded when NOT in a venv).  

Upon creating a new venv, you will find that it has (almost) no packages installed. In this way, you can control exactly what package versions are installed to better troubleshoot your new package and to ensure it runs properly. When you are working inside a venv, `pip install` will install packages within the venv library folder, and not your global library. You can also configure Jupyter Notebook and PyCharm to use your venvs when working on specific projects.  

How one creates and works in a virtual environment from the terminal depends on how you are using python:
* [Anaconda](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/)
* [Base python](https://realpython.com/python-virtual-environments-a-primer/)
* Third party
    * [PyCharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)
    * [virtualenvwrapper (preferred)](https://virtualenvwrapper.readthedocs.io/en/latest/install.html)

#### [NetworkX](https://networkx.org/)
As data becomes larger and larger, computer scientists have found that the typical [relational model](https://en.wikipedia.org/wiki/Relational_model) (i.e. storing data in multiple tables) is not the most efficient or optimal way or organizaing data anymore. Many companies, such as [Google](https://blog.google/products/search/introducing-knowledge-graph-things-not/), have begun using graphs as the primary data structure for storing and retrieving information. Graphs and networks are used in almost every field of study: air traffic control, social media relationships, wireless telecommunications, and biological interactions. Being able to quickly take data and compile it into a network is a key skill for any programmer or bioinformatician.  

A network is typically composed of nodes (or vertices) and edges. Edges and nodes can be provided in a variety of methods including JSON, GML, pickles, and adjacency lists. Though these lists tend to only have the minimum necessary information, additional *metadata* can be included in other columns, so long as they are formatted correctly.

NetworkX is a relatively lightweight python package for not only creating different types of graphs, but also for running several graph algorithms. In your homework, you will learn the basic functions of NetworkX and how to build your how protein-protein interaction (PPI) network.
