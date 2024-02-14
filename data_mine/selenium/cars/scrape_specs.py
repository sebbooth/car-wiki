from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options

def delete_element(driver, ByMethod, matchString):
    try:
        element = driver.find_element(ByMethod, matchString)
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)
    except:
        print(f"Couldn't find {matchString}")

def scrape_img(driver, url):
    driver.get(url)
    img_element = driver.find_elements(By.XPATH, '//*[@class="photo-content"]//img')

    if img_element:
        return(img_element[0].get_attribute("src"))
    
def scrape_specs(driver, url):
    driver.get(url)
    
    delete_element(driver, By.CLASS_NAME, "global-header-container")
    delete_element(driver, By.ID, "onetrust-consent-sdk")
    delete_element(driver, By.ID, "credential_picker_container")

    accordions = driver.find_elements(By.CLASS_NAME, "sds-accordion__heading")

    for accordion in accordions:            
        accordion.click()
        accordion.click()

    container_XPATH = "//*[@id='research-trim-specs']"
    category_XPATH = "//h3//span"
    row_header_XPATH = "//td[(@class='row-header')]/strong|//td[(@class='row-content')]"

    container = driver.find_element(By.XPATH, container_XPATH)
    data_elements = container.find_elements(By.XPATH, f"{category_XPATH}|{row_header_XPATH}")

    category = ""
    header = ""
    vehicle = {}
    for element in data_elements:
        if element.tag_name == "span":
            category = element.text
            vehicle[category] = {}
        elif element.tag_name == "strong":
            header = element.text
        else:
            vehicle[category][header] = element.text

    return vehicle


driver = webdriver.Firefox()

print(scrape_img(driver, "https://www.cars.com/research/acura-cl-2003/specs/100352/"))
driver.close()