from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome('driver\chromedriver.exe')

browser.get('https://www.matweb.com/search/PropertySearch.aspx')

metals = browser.find_element(By.ID, 'ctl00_ContentMain_ucMatGroupTree_LODCS1_msTreeViewn3')
metals.click()
browser.implicitly_wait(0.5)
non_ferrous = browser.find_element(By.ID, 'ctl00_ContentMain_ucMatGroupTree_LODCS1_msTreeViewn13')
non_ferrous.click()
browser.implicitly_wait(0.5)
nickel = browser.find_element(By.ID, 'ctl00_ContentMain_ucMatGroupTree_LODCS1_msTreeViewt23')
nickel.click()

find = browser.find_element(By.NAME, 'ctl00$ContentMain$btnSubmit')
find.click()

results = browser.find_element(By.ID, 'tblResults')

links = results.find_element(By.TAG_NAME, 'a').get_attribute("href")