from bs4 import BeautifulSoup

with open("brand_list.html", "r", encoding="utf-8") as html_file:
    content = html_file.read()

    soup = BeautifulSoup(content, "lxml")

    contentContainer = soup.find("div", class_= "mw-content-ltr")

    countries = contentContainer.find_all("h2")[1]

    countryContent = countries.find_next_sibling("ul")

    print(countryContent)
            


html_file.close()