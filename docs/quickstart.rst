##########
Quickstart
##########


This quickstart assumes you're already familiar with the Javascript testing
library you are using.


*****
QUnit
*****

Let's assume you have a Python project with a ``tests.py`` file containing
your unit tests and next to it a ``tests.js`` file containing your QUnit tests.

The following test suite (in your ``tests.py`` file) would load those QUnit
tests::

    import os

    from viceroy.api import BaseQunitTestSuite


    class MyQUnitTests(BaseQunitTestSuite):
        test_file_path = os.path.join(os.path.dirname(__file__), 'tests.js')


*******
Jasmine
*******

Let's assume you have a Python project with a ``tests.py`` file containing
your unit tests and next to it a ``tests.js`` file containing your Jasmine
tests.

The following test suite (in your ``tests.py`` file) would load those Jasmine
tests::

    import os

    from viceroy.api import BaseJasminTestSuite


    class MyQUnitTests(BaseJasminTestSuite):
        test_file_path = os.path.join(os.path.dirname(__file__), 'tests.js')

