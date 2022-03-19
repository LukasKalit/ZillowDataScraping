from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
from bs4 import BeautifulSoup

# Options for webdriver
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(chrome_options=chrome_options, service=Service(ChromeDriverManager().install()))

html_doc = "https://docs.google.com/forms/d/e/1FAIpQLSeKnjVVY_2FlXUIWkqArKIQjBV9aqBImGZmWxZN4FyWrPuP5A/viewform?usp=sf_link"
html_site = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22mapBounds%22%3A%7B%22west%22%3A-122.5490287680664%2C%22east%22%3A-122.34818495703125%2C%22south%22%3A37.70361535630771%2C%22north%22%3A37.81245964609993%7D%2C%22mapZoom%22%3A13%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22sort%22%3A%7B%22value%22%3A%22days%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22pagination%22%3A%7B%7D%7D"

# Get website and scrolling down for downloading all data
driver.get(html_site)
box = driver.find_element(By.ID, "search-page-list-container")
time.sleep(3)
for i in range(10):
    time.sleep(0.2)
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight", box)

# Taking data
full_site = driver.find_element(By.CSS_SELECTOR, "body")
data = full_site.get_attribute('innerHTML')

# Using BeautifulSoup for scraping data and making a lists of data
soup = BeautifulSoup(data, 'html5lib')
list_of_announcement = soup.find("ul", {"class": "photo-cards photo-cards_wow photo-cards_short"})
working_list = list_of_announcement.select(".list-card-info a")

list_of_links = []
for a in working_list:
    if "https" in a["href"]:
        list_of_links.append(a["href"])
    else:
        full_link = "https://www.zillow.com" + a["href"]
        list_of_links.append(full_link)

working_list = list_of_announcement.select(".list-card-info address")
list_of_address = [address.get_text().split(" | ")[-1] for address in working_list]

working_list = list_of_announcement.select(".list-card-price")

list_of_prices = [price.get_text()[:6] for price in working_list]

print(list_of_address)
print(list_of_links)
print(list_of_prices)

print(len(list_of_address))
print(len(list_of_links))
print(len(list_of_prices))

# Insert data to google form
driver.get(html_doc)
time.sleep(1)

for i in range(len(list_of_address)):
    address_input = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                                    "//*[@id='mG61Hd']/div[2]"
                                                                                    "/div/div[2]/div[1]/div/div"
                                                                                    "/div[2]/div/div[1]/div/"
                                                                                    "div[1]/input")))
    price_input = driver.find_element(By.XPATH,
                                      "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div"
                                      "[1]/input")
    link_input = driver.find_element(By.XPATH,
                                     "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div"
                                     "[1]/input")
    send_button = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span/span")
    address_input.send_keys(list_of_address[i])
    price_input.send_keys(list_of_prices[i])
    link_input.send_keys(list_of_links[i])
    send_button.click()
    back_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]"
                                                                                            "/div[1]/div/div[4]/a")))
    back_button.click()
