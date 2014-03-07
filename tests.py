from viceroy import *
import xvfbwrapper


class QunitTests(BaseQunitTestSuite):
    test_file_path = os.path.join(BASEDIR, 'tests', 'qunit.js')


class JasmineTests(BaseJasminTestSuite):
    test_file_path = os.path.join(BASEDIR, 'tests', 'jasmine.js')


load_tests = auto_load_tests(locals())


if __name__ == '__main__':
    with xvfbwrapper.Xvfb():
        unittest.main()
        #unittest.TextTestRunner().run(unittest.TestSuite([
        #    QunitTests(),
        #    JasmineTests()
        #]))
