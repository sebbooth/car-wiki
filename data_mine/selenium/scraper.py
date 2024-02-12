from selenium import webdriver
from selenium.webdriver.common.by import By

from resources.sel_util import *
from resources.scrape_models import *
from resources.file_io import *

class linkCollection:
    def __init__(self, setFilePath, listFilePath):
        self.linkSet = {}
        self.linkStack = []
        self.setFilePath = setFilePath
        self.listFilePath = listFilePath

    def read_from_logs(self):
        self.linkSet = read_file_link_set(self.setFilePath)
        self.linkStack = read_file_link_list(self.listFilePath)
        
        if self.linkStack:
            print("\033[32m[LINKS LOADED FROM LOGS]\033[0m ")
            return True
        return False

    def add_link(self, link, title):
        lang = link.replace("https://", "").split(".")[0]

        if lang != "en":
            return "\033[31m[NOT ENGLISH]\033[0m " + link
        
        if link not in self.linkSet:
            self.linkSet[link] = title
            append_to_file_link_set(self.setFilePath, link, title)
            self.linkStack.append(link)
            append_to_file_link_list(self.listFilePath, link)
            return "\033[32m[ADDED LINK]\033[0m " + link
        else:
            return "\033[31m[LINK ALREADY FOUND]\033[0m " + link

    def get_next_link(self):
        if self.linkStack:
            link = self.linkStack.pop()
            fileLink = pop_link(self.listFilePath)
            assert link == fileLink
            return link, self.linkSet[link]
        else:
            return None

def link_xPath(search):
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

    return "//a[contains(@href, '" + search +"')]" + xPathSuffix

def scrape_brand_list(driver, links, url, output=False):
    driver.get(url)
    content = driver.find_elements(By.XPATH, '//div[contains(@class, "mw-content-ltr")]//ul//li//a|//h2|//h3')

    with open("output/brand_list.csv", "w", encoding="utf-8") as csvF:
        csvF.write("Brand,Country,Status,Wikipedia Page") 

        curCountry, curStatus = "", ""
        
        for element in content:
            tag = element.tag_name

            if (tag=="h2" or tag=="h3"):
                try:
                    title = element.find_element(By.TAG_NAME, 'span').text
                except:
                    continue

                if (title == "See also"):
                    break
                if(output):
                    highlight(element, "blue", 5)

                if (tag=="h2"):
                    curCountry = title
                    curStatus = ""
                else:
                    curStatus = title
            
            elif (tag=="a"):
                row = element.text +","+curCountry+ "," + curStatus + "," + element.get_attribute("href")
                newLink = links.add_link(element.get_attribute("href"), element.text)

                if(output):
                    highlight(element, "yellow", 5)
                    print(newLink)
                
                csvF.write("\n"+row)
    csvF.close()
    return links

def check_for_keywords(page_source):
    hasKeyword = False
    checkKeywords = ["car", "Car", "Automobile", "automobile", "vehicle", "Vehicle", "motor", "Motor"]
    for keyword in checkKeywords:
            if keyword in page_source:
                hasKeyword = True
                break
    return hasKeyword

def main():

    driver = webdriver.Firefox()

    links = linkCollection("logs/linkSet.txt", "logs/linkList.txt")

    if not links.read_from_logs():
        links = scrape_brand_list(driver, links, "https://en.wikipedia.org/wiki/List_of_car_brands", output=True)


    vehicles = []
    for i in range(1000):
        next = links.get_next_link()
        if(next):
            nextLink, title = next
        else:
            break

        print("\033[34m[GO TO]\033[0m", nextLink, "\033[34m[TITLE]\033[0m", title)

        driver.get(nextLink)
        
        hasKeyword = check_for_keywords(driver.page_source)

        if (hasKeyword == False):
            print("\033[31;2m[NO KEYWORD FOUND]\033[0m ", nextLink)
            continue
        
        try:
            vehicles = scrape_models(driver, nextLink)
            write_to_file_json("vehicles.json", vehicles)


        except:
            pass

        linkXPath = link_xPath(title)
        linkElements = driver.find_elements(By.XPATH, linkXPath)

        for element in linkElements:
            try:
                print(links.add_link(element.get_attribute("href"), title))
                highlight(element, "yellow", 5)

            except:
                highlight(element, "red", 5)


    write_to_file_json("output/vehicles.json", vehicles)
    print("\n\nEXITING\n\n")


if __name__ == '__main__':
    main()