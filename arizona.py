from pprint import pprint
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_driver():
    driver = webdriver.Chrome()
    return driver

def get_url(driver):
    url = "https://btr.az.gov/public/registered-professional-search"
    driver.get(url)
    return driver

def post_form(driver, f_name, l_name):
    f_name_ele = driver.find_element(By.ID, "edit-field-first-name-value").send_keys(f_name)
    l_name_ele = driver.find_element(By.ID, "edit-field-last-name-value").send_keys(l_name)
    apply_button_ele = driver.find_element(By.ID, "edit-submit-registered-professional-search").submit()
    return driver

def get_rows(driver):
    table_div = driver.find_element(By.CLASS_NAME, "view-content")
    table = table_div.find_element(By.TAG_NAME, "table")
    table_body = table.find_element(By.TAG_NAME, "tbody")
    rows = table_body.find_elements(By.TAG_NAME, "tr")

    return rows

def get_results(rows):
    results = {
        "name":[],
        "license":[],
        "status":[],
        "Dicipline":[],
        "Issue Date":[],
        "Expiration":[],
        "Address":[]
    }
    
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        for i in range(len(cells)):
            pprint(cells[i].text)
            if i == 0:
                results["license"].append(cells[i].text)
            elif i == 1:
                results["name"].append(cells[i].text)
            elif i == 2:
                results["status"].append(cells[i].text)
            elif i == 3:
                results["Dicipline"].append(cells[i].text)
            elif i == 4:
                results["Issue Date"].append(cells[i].text)
            elif i == 5:
                results["Expiration"].append(cells[i].text)
            elif i == 6:
                results["Address"].append(cells[i].text)
    
    return results

if __name__ == "__main__":
    driver = get_driver()
    driver = get_url(driver)
    first_name = input("Enter First Name: ").strip().capitalize()
    last_name = input("Enter Last Name: ").strip().capitalize()
    driver = post_form(driver, first_name, last_name)
    rows = get_rows(driver)
    driver.implicitly_wait(20)

    result_list = get_results(rows)
    pprint(result_list)
    driver.quit()