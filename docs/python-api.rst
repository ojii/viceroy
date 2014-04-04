##########
Python API
##########

If you wish to use an unsupported Javascript testing library, you can do so
using the Javascript and Python APIs.


************************
Support a custom library
************************

Ideally, all you need to do is subclass :py:class:`viceroy.api.BaseTestSuite`,
implement :py:meth:`viceroy.api.BaseTestSuite.get_results`, define what
:py:class:`viceroy.api.BaseTestSuite.scripts` (of your testing framework) need
to be loaded, optionally set :py:class:`viceroy.api.BaseTestSuite.setup_script`
to a script that is run before the test script is executed and
:py:class:`viceroy.api.BaseTestSuite.runner_script` to a script that runs the
tests.

One of those scripts must call :js:func:`Viceroy.done` once the tests are done.


*********
Reference
*********


.. py:module:: viceroy.api


.. py:class:: BaseTestSuite

    Base test suite that handles selenium web drivers and calls the
    scripts defined.

    This class is an abstract base class and cannot be instantiated.

    .. py:attribute:: timeout

        Integer amount of seconds used as timeout when running Javascript.
        Default: ``10``.

    .. py:attribute:: driver_class

        Selenium web driver class to use, defaults to the firefox web
        driver.

    .. py:attribute:: scripts

        A list of absolute file paths to Javascript dependencies required
        to run the tests.

    .. py:attribute:: setup_script

        Defaults to ``None``. If set to an absolute file path, this script
        will be loaded after :py:attr:`scripts` are loaded.

    .. py:attribute:: test_file_path

        Abstract property that has to be set to an absolute file path when
        building actual test cases.

        This script is loaded after :py:attr:`setup_script`.

    .. py:attribute:: runner_script

        Defaults to ``None``. If set to an absolute file path, this script
        will be loaded after :py:attr:`test_file_path` is loaded.

        This script is where you should implement custom logic to run the
        tests, if the test script doesn't do so automatically.

    .. py:attribute:: expected_failures

        A list of expected failures.

    .. py:method:: get_results(results) -> iterator:

        Abstract method that must be implemented by subclasses.

        Given a ``results`` object that was passed from Javascript via
        :js:func:`Viceroy.done`, this method must return an iterator that
        yields :py:class:`viceroy.utils.Result` or
        :py:class:`viceroy.utils.ComparisonResult` objects.


.. py:module:: viceroy.utils

.. py:class:: Result(name, passed, message)

    A namedtuple which takes the ``name`` of the test run, a boolean flag
    whether it ``passed`` or not and a string ``message`` as arguments.

.. py:class:: ComparisonResult(name, passed, message, expected, actual)

    Similar to :py:class:`Result``, but takes two additional arguments,
    ``expected`` and ``actual`` to indicate why a comparison failed.
