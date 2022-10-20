from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def get_recent_roles():
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=C:\\Users\\hotsno\\coding\\linkedin-scraper\\selenium") 
    driver = webdriver.Chrome(chrome_options=chrome_options, service=ChromeService(executable_path=ChromeDriverManager().install()))
    driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3260030285&geoId=103644278&keywords=software%20engineer%20intern&location=United%20States&refresh=true&sortBy=DD")
    time.sleep(10)
    driver.implicitly_wait(5)

    roles = []
    positions = driver.find_elements(By.CSS_SELECTOR, ".job-card-container")
    for position in positions:
        company = position.find_element(By.CSS_SELECTOR, "a.job-card-container__company-name").text
        link = position.find_element(By.CSS_SELECTOR, "a.job-card-list__title").get_attribute('href').split('?eBP')[0]
        title = position.find_element(By.CSS_SELECTOR, "a.job-card-list__title").text
        picture = position.find_element(By.CSS_SELECTOR, "img.ember-view").get_attribute('src')
        if company != '':
            roles.append((company, title, link, picture))

    driver.quit()
    return roles

if __name__ == "__main__":
    print(get_recent_roles())
