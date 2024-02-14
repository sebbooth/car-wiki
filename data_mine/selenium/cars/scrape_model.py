from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options



def scrape_model(driver, url):
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
            for link in trim_links:
                print(link.get_attribute("href"))



"""options = Options()
#options.preferences.update({"javascript.enabled": False})
driver = webdriver.Firefox(options=options)

scrape_model(driver, "https://www.cars.com/research/acura-cl-2003")"""