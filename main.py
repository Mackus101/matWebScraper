import link_scraper as ls
import table_scraper as ts
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
    #browser.implicitly_wait(0.5)

    ls.start(browser)
    ls.pick_material(browser)
    scan_result = ls.scrape_properties(browser, properties)

    data = ts.grab_all_data(scan_result, browser)

    browser.close()