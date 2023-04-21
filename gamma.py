import selenium
from selenium import webdriver

url = "https://www.myfloridalicense.com/wl11.asp?mode=1&SID=&brd=&typ="
driver = webdriver.Chrome()
driver.get(url)
driver.refresh()
