from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import link_scraper as ls

if __name__ == '__main__':

    options = Options()
    options.headless = False
    # options.add_argument("--user-data-dir=C:/Users/Mack/AppData/Local/Google/Chrome/User Data/Default")

    browser = webdriver.Chrome('driver\chromedriver.exe', options=options)
    browser.get('https://www.matweb.com/search/PropertySearch.aspx')
    
    ls.pick_material(browser)
    
    find = browser.find_element(By.NAME, 'ctl00$ContentMain$btnSubmit')
    find.click()
    
    results = browser.find_element(By.ID, 'tblResults')
    link = results.find_element(By.XPATH, '//a[contains(@href, "MatGUID")]')
    link.click()

    browser.get('https://www.matweb.com/search/DataSheet.aspx?MatGUID=014093642976472984e91c7392e67b55&ckck=1')
    df = pd.read_html(browser.page_source, attrs={"class":"tabledataformat"})[0]
    print(df.head())
    
    browser.close()
    
    