import requests

url = "https://en.wikipedia.org/wiki/List_of_car_brands"

htmlResponse = requests.get(url)

htmlText = htmlResponse.text

htmlResponse.close()

with open("brand_list.html", "w", encoding="utf-8") as f:
    f.write(htmlText)

f.close()