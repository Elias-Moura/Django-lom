from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import os

DEFAULT_OPTIONS = ('--window-size=1100,1000', '--start-maximized', '--no-sandbox', '--disable-dev-shm-usage')

def make_chrome_browser(*options):
    service = Service(ChromeDriverManager().install())
    chrome_options = ChromeOptions()
    
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)
    
    if os.getenv('CHROME_DRIVER_HEADLESS') == '1':
        chrome_options.add_argument('--headless')
    
    chrome_prefs = dict()
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    # chrome_options.experimental_options["prefs"] = chrome_prefs
    # # chrome_options.add_argument(
    # #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
    # #     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    # # )

    driver = Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(30)
    return driver

