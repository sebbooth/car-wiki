import sys
sys.path.insert(0, '../')
from selenium_resources.sel_util import *
from selenium_resources.file_io import *
from scrapers.scrape_fields import *
from scrapers.scrape_model import *

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import random





proxies = []
with open("../selenium_resources/proxy_list.txt", "r") as f:
    file_proxies = f.read().split("\n")
    for p in file_proxies:
        proxies.append("https://"+p)



# randomly extract a proxy
random_proxy = random.choice(proxies)
print(random_proxy)

# set the proxy in Selenium Wire
seleniumwire_options = {
    'proxy': {
        'http': f'{random_proxy}',
        'https': f'{random_proxy}',
        'verify_ssl': False,
    },
}

# create a ChromeDriver instance
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    seleniumwire_options=seleniumwire_options
)



driver.get("https://www.cars.com/")
"""
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
"""