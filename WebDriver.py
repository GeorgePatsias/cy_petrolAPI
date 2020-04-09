import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#sudo apt-get install chromium-browser
from config import CHROMEDRIVER


def WebDriverObj():
    try:
        chrome_options = Options()
        chrome_options.binary_location = '/usr/bin/chromium-browser'

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--ignore-certificate-errors')

        driver = webdriver.Chrome(CHROMEDRIVER, chrome_options=chrome_options)

        return driver

    except Exception as e:
        traceback.print_exc(e)
        return None
