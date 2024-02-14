from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_models(driver, url):
    vehicles = []
    driver.get(url)

    tableXPath = """//tbody[
                    tr[count(th) <= 1 and th and not(td)] 
                    and .//th 
                    and .//td 
                    and .//img 
                    and not(.//*[contains(@class, 'navbox-title')])
                ]"""

    modelTables = driver.find_elements(By.XPATH, tableXPath)

    if modelTables:
        for table in modelTables:
            tableRows = table.find_elements(By.TAG_NAME, 'tr')
            if len(tableRows) < 2:
                continue
            sectionTitle = ""
            vehicle = {}
            for row in tableRows:
                headers = row.find_elements(By.TAG_NAME, 'th')
                datas = row.find_elements(By.TAG_NAME, 'td')

                if headers and not datas:
                    sectionTitleElement = headers[0]
                    if sectionTitle == "":

                        if vehicles:
                            make = vehicles[0]["Make"]
                            model = vehicles[0]["Model"] + " " + sectionTitleElement.text
                        else:
                            try:
                                make, model = sectionTitleElement.text.split(' ', 1)
                            except:
                                make = sectionTitleElement.text
                                model = sectionTitleElement.text

                        vehicle["Make"] = make
                        vehicle["Model"] = model
                        vehicle["URL"] = url
                        

                        sectionTitle  = sectionTitleElement.text
                    else:
                        sectionTitle  = sectionTitleElement.text
                        vehicle[sectionTitle] = {}

                    #print("\n"+sectionTitle)
                    highlight(sectionTitleElement, "blue", 5)

                if headers and datas:
                    header = headers[0]
                    data = datas[0]
                    vehicle[sectionTitle][header.text] = data.text
                    highlight(header, "red", 5)
                    highlight(data, "yellow", 5)
                    #print("  " + header.text + ": " + data.text)

                if datas and not headers:
                    if len(datas) == 2:
                        header = datas[0]
                        data = datas[1]
                        vehicle[sectionTitle][header.text] = data.text
                        highlight(header, "red", 5)
                        highlight(data, "yellow", 5)
                        #print("  " + header.text + ": " + data.text)

                    else:
                        data = datas[0]
                        
                        imgElements = data.find_elements(By.TAG_NAME, 'a')

                        if imgElements:
                            imgElement = imgElements[0]

                            vehicle["imgURL"] = imgElement.get_attribute("href")
                            highlight(imgElement, "black", 5)
                            #print("  imgUrl: " + imgElement.get_attribute("href"))
                        else:
                            sectionTitle  = data.text
                            vehicle[sectionTitle] = {}
            
            if "Overview" in vehicle:
                vehicles.append(vehicle)
                print("\nFOUND VEHICLE: " + vehicle["Make"] + " " + vehicle["Model"] + "\n")

    return vehicles


from file_io import *
from sel_util import *
driver = webdriver.Firefox()
vehiclesL = (scrape_models(driver, "https://en.wikipedia.org/wiki/Mitsubishi_Pajero"))
write_to_file_json("output/vehiclesTest.json", vehiclesL)
vehiclesL = (scrape_models(driver, "https://de.wikipedia.org/wiki/GAZ-3307"))
write_to_file_json("output/vehiclesTest.json", vehiclesL)
vehiclesL = (scrape_models(driver, "https://en.wikipedia.org/wiki/VinFast_LUX_A2.0"))
write_to_file_json("output/vehiclesTest.json", vehiclesL)
