from selenium.webdriver.support.wait import WebDriverWait


def wait_for_js_to_stop(browser, timeout=10):
    WebDriverWait(browser, timeout).until(
        lambda _: browser.execute_script('return window.VICEROY_DONE;')
    )


def wait_for_dom_ready(browser, timeout=10):
    WebDriverWait(browser, timeout).until(
        lambda _: browser.execute_script(
            'return document.readyState;'
        ) == 'complete'
    )

