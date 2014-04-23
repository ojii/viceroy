import os

from flask import Flask
from flask import send_from_directory
from flask import send_file

from viceroy.api import build_test_case
from viceroy.constants import VICEROY_ROOT
from viceroy.contrib.jasmine import jasmine
from viceroy.contrib.flask import ViceroyFlaskTestCase


JASMINE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'js', 'jasmine')
)


def index():
    return send_file(os.path.join(JASMINE_DIR, 'specrunner.html'))


def send_qunit(filename):
    return send_from_directory(JASMINE_DIR, filename)


def send_viceroy(filename):
    return send_from_directory(os.path.join(VICEROY_ROOT, 'static'), filename)


class JasmineBase(ViceroyFlaskTestCase):
    @classmethod
    def viceroy_get_flask_app(cls):
        app = Flask(__name__)
        app.route('/')(index)
        app.route('/jasmine/<path:filename>')(send_qunit)
        app.route('/viceroy/<path:filename>')(send_viceroy)

        @app.route('/spec.js')
        def send_spec():
            return send_file(cls.viceroy_source_file)

        return app


build_jasmine_test = lambda name: build_test_case(
    'Jasmine{}'.format(name[:-3].capitalize()),
    os.path.join(JASMINE_DIR, 'spec', name),
    jasmine,
    JasmineBase,
)


JasmineMatchersConsoleReporterTests = build_jasmine_test(
    'console/ConsoleReporterSpec.js'
)
JasmineMatchersCustomMatchersTests = build_jasmine_test(
    'core/integration/CustomMatchersSpec.js'
)
JasmineMatchersEnvTests = build_jasmine_test(
    'core/integration/EnvSpec.js'
)
JasmineMatchersSpecRunningTests = build_jasmine_test(
    'core/integration/SpecRunningSpec.js'
)
JasmineMatchersMatchersUtilTests = build_jasmine_test(
    'core/matchers/matchersUtilSpec.js'
)
JasmineMatchersToBeCloseToTests = build_jasmine_test(
    'core/matchers/toBeCloseToSpec.js'
)
JasmineMatchersToBeDefinedTests = build_jasmine_test(
    'core/matchers/toBeDefinedSpec.js'
)
JasmineMatchersToBeFalsyTests = build_jasmine_test(
    'core/matchers/toBeFalsySpec.js'
)
JasmineMatchersToBeGreaterThanTests = build_jasmine_test(
    'core/matchers/toBeGreaterThanSpec.js'
)
JasmineMatchersToBeLessThanTests = build_jasmine_test(
    'core/matchers/toBeLessThanSpec.js'
)
JasmineMatcherstoBeNaNTests = build_jasmine_test(
    'core/matchers/toBeNaNSpec.js'
)
JasmineMatchersToBeNullTests = build_jasmine_test(
    'core/matchers/toBeNullSpec.js'
)
JasmineMatchersToBeTests = build_jasmine_test(
    'core/matchers/toBeSpec.js'
)
JasmineMatchersToBeTruthyTests = build_jasmine_test(
    'core/matchers/toBeTruthySpec.js'
)
JasmineMatchersToBeUndefinedTests = build_jasmine_test(
    'core/matchers/toBeUndefinedSpec.js'
)
JasmineMatchersToContainTests = build_jasmine_test(
    'core/matchers/toContainSpec.js'
)
JasmineMatchersToEqualTests = build_jasmine_test(
    'core/matchers/toEqualSpec.js'
)
JasmineMatchersToHaveBeenCalledTests = build_jasmine_test(
    'core/matchers/toHaveBeenCalledSpec.js'
)
JasmineMatchersToHaveBeenCalledWithTests = build_jasmine_test(
    'core/matchers/toHaveBeenCalledWithSpec.js'
)
JasmineMatchersToMatchTests = build_jasmine_test(
    'core/matchers/toMatchSpec.js'
)
JasmineMatchersToThrowErrorTests = build_jasmine_test(
    'core/matchers/toThrowErrorSpec.js'
)
JasmineMatchersToThrowTests = build_jasmine_test(
    'core/matchers/toThrowSpec.js'
)
JasmineAnyTests = build_jasmine_test(
    'core/AnySpec.js'
)
JasmineCallTrackerTests = build_jasmine_test(
    'core/CallTrackerSpec.js'
)
JasmineClockTests = build_jasmine_test(
    'core/ClockSpec.js'
)
JasmineDelayedFunctionSchedulerTests = build_jasmine_test(
    'core/DelayedFunctionSchedulerSpec.js'
)
JasmineEnvTests = build_jasmine_test(
    'core/EnvSpec.js'
)
JasmineExceptionFormatterTests = build_jasmine_test(
    'core/ExceptionFormatterSpec.js'
)
JasmineExpectationResultTests = build_jasmine_test(
    'core/ExpectationResultSpec.js'
)
JasmineExpectationTests = build_jasmine_test(
    'core/ExpectationSpec.js'
)
JasmineJsApiReporterTests = build_jasmine_test(
    'core/JsApiReporterSpec.js'
)
JasmineMockDateTests = build_jasmine_test(
    'core/MockDateSpec.js'
)
JasmineObjectContainingTests = build_jasmine_test(
    'core/ObjectContainingSpec.js'
)
JasminePrettyPrintTests = build_jasmine_test(
    'core/PrettyPrintSpec.js'
)
JasmineQueueRunnerTests = build_jasmine_test(
    'core/QueueRunnerSpec.js'
)
JasmineReportDispatcherTests = build_jasmine_test(
    'core/ReportDispatcherSpec.js'
)
JasmineSpecTests = build_jasmine_test(
    'core/SpecSpec.js'
)
JasmineSpyTests = build_jasmine_test(
    'core/SpySpec.js'
)
JasmineSpyStrategyTests = build_jasmine_test(
    'core/SpyStrategySpec.js'
)
JasmineSuiteTests = build_jasmine_test(
    'core/SuiteSpec.js'
)
JasmineTimerTests = build_jasmine_test(
    'core/TimerSpec.js'
)
JasmineUtilTests = build_jasmine_test(
    'core/UtilSpec.js'
)
JasmineHTMLHtmlReporterTests = build_jasmine_test(
    'html/HtmlReporterSpec.js'
)
JasmineHTMLHtmlSpecFilterTests = build_jasmine_test(
    'html/HtmlSpecFilterSpec.js'
)
JasmineHTMLMatchersHtmlTests = build_jasmine_test(
    'html/MatchersHtmlSpec.js'
)
JasmineHTMLPrettyPrintHtmlTests = build_jasmine_test(
    'html/PrettyPrintHtmlSpec.js'
)
JasmineHTMLQueryStringTests = build_jasmine_test(
    'html/QueryStringSpec.js'
)
JasmineHTMLResultsNodeTests = build_jasmine_test(
    'html/ResultsNodeSpec.js'
)
