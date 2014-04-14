##############
Javascript API
##############

If you wish to use an unsupported Javascript testing library, you can do so
using the Javascript and Python APIs.


.. js:function:: viceroy_notify(failed, message)

    Notify Viceroy that the test method ran. ``failed`` is a boolean flag
    indicating whether the test method failed or passed. ``message`` is the
    error message for failed tests.
