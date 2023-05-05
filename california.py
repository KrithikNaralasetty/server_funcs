from pprint import pprint
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_driver():
    driver = webdriver.Chrome()
    return driver

def get_url(driver):
    url = "https://search.dca.ca.gov/"
    driver.get(url)
    return driver

def post_form(driver, f_name, l_name):
    f_name_ele = driver.find_element(By.ID, "firstName").send_keys(f_name)
    l_name_ele = driver.find_element(By.ID, "lastName").send_keys(l_name)
    apply_button_ele = driver.find_element(By.ID, "srchSubmitHome").submit()
    return driver

def get_rows(driver):
    main_form = driver.find_element(By.ID, "mainForm")
    list_of_items = main_form.find_element(By.ID, "wrapper")
    main_div = list_of_items.find_element(By.ID, "main")
    items_of_results = main_div.find_elements(By.TAG_NAME, "article")
    
    # Removing the last element as it is not a result
    items_of_results = items_of_results[:-1]
    
    return items_of_results

def get_results(driver, items):

    # Empty dictionary to store the results
    results = {
        "name":[],
        "license":[],
        "status":[],
        "Dicipline":[],
        "Issue Date":[],
        "Expiration":[],
        "Address":[]
    }

    # Loop through each article tag
    for article in range(len(items)):
        # Getting the id of each more details button
        id = "mD"+str(article)
        pprint(id)

        # Getting the more details page reference
        more_details_element = driver.find_element(By.ID, id)
        current_more_detail_url = more_details_element.get_attribute("href")

        # Loading the more details page
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(current_more_detail_url)
        driver.implicitly_wait(20)

        # Getting the details of the user
        main_element_details = driver.find_element(By.ID, "main")
        pprint(main_element_details.text)
        # article_element = main_element_details.find_element(By.TAG_NAME, "article")
        # header_element = article_element.find_element(By.TAG_NAME, "header")

        # # Header has 2 div elements. 
        # # First div element has the Details
        # # Second div element has the Issue Date and Expiration
        
        # # Getting the details of the user
        # details_element = header_element.find_element(By.CLASS_NAME, "title")
        # license_number_text = details_element.find_element(By.ID, "licDetail").text
        # license_number = license_number_text.split(":")[1].strip()
        # name_text = details_element.find_element(By.ID, "name").text.strip()
        # name = name_text.split(":")[1].strip().split(" ")
        # name_full = name[1] + " " + name[0][:-1]
        # license_type = details_element.find_element(By.ID, "licType").text.split(":")[1].strip()
        # status = details_element.find_element(By.ID, "primaryStatus").text.split(":")[1].strip()
        # address = details_element.find_element(By.ID, "address").text
        # if(len(address.split("\n")) < 2):
        #     address = "N/A"
        # else:
        #     address = address.split("\n")[1].strip()
        # dates_element = header_element.find_element(By.CLASS_NAME, "meta")
        # issue_date = dates_element.find_element(By.ID, "issueDate").text.strip()
        # expiration_date = dates_element.find_element(By.ID, "expDate").text.strip()

        # # Adding the results to the dictionary
        
        # results["name"].append(name_full)
        # results["license"].append(license_number)
        # results["status"].append(status)
        # results["Dicipline"].append(license_type)
        # results["Issue Date"].append(issue_date)
        # results["Expiration"].append(expiration_date)
        # results["Address"].append(address)

        # Closing the more details page and switching back to the results page
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        if(article == 6):
            break

    return results

if __name__ == "__main__":

    # Get the driver
    driver = get_driver()
    driver = get_url(driver)

    # Get user input
    
    first_name = "John" # input("Enter First Name: ").strip().capitalize()
    last_name = "Smith" # input("Enter Last Name: ").strip().capitalize()

    # Submit the form    
    driver = post_form(driver, first_name, last_name)

    #  Wait for the page to load
    driver.implicitly_wait(20)
    rows = get_rows(driver)

    result_list = get_results(driver, rows)
    pprint(result_list)

    # Close the driver
    driver.quit()