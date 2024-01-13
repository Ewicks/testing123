from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pprint

addressList = []

# Set up the WebDriver (you may need to provide the path to your chromedriver executable)
driver = webdriver.Chrome()

url = 'https://caps.woking.gov.uk/online-applications/search.do?action=advanced'
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

sections = soup.find('div', class_='col-a')
testing = sections.find_all('li', class_='searchresult')

for test1 in testing:
    a_tag = test1.find('a')

    if a_tag:
        link_text = a_tag.get_text(strip=True)
        element = driver.find_element(By.LINK_TEXT, link_text)

        # Now, you can perform actions on the found element
        # For example, click the link
        element.click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'subtab_details')))

        subtab = driver.find_element(By.ID, 'subtab_details')
        subtab.click()

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'row0')))
        name_page_source = driver.page_source
        name_soup = BeautifulSoup(name_page_source, 'html.parser')
        name_row = name_soup.find('tr', class_='row0')
        name = name_row.find('td')

        print(name)
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
