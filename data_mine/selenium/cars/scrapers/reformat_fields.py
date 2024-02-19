from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, time
sys.path.insert(0, '../../')
from selenium_resources.file_io import *

field_names = read_carsdotcom_json("../data/fields.json")
field_names2 = {}
for cat in field_names:
    for field in field_names[cat]:
        if field != "":
            field_names2[field] = cat

print(field_names2)