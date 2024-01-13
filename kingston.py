from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time
import pprint

wordlist = ['rear']
# wordlist = ['loft','ground','rear', 'erection']

def convert(s):
 
    # initialization of string to ""
    new = ""
 
    # traverse in the string
    for x in s:
        new = new + x + '|'
 
    # return string
    return new

words = convert(wordlist)
words_search_for = words.rstrip(words[-1])
print(words_search_for)


rowList = []
addressList = []
nameList = []

# Set up the WebDriver (you may need to provide the path to your chromedriver executable)
driver = webdriver.Chrome()

url = 'https://publicaccess.kingston.gov.uk/online-applications/search.do?action=advanced'
driver.get(url)

# Input start and end dates
input_element1 = driver.find_element(By.ID, 'applicationReceivedStart')
input_element2 = driver.find_element(By.ID, 'applicationReceivedEnd')
input_element1.send_keys('01/01/2024')
input_element2.send_keys('12/01/2024')
# Click the search button
search_element = driver.find_element(By.CLASS_NAME, 'recaptcha-submit')
search_element.click()

# Wait for the page to load (you may need to adjust the waiting time)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, 'resultsPerPage')))

# Get the page source after the search
page_source = driver.page_source

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

searchResultsPage = soup.find('div', class_='col-a')
searchResults = searchResultsPage.find_all('li', class_='searchresult')

for row in searchResults:

    if (re.search(words_search_for, row.text, flags=re.I)):
        rowList.append(row)
        

   
for row in rowList:
    a_tag = row.find('a')
    link_text = a_tag.get_text(strip=True)
    element = driver.find_element(By.LINK_TEXT, link_text)

    # Now, you can perform actions on the found element
    # For example, click the link
    element.click()
    driver.execute_script("window.scrollTo(0, window.scrollY + 300);")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'subtab_details')))

    subtab = driver.find_element(By.ID, 'subtab_details')
    subtab.click()
    driver.execute_script("window.scrollTo(0, window.scrollY + 320);")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'row0')))
    name_page_source = driver.page_source
    name_soup = BeautifulSoup(name_page_source, 'html.parser')
    name_rows = name_soup.find_all('tr', class_='row0')
    if len(name_rows) >= 3:
        name_row = name_rows[2]
    else: 
        nameList.append('ERROR ------ STOP')
    name = name_row.find('td')
    nameList.append(name.text.strip())
    print(nameList)
    driver.back()
    driver.back()
    driver.execute_script("location.reload(true);")

    
# for section in sections:
#     print(section.get_text())


# paragraphs = soup.find_all('p', class_='address')


# for paragraph in paragraphs:
#     addressList.append(paragraph.get_text().strip())
    




# print(addressList)
# Close the browser window
driver.quit()
