from selenium import webdriver
from selenium.webdriver.support.select import Select
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

current_page = 0
page_total = int(browser.find_element(By.ID, 'ctl00_ContentMain_UcSearchResults1_lblPageTotal2').text)

## dropdown = Select(browser.find_element(By.NAME, 'ctl00$ContentMain$UcSearchResults1$drpPageSelect2'))

results = browser.find_element(By.ID, 'tblResults')

links = []

while (current_page <= (page_total - 1)):
    browser.implicitly_wait(0.5)
    dropdown = Select(browser.find_element(By.NAME, 'ctl00$ContentMain$UcSearchResults1$drpPageSelect2'))
    results = browser.find_element(By.ID, 'tblResults')
    links_raw = results.find_elements(By.XPATH, '//a[contains(@href, "MatGUID")]')
    for link in links_raw:
        links.append(link.get_attribute('href'))
    dropdown.select_by_index(current_page)
    current_page += 1
    
for link in links:
    print(link)

print(len(links))
browser.close()