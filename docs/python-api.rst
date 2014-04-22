##########
Python API
##########

If you wish to use an unsupported Javascript testing library, you can do so
using the Javascript and Python APIs.


*********
Reference
*********


.. py:module:: viceroy.api


.. py:class:: ViceroyTestCase

    Base test case that handles selenium web drivers and calls the
    scripts defined.

    .. py:attribute:: server_class

        Server class to use. Default is :py:class:`viceroy.server.Server`. You
        may want to overwrite this to support custom Javascript frameworks or
        to support custom server side web frameworks.

    .. py:method:: get_driver(results):

        Returns an instantiated selenium web driver. Defaults to the Firefox
        web driver.

    .. py:method:: run_server(javascript):

        A context manager that runs a server for the given Javascript snippet.
        Yields the server object.

    .. py:method:: assertInBrowser(javascript):

        Run the javascript snippet given in the browser and assert it passes.


.. py:class:: QUnitTestCase

    Subclasses :py:class:`ViceroyTestCase` to run QUnit tests.


.. py:class:: JasmineTestCase

    Subclass :py:class:`ViceroyTestCase` to run Jasmine tests.


.. py:module:: viceroy.server


.. py:class:: Result(failed, message)

    A result of a test run in the browser. Usually you don't need to manually
    build these but can instead rely on :py:class:`ServerProcess.notify` to
    build it for you.


.. py:function:: static(path, content_type=None):

    Utility function to build tuples used in :py:class:`Server.urls` given a
    path to a file on the local filesystem. ``content_type`` will be guess via
    the :py:mod:`mimetypes` modules if set to ``None``.


.. py:class:: Server(javascript)

    Class that controls the HTTP server.

    .. py:attribute:: port

        Port number of the server. Is ``None`` until :py:meth:`run_async` is
        called.

    .. py:attribute:: index_html_path

        Full path to the index html file.

    .. py:attribute:: urls

        Dictionary mapping urls to tuples of ``(b'response', 'content_type')``.

        .. note::

            The response **must** be bytes, not strings.

    .. py:method:: setup_default_urls

        Sets up ``'/'`` to point to :py:attr:`index_html_path` and
        ``'/success.js'`` to point to the viceroy Javascript file.
        Overwrite this method if you want these to be mounted somewhere else.

    .. py:method:: setup_javascript_url(javascript)

        Maps the javascript snippet (given as a **string**) to the URL
        ``'/tests.js'``. Overwrite this method if you want the Javascript to be
        mounted on another URL.

    .. py:method:: setup_extra_urls

        Does nothing by default, but can be used by your subclasses to add more
        URLs.


    .. py:method:: wait(timeout=5)

        Waits for the results, or ``timeout`` and returns the result.

    .. py:method:: stop

        Stops the server.

    .. py:method:: run_async(timeout=5)

        Runs the server. Will wait maximum of ``timeout`` seconds and sets the
        :py:attr:`port` attribute to the port used by the server.


.. py:class:: QUnitServer

    Subclass of :py:class:`Server` used by
    :py:class:`viceroy.api.QUnitTestCase`. Mounts the QUnit Javascript files
    to ``/qunit/``.


.. py:class:: JasmineServer

    Subclass of :py:class:`Server` used by
    :py:class:`viceroy.api.JasmineTestCase`. Mounts the Jasmin Javascript files
    to ``/jasmine/``.
