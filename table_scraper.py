from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import link_scraper as ls
import time
import random

properties = ['Tensile Strength, Ultimate', 'Tensile Strength, Yield', 'Elongation at Break']
element_regex ='^[\w]+[,][\s][\w]*' # '^[\w]+[,][\s][A-Z][a-z]{0,1}$' (old regex)

def grab_all_data(links, browser):
    data = pd.DataFrame()
    hits = 0
    for link in links:
        try:
            pd.concat([data, grab_data(link, browser)])
            time.sleep(random.randint(1,60))
            hits += 1
        except:
            print("Function got to " + str(hits) + " materials before failure")
            return data
    print("Function got to " + str(hits) + " materials, success!")
    return data

def grab_data(link, browser):
    browser.get(link)
    table = pd.read_html(browser.page_source, index_col=0, attrs={"class":"tabledataformat"})[0]
    table.index.name = None
    prop_entry = table[table.index.notnull()].reindex(properties)[1]
    try:
        comp_entry = table['Component Elements Properties':].filter(regex=element_regex, axis='index')[1]
    except KeyError:
        return pd.DataFrame()
    new_entry = pd.concat([pd.DataFrame(prop_entry).T, pd.DataFrame(comp_entry).T], axis=1)
    new_entry.insert(0, 'URL', browser.current_url)
    new_entry.insert(0, 'Name', browser.title)
    return new_entry
        

if __name__ == '__main__':

    options = Options()
    options.headless = False
    # options.add_argument("--user-data-dir=C:/Users/Mack/AppData/Local/Google/Chrome/User Data/Default")

    browser = webdriver.Chrome('driver\chromedriver.exe', options=options)
    browser.get('https://www.matweb.com/search/PropertySearch.aspx')
    browser.implicitly_wait(0.5)
    
    ls.pick_material(browser)
    
    find = browser.find_element(By.NAME, 'ctl00$ContentMain$btnSubmit')
    find.click()
    
    results = browser.find_element(By.ID, 'tblResults')
    link = results.find_element(By.XPATH, '//a[contains(@href, "MatGUID")]')
    link.click()

    # browser.get('https://www.matweb.com/search/DataSheet.aspx?MatGUID=014093642976472984e91c7392e67b55&ckck=1')
    # table = pd.read_html(browser.page_source, index_col=0, attrs={"class":"tabledataformat"})[0]
    
    # table.index.name = None
    
    # prop_entry = table[table.index.notnull()].reindex(properties)[1]
    
    
    # comp_entry = table['Component Elements Properties':].filter(regex=element_regex, axis='index')[1] # Check the regex works for single letter elements
    
    # new_entry = pd.concat([pd.DataFrame(prop_entry).T, pd.DataFrame(comp_entry).T], axis=1)
    # new_entry.insert(0, 'URL', browser.current_url)
    # new_entry.insert(0, 'Name', browser.title)
    
    entry = grab_data('https://www.matweb.com/search/DataSheet.aspx?MatGUID=014093642976472984e91c7392e67b55&ckck=1', browser)
    
    print(entry.head())
    
    browser.close()
    
    
    