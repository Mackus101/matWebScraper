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
    browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=options)
    # browser = webdriver.Chrome('driver\chromedriver.exe', options=options)

    ls.start(browser)
    # ls.pick_material(browser)
    # scan_links = np.array(list(ls.scrape_properties(browser, properties)))
    
    file = input("What file do you want?")
    
    # grab_links = np.loadtxt('links/partition_' + str(file) + '.dat', dtype=str, delimiter=" ")

    grab_links = ['https://www.matweb.com/search/DataSheet.aspx?MatGUID=0745fab0a2714ca2b2fe94370053b3ff', 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=e5868e2f0dc0449ea6b7e5799828db30']
    
    data = ts.grab_all_data(grab_links, browser)
    print(data)
    data.to_csv('data/nickel_data_' + str(file) + '.csv')
    browser.close()