from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from dotenv import load_dotenv
import os, time, json

load_dotenv()
LINKEDIN_URL = os.getenv('LINKEDIN_URL')
SELENIUM_USER_DATA_DIR = os.getenv('SELENIUM_USER_DATA_DIR')

def get_recent_roles():
    options = Options()
    options.add_argument(f"user-data-dir={SELENIUM_USER_DATA_DIR}")
    driver = webdriver.Chrome(options=options, service=ChromeService(executable_path=ChromeDriverManager().install()))

    # Open LinkedIn URL
    driver.get(LINKEDIN_URL)
    time.sleep(5) 

    # Need to scroll to load all the postings on the page
    header = driver.find_element(By.CSS_SELECTOR, ".jobs-search-results-list__header")
    scroll_origin = ScrollOrigin.from_element(header, 50, 100) # Offset: right/down
    for i in range(5):
        ActionChains(driver).scroll_from_origin(scroll_origin, 0, 1000).perform() # Scroll down
        time.sleep(1)

    # Get roles
    roles = []
    positions = driver.find_elements(By.CSS_SELECTOR, ".job-card-container")
    for position in positions:
        company = position.find_element(By.CSS_SELECTOR, ".job-card-container__primary-description").text
        link = position.find_element(By.CSS_SELECTOR, "a.job-card-list__title").get_attribute('href').split('?eBP')[0]
        title = position.find_element(By.CSS_SELECTOR, "a.job-card-list__title").text
        picture = position.find_element(By.CSS_SELECTOR, "img.ember-view").get_attribute('src')
        roles.append((company, title, link, picture))

    driver.quit()
    return roles

if __name__ == "__main__":
    roles = get_recent_roles()
    print(json.dumps(roles, indent=1))
