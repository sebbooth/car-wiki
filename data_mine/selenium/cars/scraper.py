from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import sys
sys.path.insert(0, '../')
from selenium_resources.sel_util import *
from selenium_resources.file_io import *
from scrapers.scrape_fields import *
from scrapers.scrape_model import *

driver = webdriver.Chrome()


links = read_carsdotcom_json("data/complete_links.json")
for link in links:
    
    try:
        driver.get(link["URL"]) 
        trims = scrape_model_1(driver)
        fulltrims = []
        if trims:
            for trim_data in trims:
                trim = { "Make": link["Make"],"Model": link["Model"],"Year": link["Year"]}
                trim.update(trim_data)
                fulltrims.append(trim)

        write_to_file_json("data/cars.json", fulltrims)

    except:
        continue

    try:
        driver.get(link["URL"]) 
        trims = scrape_model_2(driver)
        fulltrims = []
        if trims:
            for trim in trims:
                trim = { "Make": link["Make"],"Model": link["Model"],"Year": link["Year"]}
                trim.update(trim_data)
                fulltrims.append(trim)

        write_to_file_json("data/cars.json", fulltrims)

    except:
        continue
    
    

