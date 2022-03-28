from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def pick_material(page):
    # Pick Nickel
    metals = page.find_element(By.ID, 'ctl00_ContentMain_ucMatGroupTree_LODCS1_msTreeViewn3')
    metals.click()
    page.implicitly_wait(1)
    non_ferrous = page.find_element(By.ID, 'ctl00_ContentMain_ucMatGroupTree_LODCS1_msTreeViewn13')
    non_ferrous.click()
    page.implicitly_wait(0.5)
    nickel = page.find_element(By.ID, 'ctl00_ContentMain_ucMatGroupTree_LODCS1_msTreeViewt23')
    nickel.click()
    return None

def scan(page):
    # Scan all the pages
    current_page = 0
    page_total = int(page.find_element(By.ID, 'ctl00_ContentMain_UcSearchResults1_lblPageTotal2').text)
    
    results = page.find_element(By.ID, 'tblResults')
    
    links = set()
    
    while (current_page <= (page_total - 1)):
        page.implicitly_wait(0.5)
        dropdown = Select(page.find_element(By.NAME, 'ctl00$ContentMain$UcSearchResults1$drpPageSelect2'))
        results = page.find_element(By.ID, 'tblResults')
        links_raw = results.find_elements(By.XPATH, '//a[contains(@href, "MatGUID")]')
        for link in links_raw:
            links.add(link.get_attribute('href'))
        dropdown.select_by_index(current_page)
        current_page += 1
        
    return links

def scrape_properties(page, properties):

    links = set()
    
    for property in properties:
        dropdown = Select(page.find_element(By.NAME, 'ctl00$ContentMain$ucPropertyDropdown1$drpPropertyList'))
        dropdown.select_by_visible_text(property)
        
        find = page.find_element(By.NAME, 'ctl00$ContentMain$btnSubmit')
        find.click()
        
        links.update(scan(page))
        page.implicitly_wait(0.5)
        
    return links