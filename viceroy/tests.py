import unittest

from viceroy.api import JasmineTestCase
from viceroy.api import QUnitTestCase
from viceroy.api import ViceroyTestCase


class DummyTests(ViceroyTestCase):
    @unittest.expectedFailure
    def test_fail(self):
        self.assertInBrowser("""
        viceroy_notify(true, 'test message');
        """)

    def test_success(self):
        self.assertInBrowser("""
        viceroy_notify(false, 'test message');
        """)


# class QunitTests(QUnitTestCase):
#     @unittest.expectedFailure
#     def test_fail(self):
#         self.assertInBrowser("""
#         test( "hello fail", function() {
#           deepEqual( 1 , "1", "Failed!" );
#         });
#         """)
#
#     def test_success(self):
#         self.assertInBrowser("""
#         test( "hello success", function() {
#           equal( 1 , "1", "Success!" );
#         });
#         """)
#
#
# class JasmineTests(JasmineTestCase):
#     suite_name = "A suite"
#
#     def test_spec_success(self):
#         self.assertInBrowser("""
#         it("contains spec with an expectation", function() {
#             expect(true).toBe(true);
#         });
#         """)
#
#     @unittest.expectedFailure
#     def test_spec_fail(self):
#         self.assertInBrowser("""
#         it("contains spec with an failing expectation", function() {
#             expect(true).toBe(false);
#         });
#         """)
