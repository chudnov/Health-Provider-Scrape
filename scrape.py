from bs4 import BeautifulSoup#extract the html from the request
from selenium import webdriver #deal with the dynamic javascript
import csv
import time

NUMBER_OF_PAGES = 627

#Load the path of the driver for use
def load_driver_path():
    path_file = open('DriverPath.txt', 'r')
    path = path_file.read().strip()
    path_file.close()
    return path

#Establish the webdriver
def link_driver(path_to_driver):
    #Establish the driver
    driver = webdriver.Chrome(path_to_driver)
    return driver

#  1. Loads the html data
#  2. Turns it into soup
def load_data(webdriver, URL, page):
    #Get the contents of the URL
    webdriver.get(URL)

    #returns the inner HTML as a string
    innerHTML = webdriver.page_source

    #turns the html into an object to use with BeautifulSoup library
    soup = BeautifulSoup(innerHTML, "html.parser")

    get_data(soup, page)

#closes the driver
def quit_driver(webdriver):
    webdriver.close()
    webdriver.quit()

## Now need to get the following from the page:
#    1. Name
#    2. Address
#    3. Phone #

# get the data
def get_data(soup, page):
    output_data = open('OutputData.csv', 'a')
    writer = csv.writer(output_data, delimiter='$', quoting=csv.QUOTE_NONE, escapechar=" ")

    print("Currently on page: " + str(page))

    for entry in soup.find_all('div', {'class' : "provider-card row"}):
        name = " " + entry.find('h4').get_text().strip()
        address = " " + entry.find('address', {'class': 'mb-0 ember-view'}).get_text().strip().replace('\n', '')
        phone_number = " " + entry.find('a', {'class': 'disable-pointer-events text-dark'}).find('span').get_text().strip()
        writer.writerow([name, address, phone_number])

    print("Data saved for " + str(page))

for i in range(1, NUMBER_OF_PAGES + 1):
    path = load_driver_path()
    driver = link_driver(path)

    URL = "https://myfindadoctor.bluecrossma.com/professional?saved_search_id=11&ci=DFT&geo_location=02119,boston,ma,city&network_id=311005011&page=" + str(i) + "&radius=10000&sort=Distance"
    load_data(driver, URL, i)
    if i == NUMBER_OF_PAGES:
        quit_driver(driver)
