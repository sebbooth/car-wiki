from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox()
    # Navigate to the website
driver.get("https://www.cars.com/research/")  # Replace with the website URL

# Find the search bar elements
make_select = driver.find_element(By.ID, "make-select")
model_select = driver.find_element(By.ID, "model-select")
year_select = driver.find_element(By.ID, "year-select")
search_button = driver.find_element(By.CLASS_NAME , "js-mmy-search-button")

# Loop through the makes
for make in make_select.find_elements(By.TAG_NAME, "option"):
    # Select the make
    make.click()
    
    # Loop through the models
    for model in model_select.find_elements(By.TAG_NAME, "option"):
        # Select the model
        model.click()
        
        # Loop through the years
        for year in year_select.find_elements(By.TAG_NAME, "option"):
            # Select the year
            year.click()
            
            # Extract the values from the input fields
            make_value = make_select.get_attribute("value")
            model_value = model_select.get_attribute("value")
            year_value = year_select.get_attribute("value")

            # Check if all input fields have non-empty values
            if make_value and model_value and year_value:
                # Build the URL using the values and hyphens
                url = f"https://www.cars.com/research/{make_value}-{model_value}-{year_value}"
                
                # Open the file in append mode
                with open("model_links.txt", "a") as f:
                    # Write the URL to the file
                    f.write(url + "\n")

            else:
                print("One or more input fields are empty!")

# Close the browser
driver.quit()
