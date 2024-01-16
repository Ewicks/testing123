
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import re
import time
import pprint

wordlist = ['rear']

# wordlist = ['loft','ground','rear']
row_list = []
address_list = []
name_list = []
data = []


def convert(s):
 
    # initialization of string to ""
    new = ""
 
    # traverse in the string
    for x in s:
        new = new + x + '|'
 
    # return string
    return new

def format_address(address):
    formatted_address = address.replace('\n', ' ')
    address_list.append(formatted_address)


words = convert(wordlist)
words_search_for = words.rstrip(words[-1])


# Set up the WebDriver (you may need to provide the path to your chromedriver executable)
driver = webdriver.Chrome()

url = 'https://www2.richmond.gov.uk/lbrplanning/Planning_Report.aspx'
driver.get(url)

# Input start and end dates
input_element1 = driver.find_element(By.ID, 'ctl00_PageContent_dpValFrom')
input_element2 = driver.find_element(By.ID, 'ctl00_PageContent_dpValTo')
input_element1.send_keys('01/01/2024')
input_element2.send_keys('02/01/2024')
# Click the search button
search_element = driver.find_element(By.CLASS_NAME, 'btn-primary')


# Wait for the cookie consent popup to appear
wait = WebDriverWait(driver, 10)
cookie_popup = wait.until(EC.presence_of_element_located((By.ID, 'ccc-end')))

# Locate and click the "Accept" button
accept_button = cookie_popup.find_element(By.ID, 'ccc-dismiss-button')
accept_button.click()

# Select 500 to show max results
num_results_element = Select(driver.find_element(By.ID, 'ctl00_PageContent_ddLimit'))
num_results_element.select_by_visible_text('500')

# Click submit for advanced results page
search_element.click()

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'infocontent')))
# driver.execute_script("location.reload(true);")
# ctl00_PageContent_lbl_APPS


# Get the page source after the search
page_source = driver.page_source

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')


span_div = driver.find_element(By.ID, 'ctl00_PageContent_lbl_APPS')
num_results = span_div.find_element(By.TAG_NAME, 'strong')

if (int(num_results.text) == 500):
    print('Results over 500 please alter your search results')
    driver.quit()
else:
    print('Number of results for this search is: ' + num_results.text)



searchResultsPage = soup.find('ul', class_='planning-apps')
searchResults = searchResultsPage.find_all('li')

# search the description but append all rows with key words in description to row_list
for row in searchResults:
    address_divs = row.find_all('p')
    address_desc = address_divs[1].text

    if (re.search(words_search_for, address_desc, flags=re.I)):
        row_list.append(row)
   

for row in row_list:
    # Find the address and add to address_list
    address_div = row.find('h3')
    address = address_div.text.strip()
    format_address(address)

    a_tag = row.find('a')
    href_value = a_tag.get('href')
    element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, f"//a[@href='{href_value}']"))
    )
    element.click()
    try:
        subtab = None
        subtab = driver.find_element(By.ID, 'ctl00_PageContent_btnShowApplicantDetails')
    except:
        driver.back()
        name_list.append('n/a')
        continue

   
    subtab.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'ctl00_PageContent_lbl_Applic_Name')))
    name_page_source = driver.page_source
    name_soup = BeautifulSoup(name_page_source, 'html.parser')
    name = name_soup.find('span', id='ctl00_PageContent_lbl_Applic_Name')
    name_list.append(name.text.strip())

    driver.back()
    driver.back()


merge_data = zip(name_list, address_list)

for item in merge_data:
    data.append(item)

print(data)


# Close the browser window
driver.quit()
