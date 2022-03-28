from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':

    options = Options()
    options.headless = False
    # options.add_argument("--user-data-dir=chrome-data") 

    browser = webdriver.Chrome('driver\chromedriver.exe', options=options)

    browser.get('https://www.matweb.com/search/DataSheet.aspx?MatGUID=014093642976472984e91c7392e67b55&ckck=1')
    df = pd.read_html(browser.page_source)[0]
    print(df.head())
    
    