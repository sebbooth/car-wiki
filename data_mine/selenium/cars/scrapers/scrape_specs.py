from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, time
sys.path.insert(0, '../../')
from selenium_resources.sel_util import *
from selenium_resources.file_io import *

def scrape_img(driver):
    img_element = driver.find_elements(By.XPATH, '//*[@class="photo-content"]//img')

    if img_element:
        return(img_element[0].get_attribute("src"))
    
    img_element = driver.find_elements(By.XPATH, '/html/body/section/div[2]/div/div[2]/spark-page-section[1]/div/div[2]/picture/img')

    if img_element:
        return(img_element[0].get_attribute("src"))
    
def scrape_specs_1(driver):
    accordions = driver.find_elements(By.CLASS_NAME, "sds-accordion__heading")

    for accordion in accordions:            
        accordion.click()
        accordion.click()

    container_XPATH = "//*[@id='research-trim-specs']"
    category_XPATH = "//h3//span"
    row_header_XPATH = "//td[(@class='row-header')]/strong|//td[(@class='row-content')]"

    container = driver.find_element(By.XPATH, container_XPATH)

    category = ""
    header = ""
    vehicle = {}
    for element in container.find_elements(By.XPATH, f"{category_XPATH}|{row_header_XPATH}"):
        element_tag = element.tag_name
        if element_tag == "span":
            category = element.text
            vehicle[category] = {}
        elif element_tag == "strong":
            header = element.text
        else:
            vehicle[category][header] = element.text
    try:
        img = scrape_img(driver)
        vehicle["imgURL"] = img
    except:
        pass
    return vehicle

def scrape_specs_2(driver):
    category = ""
    vehicle = {}
    field_names = read_carsdotcom_json("../data/fields_inv.json")
    msrp = driver.find_element(By.CLASS_NAME, "msrp").text
    vehicle["MSRP"] = msrp
 
    see_specs_button = driver.find_element(By.XPATH, "/html/body/section/div[2]/div/div[3]/spark-page-section/div/hubcap-button")
    driver.execute_script("arguments[0].click();", see_specs_button)        

    spec_tabs = driver.find_elements(By.CLASS_NAME, "spec-group")
    for spec_tab in spec_tabs:
        highlight(spec_tab, "blue", 5)
        category = spec_tab.find_element(By.CLASS_NAME, "spec-group-heading").text
        
        specs = []
        for spec in spec_tab.find_elements(By.CLASS_NAME, "spec-value"):
            specs.append(spec.text)

        vehicle[category] = {}
        for spec in specs:
            for field in field_names:
                matched_fields = []
                if field in spec:
                    matched_fields.append(field)
                if matched_fields:
                    index = spec.find(max(matched_fields, key=len))
                    vehicle[category][max(matched_fields, key=len)] = spec[:index].strip()
            if field not in vehicle[category] and "Standard" in spec:
                vehicle[category][spec.split("Standard")[1].strip()] = "Standard"
        
        if vehicle[category] == {}:
            vehicle[category] = specs
        
    try:
        img = scrape_img(driver)
        vehicle["imgURL"] = img
    except:
        pass

    return vehicle

"""
driver = webdriver.Firefox()

driver.get("https://www.cars.com/research/acura-cl-2003/specs/100352/")
time.sleep(2)
delete_element(driver, By.CLASS_NAME, "global-header-container")
delete_element(driver, By.ID, "onetrust-consent-sdk")
delete_element(driver, By.ID, "credential_picker_container")
print(scrape_specs_1(driver))

driver.get("https://www.cars.com/research/kia-niro_ev-2024/")
time.sleep(2)
delete_element(driver, By.CLASS_NAME, "global-header-container")
delete_element(driver, By.ID, "onetrust-consent-sdk")
delete_element(driver, By.ID, "credential_picker_container")
print(scrape_specs_2(driver))
driver.close()
"""