def getfile(browser):
    pagesource=browser.page_source
    browser.switch_to.default_content()
    return pagesource
