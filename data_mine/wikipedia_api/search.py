import requests

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action": "opensearch",
    "namespace": "0",
    "search": "Toyota",
    "limit": "5",
    "format": "json",
}

R = S.get(url=URL, params=PARAMS)
searchData = R.json()

pageTitles = searchData[1]
pageURLs = searchData[3]

print("\n"+pageTitles[0])
print(pageURLs[0])
