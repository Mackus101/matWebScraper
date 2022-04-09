from copyreg import pickle
import link_scraper as ls
import table_scraper as ts
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options
import numpy as np
import pickle
import time

if (__name__ == '__main__'):
    # scan_properties = ['ELONGATION [PROPERTY GROUP]',
    #             'Tensile Strength, Ultimate (66430 matls)',
    #             'Tensile Strength, Yield (46238 matls)']
    
    scan_properties = ['Tensile Strength, Ultimate (66430 matls)',
                       'Tensile Strength, Yield (46238 matls)',
                       'Elongation at Break (72346 matls)',
                       'Density (108227 matls)',
                       'Electrical Resistivity (30440 matls)',
                       'Melting Point (27230 matls)',
                       'Tensile Modulus (41250 matls)',
                       ]
    
    regenerate = input("Do you want to regenerate the links? y/n") == 'y'
    
    start = i = int(input("What file do you want to start from?"))
    stop = int(input("Where do you want to end?"))

    options = Options()
    options.headless = True
    options.add_argument('no-sandbox')
    browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=options)
    # browser = webdriver.Chrome('driver\chromedriver.exe', options=options)

    ls.start(browser)
    ls.pick_material(browser)
    regen_start = time.time()
    if (regenerate):
        scan_links = np.array(list(ls.scrape_properties(browser, scan_properties)))
        ls.save_links(scan_links)
        print("--- %s Seconds ---" % (time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - regen_start))))
    while (start<=i<=stop):
        grab_start = time.time()
        grab_links = np.loadtxt('links/partition_' + str(i) + '.dat', dtype=str, delimiter=" ")
        # grab_links = ['https://www.matweb.com/search/DataSheet.aspx?MatGUID=0745fab0a2714ca2b2fe94370053b3ff', 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=e5868e2f0dc0449ea6b7e5799828db30']
        print('Starting partition: ' + str(0))
        data = ts.grab_all_DataFrames(grab_links, browser)
        pickle.dump(data, open('data/nickel_data_' + str(i) + '.p', 'wb'))
        print("--- %s Seconds ---" % (time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - grab_start))))
        i += 1

    test = pickle.load(open('data/nickel_data_0.p', 'rb'))
    print("WooHoo! Scraping Complete!")
    browser.close()