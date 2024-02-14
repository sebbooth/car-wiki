from bs4 import BeautifulSoup
import re
import requests

def has_active(text):
    pattern = r'active'
    return bool(re.search(pattern, text, flags=re.IGNORECASE))

def has_former(text):
    pattern = r'former'
    return bool(re.search(pattern, text, flags=re.IGNORECASE))

url = "https://en.wikipedia.org/wiki/List_of_Aston_Martin_vehicles"
htmlResponse = requests.get(url)

soup = BeautifulSoup(htmlResponse.content, "html.parser")
links = soup.find_all("a")

for link in links:
    try:
        print(link["href"])
    except:
        print("#"*90)
        print(link)