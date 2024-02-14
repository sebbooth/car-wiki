from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from scrape_model import *

def visit_links(driver):
    # Open the file containing the links
    with open("model_links.txt", "r") as f:
        # Read the links into a list
        links = [line.strip() for line in f.readlines()]
    
    # Visit each link using the Selenium driver
    for link in links:
        scrape_model(driver, link)


driver = webdriver.Firefox()

visit_links(driver)