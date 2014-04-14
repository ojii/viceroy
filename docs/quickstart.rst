##########
Quickstart
##########


This quickstart assumes you're already familiar with the Javascript testing
library you are using.


******
Basics
******

At the core of viceroy is
:py:meth:`viceroy.api.ViceroyTestCase.assertInBrowser`, which runs a snippet of
Javascript and reports the result via standard Python unittest methods.


**************
QUnit Examples
**************

.. code-block:: python

    import unittest

    from viceroy.api import QUnitTestCase


    class MyQUnitTests(BaseQunitTestSuite):
        @unittest.expectedFailure
        def test_an_expected_failure(self):
            self.assertInBrowser("""
                test("this will fail", function(){
                    deepEqual(1, "1", "1 is not equal '1'!");
                });
            """)

        def test_something_that_will_pass(self):
            self.assertInBrowser("""
                test("this will pass", function(){
                    equal(1, "1", "1 is not equal '1'!");
                });
            """)


****************
Jasmine Examples
****************

.. code-block:: python

    import unittest

    from viceroy.api import JasmineTestCase

    class JasmineTests(JasmineTestCase):
        suite_name = "A suite"

        def test_spec_success(self):
            self.assertInBrowser("""
            it("contains spec with an expectation", function() {
                expect(true).toBe(true);
            });
            """)

        @unittest.expectedFailure
        def test_spec_fail(self):
            self.assertInBrowser("""
            it("contains spec with an failing expectation", function() {
                expect(true).toBe(false);
            });
            """)
