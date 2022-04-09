from matplotlib.pyplot import table
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
import link_scraper as ls
import time
import random

element_regex ='^[\w]+[,][\s][\w]*' # '^[\w]+[,][\s][A-Z][a-z]{0,1}$' (old regex)

def grab_all_DataFrames(links, browser):
    data = []
    hits = 0
    for link in links:
        try:
            browser.get(link)
            main_table = pd.read_html(browser.page_source, index_col=0, attrs={'class':"tabledataformat"})[0]
            head_table = pd.read_html(browser.page_source, index_col=0, attrs={'class':"tabledataformat t_ableborder tableloose altrow"})[0]
            entry = pd.concat([main_table, head_table.squeeze()])
            entry.loc['URL'] = browser.current_url
            entry.loc["Name"] = browser.title
            data.append(entry)
            time.sleep(random.randint(15,30))
            print('Number of materials: ' + str(hits))
            hits += 1
        except Exception as e:
            print(e)
            print("Function got to " + str(hits) + " materials before failure")
            return data
    print("Function got to " + str(hits) + " materials, success!")
    return data
    

# Depreciated, now we save the dataframes directly
def grab_all_data(links, browser):
    data = pd.DataFrame()
    hits = 0
    for link in links:
        try:
            entry = grab_table(link, browser)
            print(entry)
            data = pd.concat([data, entry])
            time.sleep(random.randint(1,60))
            print('Number of materials: ' + str(hits))
            hits += 1
        except Exception as e:
            print(e)
            print("Function got to " + str(hits) + " materials before failure")
            return data
    print("Function got to " + str(hits) + " materials, success!")
    return data

# Depreciated function to only grab properties from a list
def grab_data(link, properties, browser):
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

# This one just takes everything
def grab_table(link, browser):
    browser.get(link)
    table = pd.read_html(browser.page_source, index_col=0, attrs={"class":"tabledataformat"})[0]
    table.index.name = None
    formatted_table = pd.DataFrame(table[table.index.notnull()][1]).T
    formatted_table.insert(0, 'URL', browser.current_url)
    formatted_table.insert(0, 'Name', browser.title)
    return formatted_table
        

if __name__ == '__main__':

    options = Options()
    options.headless = False
    options.add_argument('no-sandbox')
    browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=options)

    browser.get('https://www.matweb.com/search/PropertySearch.aspx')
    browser.implicitly_wait(0.5)
    
    ls.pick_material(browser)
    
    find = browser.find_element(By.NAME, 'ctl00$ContentMain$btnSubmit')
    find.click()
    
    results = browser.find_element(By.ID, 'tblResults')
    link = results.find_element(By.XPATH, '//a[contains(@href, "MatGUID")]')
    link.click()

    browser.get('https://www.matweb.com/search/DataSheet.aspx?MatGUID=014093642976472984e91c7392e67b55&ckck=1')
    # table = pd.read_html(browser.page_source, index_col=0, attrs={"class":"tabledataformat"})[0]
    
    # table.index.name = None
    
    # prop_entry = table[table.index.notnull()].reindex(properties)[1]
    
    
    # comp_entry = table['Component Elements Properties':].filter(regex=element_regex, axis='index')[1] # Check the regex works for single letter elements
    
    # new_entry = pd.concat([pd.DataFrame(prop_entry).T, pd.DataFrame(comp_entry).T], axis=1)
    # new_entry.insert(0, 'URL', browser.current_url)
    # new_entry.insert(0, 'Name', browser.title)
    
    # test = grab_all_data('https://www.matweb.com/search/DataSheet.aspx?MatGUID=014093642976472984e91c7392e67b55&ckck=1', browser)
    
    # print(entry.head())
    
    # print(data)
    
    browser.close()
    