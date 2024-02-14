from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options



def scrape_exterior_colors(driver, url):
    driver.get(url)
    # Get all elements with class "color-box"
    color_boxes = driver.find_elements(By.CLASS_NAME, "color-box")
    
    # Create a list to store the extracted data
    data = []
    
    # Iterate through each color box element
    for color_box in color_boxes:
        # Extract the "data-color-name" attribute
        color_name = color_box.get_attribute("data-color-name")
        
        # Extract the "background-color" attribute
        background_color = color_box.get_attribute("style").split(":")[1].strip()
        
        # Append the extracted data to the list
        data.append({"color_name": color_name, "background_color": background_color})
    
    # Return the extracted data
    return data

def scrape_interior_colors(driver, url):
    # Navigate to the webpage
    driver.get(url)
    
    # Find the interior-color-container div
    container = driver.find_element(By.CLASS_NAME, "interior-color-container")
    
    # Find all <p> tags within the container
    ps = container.find_elements(By.TAG_NAME, "p")
    
    # Extract the text from each <p> tag that does not have a class attribute
    text_list = [p.text for p in ps if not p.get_attribute("class")]
    
    # Return the list of extracted text
    return text_list

options = Options()
#options.preferences.update({"javascript.enabled": False})
driver = webdriver.Firefox(options=options)

print(scrape_exterior_colors(driver, "https://www.cars.com/research/acura-cl-2003/specs/"))
print(scrape_interior_colors(driver, "https://www.cars.com/research/acura-cl-2003/specs/"))