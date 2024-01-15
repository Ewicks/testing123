from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
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

# lists
row_list = []
address_list = []
name_list = []
data = []


# Set up the WebDriver (you may need to provide the path to your chromedriver executable)
driver = webdriver.Chrome()

url = 'https://publicaccess.kingston.gov.uk/online-applications/search.do?action=advanced'
driver.get(url)

# Input start and end dates
input_element1 = driver.find_element(By.ID, 'applicationReceivedStart')
input_element2 = driver.find_element(By.ID, 'applicationReceivedEnd')
input_element1.send_keys('20/12/2023')
input_element2.send_keys('12/01/2024')
# Click the search button
search_element = driver.find_element(By.CLASS_NAME, 'recaptcha-submit')
search_element.click()

# Wait for the page to load (you may need to adjust the waiting time)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, 'resultsPerPage')))

# Select 100 and submit to show max results
num_results_element = Select(driver.find_element(By.ID, 'resultsPerPage'))
num_results_element.select_by_visible_text('100')
num_results_go = driver.find_element(By.CLASS_NAME, 'primary')
num_results_go.click()

next_a_tag = None
multiple_pages = True

while (multiple_pages):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'resultsPerPage')))
    # Get the page source after the search
    page_source = driver.page_source

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    searchResultsPage = soup.find('div', class_='col-a')
    searchResults = searchResultsPage.find_all('li', class_='searchresult')

    row_list = []

    for row in searchResults:

        if (re.search(words_search_for, row.text, flags=re.I)):
            row_list.append(row)
            

    for row in row_list:
        # Find the address and add to address_list
        address_div = row.find('p', class_='address')
        address = address_div.text.strip()
        address_list.append(address)

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
        info_soup = BeautifulSoup(name_page_source, 'html.parser')

        applicant_row = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//th[text()="Applicant Name"]/following-sibling::td'))
        )

        # Extract the "Applicant Name" text content
        applicant_name_value = applicant_row.text if applicant_row else None
        print(applicant_name_value)

        name_list.append(applicant_name_value)
        driver.back()
        driver.back()
        driver.execute_script("location.reload(true);")

    try:
        next_a_tag = driver.find_element(By.CLASS_NAME, 'next')
        # If the element is found, you can interact with it here
        multiple_pages = True
        next_a_tag.click()
        time.sleep(10)
        
    except NoSuchElementException:
        # If the element is not found, handle the exception here
        multiple_pages = False
        print("Element not found. Continuing without clicking.")



merge_data = zip(name_list, address_list)

for item in merge_data:
    data.append(item)

print(data)

# Close the browser window
driver.quit()
