from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import json

from sel_util import *
from scrape_models import *
from write_to_file import *

driver = webdriver.Firefox()
driver.get("https://en.wikipedia.org/wiki/List_of_car_brands")


content = driver.find_elements(By.XPATH, '//div[contains(@class, "mw-content-ltr")]//ul//li//a|//h2|//h3')


class linkCollection:
    def __init__(self):
        self.linkSet = {}
        self.linkStack = []

    def add_link(self, link, title):
        lang = link.replace("https://", "").split(".")[0]

        if lang != "en":
            return "\033[31m[NOT ENGLISH]\033[0m " + link
        
        if link not in self.linkSet:
            self.linkSet[link] = title
            self.linkStack.append(link)
            return "\033[32m[ADDED LINK]\033[0m " + link
        else:
            return "\033[31m[LINK ALREADY FOUND]\033[0m " + link

    def get_next_link(self):
        if self.linkStack:
            link = self.linkStack.pop()
            return link, self.linkSet[link]
        else:
            return None

with open("brand_list.csv", "w", encoding="utf-8") as csvF:
    csvF.write("Brand,Country,Status,Wikipedia Page") 

    curCountry = ""
    curStatus = ""
    links = linkCollection()

    for element in content:
        tag = element.tag_name

        if (tag=="h2" or tag=="h3"):
            try:
                title = element.find_element(By.TAG_NAME, 'span').text
            except:
                continue
            if (title == "See also"):
                break
            highlight(element, "blue", 5)
            if (tag=="h2"):
                curCountry = title
                curStatus = ""
            else:
                curStatus = title
        
        elif (tag=="a"):
            highlight(element, "yellow", 5)
            row = element.text +","+curCountry+ "," + curStatus + "," + element.get_attribute("href")
            print(links.add_link(element.get_attribute("href"), element.text))
            
            csvF.write("\n"+row)

csvF.close()

mandatoryKeywords = ["car", "Car", "Automobile", "automobile", "vehicle", "Vehicle", "motor", "Motor"]
xPathSuffix = ""
xPathSuffix += "[contains(@href, '/wiki/')]"
xPathSuffix += "[not(span)]"
xPathSuffix += "[not(contains(@href, '.svg'))]"
xPathSuffix += "[not(contains(@href, '.JPG'))]"
xPathSuffix += "[not(contains(@href, '.jpg'))]"
xPathSuffix += "[not(contains(@href, '.png'))]"
xPathSuffix += "[not(contains(@href, '.PNG'))]"
xPathSuffix += "[not(contains(@href, '.gif'))]"
xPathSuffix += "[not(contains(@href, '.GIF'))]"
xPathSuffix += "[not(contains(@href, '.ogg'))]"
xPathSuffix += "[not(contains(@href, 'wikimedia.org'))]"
xPathSuffix += "[not(contains(@href, 'wikidata.org'))]"
xPathSuffix += "[not(contains(@href, 'wikisource.org'))]"
xPathSuffix += "[not(contains(@href, 'User:'))]"
xPathSuffix += "[not(contains(@href, 'Special:'))]"
xPathSuffix += "[not(contains(@href, 'Datei:'))]"
xPathSuffix += "[not(contains(@href, 'action=edit'))]"

vehicles = []
for i in range(1000):
    next = links.get_next_link()
    if(next):
        nextLink, title = next
    else:
        break

    print("\033[34m[GO TO]\033[0m", nextLink, "\033[34m[TITLE]\033[0m", title)

    driver.get(nextLink)
    
    page_source = driver.page_source
    hasKeyword = False

    for keyword in mandatoryKeywords:
        if keyword in page_source:
            hasKeyword = True
            break

    if (hasKeyword == False):
        print("\033[31;2m[NO KEYWORD FOUND]\033[0m ", nextLink)
        continue
    
    try:
        vehicles = scrape_models(driver, nextLink)
        write_to_file("vehicles.json", vehicles)


    except:
        pass

    linkXPath = "//a[contains(@href, '" + title +"')]" + xPathSuffix

    linkElements = driver.find_elements(By.XPATH, linkXPath)

    for element in linkElements:
        try:
            print(links.add_link(element.get_attribute("href"), title))
            highlight(element, "yellow", 5)

        except:
            highlight(element, "red", 5)


write_to_file("vehicles.json", vehicles)