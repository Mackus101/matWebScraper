import link_scraper as ls
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if (__name__ == '__main__'):
    properties = ['ELONGATION [PROPERTY GROUP]',
                'Tensile Strength, Ultimate (66430 matls)',
                'Tensile Strength, Yield (46238 matls)']

    options = Options()
    options.headless = False
    options.add_argument('no-sandbox')

    browser = webdriver.Chrome('driver\chromedriver.exe', options=options)

    ls.start(browser)
    ls.pick_material(browser)
    scan_result = ls.scrape_properties(browser, properties)

    browser.close()