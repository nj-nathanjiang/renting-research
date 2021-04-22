from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time

CHROME_DRIVER_PATH = "/Users/user/Development/chromedriver"
ZILLOW_LINK = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
FORM_LINK = "GoogleFormLink"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15",
    "Accept-Language": "en-US"
}

response = requests.get(ZILLOW_LINK, headers=headers)
html_code = response.text

soup = BeautifulSoup(html_code, "html.parser")
unformatted_urls = soup.find_all(class_="list-card-link")
formatted_urls = []
for url in unformatted_urls:
    url = url.get("href")
    if "https://www.zillow.com" not in url:
        formatted_urls.append(f"https://www.zillow.com{url}")
    else:
        formatted_urls.append(url)

prices = soup.find_all(class_="list-card-price")
prices = [price.text.replace("/mo", "").replace("+ 1 bd", "").replace("+", "") for price in prices]

addresses = soup.find_all(class_="list-card-addr")
addresses = [address.text for address in addresses]

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

counter = 0
for url in formatted_urls:
    driver.get(FORM_LINK)

    the_url = url
    try:
        the_price = prices[counter]
    except IndexError:
        break
    the_address = addresses[counter]

    short_answers = driver.find_elements_by_class_name("exportInput")

    time.sleep(3)
    short_answers[0].send_keys(the_url)
    short_answers[1].send_keys(the_price)
    short_answers[2].send_keys(the_address)

    submit_button = driver.find_element_by_class_name("freebirdFormviewerViewNavigationSubmitButton")
    submit_button.click()

    counter += 1

time.sleep(30)
driver.quit()
