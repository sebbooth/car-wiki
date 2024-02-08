import requests

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action": "parse",
    "page": "List of car brands",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

print(R.url)

print(DATA["parse"]["title"])
print(DATA["parse"]["pageid"])
