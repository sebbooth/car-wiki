from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options

import time

def scrape_model_1(driver, url):
    driver.get(url)
    specs_link_xpath = '//a[contains(@href, "/specs/")]'
    specs_link = driver.find_element(By.XPATH, specs_link_xpath)
    if specs_link:
        specs_href = specs_link.get_attribute('href')
        driver.get(specs_href)

        change_trim_link = driver.find_elements(By.CLASS_NAME, "change-trim-link")
        if change_trim_link:
            change_trim_link[0].click()

            trim_links = driver.find_elements(By.XPATH, "//div[contains(@class, 'sds-modal__content-body')]//ul//li//a")
            links_dict = {}
            for link in trim_links:
                href = link.get_attribute("href")
                name = link.text
                msrp_span = link.find_element(By.XPATH, ".//following-sibling::span")
                msrp = msrp_span.text.strip()
                links_dict[href] = {"name": name, "msrp": msrp}

            return links_dict
        
def scrape_model_2(driver, url):
    driver.get(url)
    
    desktop_trim_picker_button = driver.find_element(By.ID, "desktop-trim-picker")
    desktop_trim_picker_button.click()

    buttons = driver.find_elements(By.XPATH, "//div[@class='popover-picker-main']//button")
    for button in buttons:
        button.click()
        print(button.get_attribute("data-option-value"))
        time.sleep(2)


        """
        DO SPECS SCRAPING HERE
        """

        desktop_trim_picker_button.click()
        time.sleep(2)



options = Options()
#options.preferences.update({"javascript.enabled": False})
driver = webdriver.Firefox(options=options)

#print(scrape_model_1(driver, "https://www.cars.com/research/acura-cl-2003"))
print(scrape_model_2(driver, "https://www.cars.com/research/kia-ev9-2024/"))
driver.close()