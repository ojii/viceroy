##############
Javascript API
##############

If you wish to use an unsupported Javascript testing library, you can do so
using the Javascript and Python APIs.

.. warning::

    In Viceroy you cannot rely on the load event on the window to fire, if your
    testing library depends on it, you need to manually start the library in
    your :py:attr:`viceroy.api.BaseTestSuite.runner_script`.

.. js:function:: Viceroy.done(results)

    Function you must call after all tests are run. The ``results`` argument
    is then passed to :py:meth:`viceroy.api.BaseTestSuite.get_results` to
    transform them into the expected data structure.
