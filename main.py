import link_scraper as ls
import table_scraper as ts
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options
import numpy as np

if (__name__ == '__main__'):
    # properties = ['ELONGATION [PROPERTY GROUP]',
    #             'Tensile Strength, Ultimate (66430 matls)',
    #             'Tensile Strength, Yield (46238 matls)']

    options = Options()
    options.headless = True
    options.add_argument('no-sandbox')
    browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    # browser = webdriver.Chrome('driver\chromedriver.exe', options=options)

    ls.start(browser)
    # ls.pick_material(browser)
    # scan_links = np.array(list(ls.scrape_properties(browser, properties)))
    
    file = input("What file do you want?")
    
    grab_links = np.loadtxt('links/partition_' + str(file) + '.dat', dtype=str, delimiter=" ")

    data = ts.grab_all_data(grab_links, browser)
    data.to_csv('data/nickel_data_' + str(file) + '.csv')
    browser.close()