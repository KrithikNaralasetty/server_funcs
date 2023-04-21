from bs4 import BeautifulSoup

from pprint import pprint
from urllib.parse import urljoin
import webbrowser
import sys

from alpha import get_all_forms, get_form_details, session

url = "https://www.myfloridalicense.com/wl11.asp?mode=1&SID=&brd=&typ="
all_forms = get_all_forms(url)
# get the first form (edit this as you wish)
# first_form = get_all_forms(url)[0]
for i, f in enumerate(all_forms, start=1):
    form_details = get_form_details(f)
    print(f"{i} #")
    pprint(form_details)
    print("="*50)

choice = int(input("Enter form indice: "))
# extract all form details
form_details = get_form_details(all_forms[choice-1])
pprint(form_details)

# Data of the form
data = {}
for input_tag in form_details["inputs"]:
    if input_tag["type"] == "hidden":
        if input_tag["name"] == "hFirstName":
            data[input_tag["name"]] = "John"
        elif input_tag["name"] == "hLastName":
            data[input_tag["name"]] = "Smith"
        else:
            data[input_tag["name"]] = input_tag["value"]
    elif input_tag["type"] == "select":
        data[input_tag["name"]] = input_tag["value"]
    elif input_tag["type"] != "submit":
        # all others except submit, prompt the user to set it
        data[input_tag["name"]] = input_tag["value"]

# join the url with the action (form request URL)
url = urljoin(url, form_details["action"])
if form_details["method"] == "post":
    res = session.post(url, data=data)
    pprint(res)
elif form_details["method"] == "get":
    res = session.get(url, params=data)
    pprint(res)

soup = BeautifulSoup(res.content, "html.parser")
for link in soup.find_all("link"):
    try:
        link.attrs["href"] = urljoin(url, link.attrs["href"])
    except:
        pass
for script in soup.find_all("script"):
    try:
        script.attrs["src"] = urljoin(url, script.attrs["src"])
    except:
        pass
for img in soup.find_all("img"):
    try:
        img.attrs["src"] = urljoin(url, img.attrs["src"])
    except:
        pass
for a in soup.find_all("a"):
    try:
        a.attrs["href"] = urljoin(url, a.attrs["href"])
    except:
        pass

# write the page content to a file
open("page.html", "w").write(str(soup))
