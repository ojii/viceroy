.. Viceroy documentation master file, created by
   sphinx-quickstart on Thu Apr  3 03:39:40 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

#####################
Viceroy Documentation
#####################


.. warning::

    This project is still in an early stage and quite a few things are not
    supported yet. Feel free to give it a try, but don't expect this to be
    production ready yet.

    I will likely change 100% of the APIs in new releases until I hit 1.0.


***************
What is Viceroy
***************

Viceroy is a Python library that allows you to run Javascript tests in a
browser, using Selenium, and reports them just like normal Python unit tests.

The main goal is to streamline continuous integration of Python web projects
that would like to test their Javascript.

For now, QUnit and Jasmine are supported, but you can add support for your
preferred testing library if you want to.

As for Python frameworks, Flask and Django are supported out of the box, but
again you may feel free to add support for the framework of your choice.

Note that how to extend Viceroy is not yet documented, as the API is not
finalized yet.


********
Contents
********

.. toctree::
    :maxdepth: 2

    installation
    quickstart

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

