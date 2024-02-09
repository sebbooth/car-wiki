from bs4 import BeautifulSoup
import re
import requests

def has_active(text):
    pattern = r'active'
    return bool(re.search(pattern, text, flags=re.IGNORECASE))

def has_former(text):
    pattern = r'former'
    return bool(re.search(pattern, text, flags=re.IGNORECASE))

url = "https://en.wikipedia.org/wiki/List_of_car_brands"
htmlResponse = requests.get(url)

soup = BeautifulSoup(htmlResponse.content, "html.parser")
contentContainer = soup.find("div", class_= "mw-content-ltr")
stack = contentContainer.find_all(["h2", "h3", "li"])

curCountry = ""
curStatus = ""
with open("brand_list.csv", "w", encoding="utf-8") as csvF:
    csvF.write("Brand,Country,Status,Wikipedia Page") 

    for t in (stack):
        title = t.find("span")
        brand = t.find("a")
        
        if (title):
            if (title.text=="citation needed"):
                continue

            id = title['id']

            if (id == "See_also"):
                break

            if (has_active(id) or has_former(id)):
                if has_active(id):
                    curStatus = "Active"
                else:
                    curStatus = "Former"
            else:
                curCountry = id
                curStatus = ""          
                
        elif (brand):
            row = "\n" +brand['title'] + "," + curCountry + "," + curStatus + ",https://en.wikipedia.org" + brand['href']
            try:
                csvF.write(row) 
            except:
                print(brand['title'])
                print(curCountry)
                print(curStatus)
                print(brand['href'])
csvF.close()
