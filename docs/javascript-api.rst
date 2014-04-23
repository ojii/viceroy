##############
Javascript API
##############



.. js:function:: VICEROY.start_test(test_name)

    Notify Viceroy that a test starts. This is optional, but will result in
    better error reporting in case the test throws an exception.


.. js:function:: VICEROY.success(test_name)

    Report ``test_name`` was successful.


.. js:function:: VICEROY.fail(test_name, reason)

    Report ``test_name`` failed with ``reason``.


.. js:function:: VICEROY.skip(test_name, reason)

    Report that ``test_name`` has been skipped.


.. js:function:: VICEROY.done()

    Indicates the test suite is done. This **must** be called.
