from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import numpy as np
import time
import random


def pick_material(page):
    # Pick Nickel
    metals = WebDriverWait(page, timeout=60).until(lambda d: d.find_element(By.ID, 'ctl00_ContentMain_ucMatGroupTree_LODCS1_msTreeViewn3'))
    metals.click()
    non_ferrous = WebDriverWait(page, timeout=60).until(lambda d: d.find_element(By.ID, 'ctl00_ContentMain_ucMatGroupTree_LODCS1_msTreeViewn13'))
    non_ferrous.click()
    nickel = WebDriverWait(page, timeout=60).until(lambda d: d.find_element(By.ID, 'ctl00_ContentMain_ucMatGroupTree_LODCS1_msTreeViewt23'))
    nickel.click()
    return None

def start(page):
    page.get('https://www.matweb.com/search/PropertySearch.aspx')
    pick_material(page)
    find = WebDriverWait(page, timeout=60).until(lambda d: d.find_element(By.NAME, 'ctl00$ContentMain$btnSubmit'))
    find.click()
    
    results = WebDriverWait(page, timeout=60).until(lambda d: d.find_element(By.ID, 'tblResults'))
    link = results.find_element(By.XPATH, '//a[contains(@href, "MatGUID")]')
    link.click()
    page.get('https://www.matweb.com/search/PropertySearch.aspx')

def scan(page):
    # Scan all the pages
    current_page = 0
    page_total = int(page.find_element(By.ID, 'ctl00_ContentMain_UcSearchResults1_lblPageTotal2').text)
    
    results = page.find_element(By.ID, 'tblResults')
    
    links = set()
    
    while (current_page <= (page_total - 1)):
        print('Current page: ' + str(current_page))
        dropdown = Select(page.find_element(By.NAME, 'ctl00$ContentMain$UcSearchResults1$drpPageSelect2'))
        results = WebDriverWait(page, timeout=60).until(lambda d: d.find_element(By.ID, 'tblResults'))
        links_raw = results.find_elements(By.XPATH, '//a[contains(@href, "MatGUID")]')
        for link in links_raw:
            links.add(link.get_attribute('href'))
        dropdown.select_by_index(current_page)
        current_page += 1
        time.sleep(random.randint(1,10))
    return links

def scrape_properties(page, properties):

    links = set()
    
    for property in properties:
        print('Scanning for ' + property)
        dropdown = Select(page.find_element(By.NAME, 'ctl00$ContentMain$ucPropertyDropdown1$drpPropertyList'))
        dropdown.select_by_visible_text(property)
        
        find = WebDriverWait(page, timeout=60).until(lambda d: d.find_element(By.NAME, 'ctl00$ContentMain$btnSubmit'))
        find.click()
        
        links.update(scan(page))
    return links

def save_links(links_list):
    pnum = 0
    split_list = np.array_split(links_list, 10)
    for partition in split_list:
        np.savetxt('links/partition_' + str(pnum) + '.dat', partition, delimiter=" ", fmt="%s")
        pnum += 1
    return None