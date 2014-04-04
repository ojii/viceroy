##########
Quickstart
##########


This quickstart assumes you're already familiar with the Javascript testing
library you are using.


******
Common
******

The way to run your tests is to define a test suite, by subclassing the
appropriate base class for your library, and set
:py:attr`viceroy.api.BaseTestSuite.test_file_path` to a path of your Javascript
file containing the tests. You may set
:py:attr`viceroy.api.BaseTestSuite.expected_failures` to a list of tests that
are expected to fail (if your Javascript library supports this natively, you
can ignore that attribute).


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

