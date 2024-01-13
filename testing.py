from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pprint

# Set up the WebDriver (you may need to provide the path to your chromedriver executable)
driver = webdriver.Chrome()

url = 'https://caps.woking.gov.uk/online-applications/search.do?action=advanced'
driver.get(url)

# Input start and end dates
input_element1 = driver.find_element(By.ID, 'applicationReceivedStart')
input_element2 = driver.find_element(By.ID, 'applicationReceivedEnd')
input_element1.send_keys('01/01/2023')
input_element2.send_keys('12/01/2023')
time.sleep(5)
# Click the search button
search_element = driver.find_element(By.CLASS_NAME, 'recaptcha-submit')
search_element.click()
time.sleep(1)

# Wait for the page to load (you may need to adjust the waiting time)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, 'resultsPerPage')))
print('i')
# Get the page source after the search
page_source = driver.page_source
pprint.pprint(page_source)

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Locate and extract data (adjust this part based on your HTML structure)
# Example: Extract text from all paragraphs with a specific class
paragraphs = soup.find_all('div', class_='searchresult')
for paragraph in paragraphs:
    print(paragraph.text)
time.sleep(20)
# Close the browser window
driver.quit()
